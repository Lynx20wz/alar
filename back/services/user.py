from typing import override

from passlib.hash import sha256_crypt

from exceptions import NotCorrectPassword, UserAlreadyExists, UserNotFound
from models import UserModel
from repositories import UserRepository
from schemas import UserRegisterSchema

from .base import BaseService


class UserService(BaseService[UserRepository, UserModel]):
    repo = UserRepository

    @override
    async def add(self, obj: UserRegisterSchema) -> UserModel:
        user = await self.get_user_by_username(obj.username)

        if user:
            raise UserAlreadyExists(object_id=user.id)

        password_hash = await self.generate_password_hash(obj.password)

        user_model = UserModel(
            username=obj.username,
            email=obj.email,
            password_hash=password_hash,
            banner=await obj.banner.read() if obj.banner else None,
            avatar=await obj.avatar.read() if obj.avatar else None,
        )

        return await self.repository.add(user_model)

    async def get_user_by_id(self, user_id: int) -> UserModel | None:
        return await self.repository.get(user_id)

    async def get_user_by_username(self, username: str) -> UserModel | None:
        return await self.repository.get_by_username(username)

    async def login(self, username: str, password: str) -> UserModel:
        user = await self.get_user_by_username(username)

        if user is None:
            raise UserNotFound(username=username)

        if not await self.check_password(user, password):
            raise NotCorrectPassword()

        return user

    async def generate_password_hash(self, password: str) -> str:
        return sha256_crypt.hash(password)

    async def check_password(self, user: UserModel, password: str) -> bool:
        if sha256_crypt.verify(password, user.password_hash):
            return True

        return False

    async def get_follows(self, user_id: int) -> LikesInfo:
        user = await self.get_user_by_id(user_id)

        if user is None:
            raise UserNotFound(object_id=user_id)

        return LikesInfo(
            type=LikesType.users,
            total=len(user.like_users_relations),
            objects=[relation.liked_user for relation in user.like_users_relations],
        )

    async def get_followers(self, user_id: int) -> LikesInfo:
        user = await self.get_user_by_id(user_id)

        if user is None:
            raise UserNotFound(object_id=user_id)

        return LikesInfo(
            type=LikesType.users,
            total=len(user.like_by_users_relations),
            objects=[relation.user for relation in user.like_by_users_relations],
        )

    async def get_liked_posts(self, user_id: int) -> LikesInfo:
        user = await self.get_user_by_id(user_id)

        if user is None:
            raise UserNotFound(object_id=user_id)

        return LikesInfo(
            type=LikesType.posts,
            total=len(user.like_posts_relations),
            objects=[relation.post for relation in user.like_posts_relations],
        )

    async def check_exists(self, username: str) -> bool:
        return await self.get_user_by_username(username) is not None
