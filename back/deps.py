__all__ = ('get_db_session', 'get_current_user', 'AsyncSession')

from re import A
from typing import AsyncGenerator
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database import DataBaseCrud
from database.models import UserModel
from schemas import UserInfo

db = DataBaseCrud()


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with db.session_maker() as session:
        yield session


async def get_current_user(
    request: Request, session: AsyncSession = Depends(get_db_session)
) -> AsyncGenerator[UserInfo | None]:
    username = request.cookies.get('username')
    if not username:
        yield None
    user = await db.get_user(session, UserModel(username=username))
    if not user:
        yield None
    else:
        yield UserInfo.model_validate(user)
