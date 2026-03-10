"""
Database engine and session factory.

Uses SQLAlchemy async engine backed by asyncpg for PostgreSQL 16 + pgvector.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(
    settings.database_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=settings.app_debug,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""
    pass


async def init_db() -> None:
    """Create all tables on startup (development only; use Alembic in production)."""
    if not settings.is_production:
        async with engine.begin() as conn:
            from app.models import debate, document, persona, user  # noqa: F401
            await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Dispose the async engine connection pool."""
    await engine.dispose()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a database session per request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
