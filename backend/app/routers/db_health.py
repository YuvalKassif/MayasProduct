from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session


router = APIRouter(tags=["health"])


@router.get("/health/db")
async def health_db(session: AsyncSession = Depends(get_session)):
    try:
        res = await session.execute(text("SELECT 1"))
        ok = res.scalar_one() == 1
        return {"database": "ok" if ok else "error"}
    except Exception:
        return {"database": "error"}
