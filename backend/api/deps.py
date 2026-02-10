"""
API dependencies and utilities
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting database sessions
    """
    async with SessionLocal() as session:
        yield session
