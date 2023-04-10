from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import AsyncSessionLocal


async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
