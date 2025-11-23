from typing import Optional

from exceptions import NotCorrectPassword, UserAlreadyExists, UserNotFound
from models import UserModel
from repository import UserRepository
from schemas import LikesInfo, LikesType, UserRegisterData

from .base import BaseService


class UserService(BaseService[UserRepository]):
    repo = UserRepository

    def _get_user_or_raise(self, user: UserModel | None) -> UserModel:
        if not user:
            raise UserNotFound()
        return user

    async def get_user_by_id(self, user_id: int) -> UserModel:
        return self._get_user_or_raise(await self.repository.get(user_id))

    async def get_user_by_username(self, username: str) -> Optional[UserModel]:
        return self._get_user_or_raise(await self.repository.get_by(username=username))

    async def get_base_info(
        self, user_id: Optional[int] = None, username: Optional[str] = None
    ) -> tuple[int, str]:
        if user_id:
            user = self._get_user_or_raise(await self.get_user_by_id(user_id))
        elif username:
            user = self._get_user_or_raise(await self.get_user_by_username(username))
        else:
            raise ValueError

        return user.id, user.username

    async def login(self, username: str, password: str) -> UserModel:
        user = self._get_user_or_raise(await self.get_user_by_username(username))

        if not user.check_password(password):
            raise NotCorrectPassword()

        return user

    async def get_follows(self, user_id: int) -> LikesInfo:
        user = self._get_user_or_raise(await self.get_user_by_id(user_id))

        return LikesInfo(
            type=LikesType.users,
            total=len(user.like_users_relations),
            objects=[relation.liked_user for relation in user.like_users_relations],
        )

    async def get_followers(self, user_id: int) -> LikesInfo:
        user = self._get_user_or_raise(await self.get_user_by_id(user_id))

        return LikesInfo(
            type=LikesType.users,
            total=len(user.like_by_users_relations),
            objects=[relation.user for relation in user.like_by_users_relations],
        )

    async def get_liked_posts(self, user_id: int) -> LikesInfo:
        user = self._get_user_or_raise(await self.get_user_by_id(user_id))

        return LikesInfo(
            type=LikesType.posts,
            total=len(user.like_posts_relations),
            objects=[relation.post for relation in user.like_posts_relations],
        )

    async def add_user(self, data: UserRegisterData) -> UserModel:
        if await self.get_user_by_username(data.username):
            raise UserAlreadyExists()
        
        user_model = UserModel(
            username=data.username,
            email=data.email,
            password=data.password,
            banner=data.banner.read() if data.banner else None,
            avatar=data.avatar.read() if data.avatar else None,
        )
        
        return await self.repository.add(user_model)
