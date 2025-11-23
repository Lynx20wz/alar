from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from models import LikePostModel, PostModel

from .base import BaseRepository


class PostRepository(BaseRepository[PostModel]):
    model = PostModel

    async def get(self, id: int) -> Optional[PostModel]:
        return await self.session.scalar(
            select(PostModel)
            .where(PostModel.id == id)
            .options(
                joinedload(PostModel.author),
                selectinload(PostModel.comments),
                selectinload(PostModel.likes_relations).joinedload(LikePostModel.user),
            )
        )

    async def get_all_for_user(self, user_id: int) -> list[PostModel]:
        return list(
            await self.session.scalars(
                select(PostModel)
                .where(PostModel.author_id == user_id)
                .order_by(PostModel.created_at.desc())
                .options(
                    joinedload(PostModel.author),
                    selectinload(PostModel.comments),
                    selectinload(PostModel.likes_relations).joinedload(LikePostModel.user),
                )
            )
        )
