from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from models import CommentModel, LikePostModel, LikeUserModel, PostModel, UserModel

from .base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    model = UserModel
    options = [
        selectinload(UserModel.stacks),
        selectinload(UserModel.social_links),
        selectinload(UserModel.posts).joinedload(PostModel.comments),
        selectinload(UserModel.comments).joinedload(CommentModel.author),
        selectinload(UserModel.like_by_users_relations).joinedload(LikeUserModel.user),
        selectinload(UserModel.like_users_relations).joinedload(LikeUserModel.like_user),
        selectinload(UserModel.like_posts_relations).joinedload(LikePostModel.post),
    ]

    async def get(self, id: int) -> Optional[UserModel]:
        return await self.session.scalar(
            select(UserModel).where(UserModel.id == id).options(*self.options)
        )

    async def get_by(self, **kwargs) -> Optional[UserModel]:
        filters = [getattr(self.model, key) == value for key, value in kwargs.items()]

        if filters:
            return await self.session.scalar(
                select(self.model).where(*filters).options(*self.options)
            )
