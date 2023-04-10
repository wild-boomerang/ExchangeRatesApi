from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
