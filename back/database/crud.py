from sqlalchemy import select

from .models import *
from .core import *


class DataBaseCrud:
    instance_ = None

    def __new__(cls):
        if cls.instance_ is None:
            cls.instance_ = super().__new__(cls)
        return cls.instance_

    def __init__(self, engine=engine, session_maker=sm):
        self.engine = engine
        self.session_maker = session_maker

    async def create_tables(self):
        print('creating tables')
        async with self.engine.begin() as conn:
            print(Base.metadata.tables)
            await conn.run_sync(Base.metadata.create_all)

    async def add_user(self, user: UserModel) -> int:
        async with self.session_maker() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user.id

    async def get_user(self, user: UserModel):
        async with self.session_maker() as session:
            user = await session.scalar(select(UserModel).filter_by(username=user.username))
            return user

    async def get_user_by_id(self, userid: int) -> UserModel | None:
        async with self.session_maker() as session:
            return await session.get(UserModel, userid)
