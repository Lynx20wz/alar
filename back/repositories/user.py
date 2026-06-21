from typing import override

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models import UserModel

from .base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    model: type[UserModel] = UserModel

    @override
    async def get(self, id: int) -> UserModel | None:
        return await self.session.scalar(
            select(UserModel)
            .options(selectinload(UserModel.stacks), selectinload(UserModel.social_links))
            .where(UserModel.id == id)
        )

    async def get_by_username(self, username: str) -> UserModel | None:
        return await self.session.scalar(
            select(UserModel)
            .options(selectinload(UserModel.stacks), selectinload(UserModel.social_links))
            .where(UserModel.username == username)
        )
