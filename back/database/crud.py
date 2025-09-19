from sqlalchemy import select

from .models import *
from .core import *


class DataBaseCrud:
    def __init__(self, engine=engine, session_maker=sm):
        self.engine = engine
        self.session_maker = session_maker

    async def create_tables(self):
        print('creating tables')
        async with self.engine.begin() as conn:
            print(Base.metadata.tables)
            await conn.run_sync(Base.metadata.drop_all)  # TODO remove after development
            await conn.run_sync(Base.metadata.create_all)

    async def add_user(self, user: UserModel):
        with open('avatar.png', 'wb') as f:
            f.write(user.avatar)
        async with self.session_maker() as session:
            session.add(user)
            await session.commit()

    async def get_user(self, user: UserModel):
        async with self.session_maker() as session:
            user = await session.scalar(
                select(UserModel).where(
                    (UserModel.email == user.email) & (UserModel.password == user.password)
                )
            )
            return user
