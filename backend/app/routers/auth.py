from __future__ import annotations

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..db import get_session
from ..models.user import User
from ..schemas.auth import LoginRequest, RegisterRequest, UserOut
from ..security.jwt import create_access_token, create_refresh_token, decode_token
from ..security.passwords import hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


COOKIE_ACCESS = "access_token"
COOKIE_REFRESH = "refresh_token"


def set_auth_cookies(resp: Response, access: str, refresh: str) -> None:
    common = {
        "httponly": True,
        "secure": False if settings.environment == "local" else True,
        "samesite": "lax",
        "domain": settings.cookie_domain,
        "path": "/",
    }
    resp.set_cookie(COOKIE_ACCESS, access, **common)
    resp.set_cookie(COOKIE_REFRESH, refresh, **common)


def clear_auth_cookies(resp: Response) -> None:
    resp.delete_cookie(COOKIE_ACCESS, path="/", domain=settings.cookie_domain)
    resp.delete_cookie(COOKIE_REFRESH, path="/", domain=settings.cookie_domain)


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    resp: Response,
    session: AsyncSession = Depends(get_session),
):
    email = payload.email.lower()
    existing = await session.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(email=email, password_hash=hash_password(payload.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    set_auth_cookies(resp, access, refresh)
    return UserOut(id=user.id, email=user.email, email_verified=user.email_verified, role=user.role)


@router.post("/login", response_model=UserOut)
async def login(
    payload: LoginRequest,
    resp: Response,
    session: AsyncSession = Depends(get_session),
):
    email = payload.email.lower()
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if (
        not user
        or not user.password_hash
        or not verify_password(payload.password, user.password_hash)
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    set_auth_cookies(resp, access, refresh)
    return UserOut(id=user.id, email=user.email, email_verified=user.email_verified, role=user.role)


@router.post("/refresh")
async def refresh(
    resp: Response,
    refresh_token: str | None = None,
    refresh_cookie: str | None = Cookie(default=None, alias=COOKIE_REFRESH),
):
    # Accept from explicit body param or cookie
    token = refresh_token or refresh_cookie
    if token is None:
        raise HTTPException(status_code=400, detail="No refresh token provided")
    try:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=400, detail="Invalid token payload")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    access = create_access_token(sub)
    new_refresh = create_refresh_token(sub)
    set_auth_cookies(resp, access, new_refresh)
    return {"status": "ok"}


@router.post("/logout", status_code=204)
async def logout(resp: Response):
    clear_auth_cookies(resp)
    return Response(status_code=204)


@router.get("/me", response_model=UserOut)
async def me(
    access_token: str | None = None,
    access_cookie: str | None = Cookie(default=None, alias=COOKIE_ACCESS),
    session: AsyncSession = Depends(get_session),
):
    # Prefer explicit param; fall back to cookie for browser flows
    token = access_token or access_cookie
    if not token:
        raise HTTPException(status_code=401, detail="Missing access token")
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=400, detail="Invalid token type")
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=400, detail="Invalid token payload")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    result = await session.execute(select(User).where(User.id == sub))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(id=user.id, email=user.email, email_verified=user.email_verified, role=user.role)
