from exceptions import NotCorrectPassword, UserAlreadyExists, UserNotFound
from models import UserModel
from repositories import UserRepository
from schemas import LikesInfo, LikesType, UserRegisterData

from .base import BaseService


class UserService(BaseService[UserRepository, UserModel]):
    repo = UserRepository

    def _get_user_or_raise(self, user: UserModel | None) -> UserModel:
        if not user:
            raise UserNotFound()
        return user

    async def get_user_by_id(self, user_id: int) -> UserModel:
        return self._get_user_or_raise(await self.repository.get(user_id))

    async def get_user_by_username(self, username: str) -> UserModel:
        return self._get_user_or_raise(await self.repository.get_by(username=username))

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

    async def check_exists(self, username: str) -> bool:
        """Checks if user exists.

        The self.get_user_by_username returns UserModel or raise UserNotFound
        so if it raise the exception, user don't exists.

        Also, user counts as exists if the given username is the same as the username of the user reduced to lowercase

        Returns:
            bool: True if user exists
        """
        try:
            user = await self.get_user_by_username(username)
            return user.username.lower() == username.lower()
        except UserNotFound:
            return False

    async def add_user(self, data: UserRegisterData) -> UserModel:
        try:
            await self.get_user_by_username(data.username)
        except UserNotFound:
            user_model = UserModel(
                username=data.username,
                email=data.email,
                password=data.password,
                banner=data.banner.read() if data.banner else None,
                avatar=data.avatar.read() if data.avatar else None,
            )

            return await self.repository.add(user_model)
        else:
            raise UserAlreadyExists()
