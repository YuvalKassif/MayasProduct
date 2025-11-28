from __future__ import annotations

from typing import Optional

from fastapi import Cookie, Depends, Header, HTTPException, status

from .jwt import decode_token


ACCESS_COOKIE = "access_token"


def get_current_user_id(
    access_cookie: Optional[str] = Cookie(default=None, alias=ACCESS_COOKIE),
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
) -> str:
    token: Optional[str] = None
    if access_cookie:
        token = access_cookie
    elif authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return sub
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

