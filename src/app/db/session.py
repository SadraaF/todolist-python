"""Database session and engine configuration for SQLAlchemy."""
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(settings.DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency to get an async database session.

    Yields a session from the session factory and ensures it is closed
    after the request is finished.

    :yield: An asynchronous database session.
    """
    async with AsyncSessionLocal() as session:
        yield session