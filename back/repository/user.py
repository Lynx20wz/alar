from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from models import CommentModel, LikePostModel, LikeUserModel, PostModel, UserModel

from .base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    model = UserModel
    async def get(self, id: int) -> Optional[UserModel]:
        userDB = await self.session.scalar(
            select(UserModel)
            .where(UserModel.id == id)
            .options(
                joinedload(UserModel.stacks),
                joinedload(UserModel.social_links),
                selectinload(UserModel.posts).joinedload(PostModel.comments),
                selectinload(UserModel.comments).joinedload(CommentModel.author),
                selectinload(UserModel.liked_by_users_relations).joinedload(LikeUserModel.user),
                selectinload(UserModel.liked_users_relations).joinedload(LikeUserModel.liked_user),
                selectinload(UserModel.liked_posts_relations).joinedload(LikePostModel.post),
            )
        )
        if userDB:
            return userDB
