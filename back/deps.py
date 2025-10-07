from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from back.database.models import UserModel
from back.schemas import UserInfo
from database import DataBaseCrud

db = DataBaseCrud()


async def get_db_session() -> AsyncSession:
    async with db.session_maker() as session:
        yield session


async def get_user(request: Request, session: AsyncSession = Depends(get_db_session)) -> UserInfo:
    yield UserInfo.model_validate(await db.get_user(session, UserModel(username=request.cookies.get('username'))))
