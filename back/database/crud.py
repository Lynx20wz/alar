from sqlalchemy import select
from passlib.hash import bcrypt

from .models import *
from .core import *
from exceptions import NotCorrectPassword


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
            user.password = bcrypt.hash(user.password)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user.id

    async def get_user(self, user: UserModel, check_password: bool = False) -> UserModel | None:
        async with self.session_maker() as session:
            userDB = await session.scalar(select(UserModel).filter_by(username=user.username))
            if not userDB:
                return None
            elif check_password and not bcrypt.verify(user.password, userDB.password):
                raise NotCorrectPassword()
            return userDB

    async def get_user_by_id(self, userid: int) -> UserModel | None:
        async with self.session_maker() as session:
            return await session.get(UserModel, userid)
