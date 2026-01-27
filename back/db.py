__all__ = ('sm', 'Base')

from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import config

sm: async_sessionmaker


async def db_init():
    db_path = Path(config.DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.touch()

    engine = create_async_engine(
        url=f'sqlite+aiosqlite:///{db_path}',
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    global sm
    sm = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with sm() as session:
        yield session


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
