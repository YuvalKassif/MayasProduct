from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .config import settings

engine: AsyncEngine | None = None
SessionLocal: async_sessionmaker[AsyncSession] | None = None


def init_engine() -> None:
    global engine, SessionLocal
    if engine is None:
        engine = create_async_engine(settings.database_url, future=True, echo=False)
        SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if SessionLocal is None:
        init_engine()
    assert SessionLocal is not None
    async with SessionLocal() as session:
        yield session


async def ping_db(session: AsyncSession = Depends(get_session)) -> bool:
    try:
        result = await session.execute(text("SELECT 1"))
        row = result.scalar_one()
        return row == 1
    except Exception:
        return False
