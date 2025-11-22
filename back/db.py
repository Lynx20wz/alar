__all__ = ('engine', 'sm', 'Base')

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import config


engine = create_async_engine(
    url=f'sqlite+aiosqlite:///{config.DB_PATH}',
    echo=False,
)

sm = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    return sm()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
