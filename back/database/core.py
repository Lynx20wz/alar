__all__ = ('engine', 'sm', 'Base')

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from config import config


engine = create_async_engine(
    url=f'sqlite+aiosqlite:///{config.DB_PATH}',
    echo=False,
)

sm = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
