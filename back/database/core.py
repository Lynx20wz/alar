__all__ = ('engine', 'sm', 'Base')

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from config import config


engine = create_async_engine(
    url=f'sqlite+aiosqlite:///{config.DB_PATH}',
    echo=True,
)

sm = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
