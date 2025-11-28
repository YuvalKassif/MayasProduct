from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from ..config import settings

ALG = "HS256"


def _exp(minutes: int | None = None, days: int | None = None) -> datetime:
    delta = timedelta(minutes=minutes or 0, days=days or 0)
    return datetime.now(UTC) + delta


def create_access_token(sub: str) -> str:
    payload: dict[str, Any] = {
        "sub": sub,
        "type": "access",
        "exp": _exp(minutes=settings.jwt_access_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALG)


def create_refresh_token(sub: str) -> str:
    payload: dict[str, Any] = {
        "sub": sub,
        "type": "refresh",
        "exp": _exp(days=settings.jwt_refresh_days),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALG)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret, algorithms=[ALG])
