from typing import Optional

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from models import LikePostModel, PostModel

from .base import BaseRepository


class PostRepository(BaseRepository[PostModel]):
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

    async def get_all(self, session: AsyncSession, user_id: int) -> list[PostModel]:
        result = (
            await session.execute(
                select(
                    PostModel,
                    exists(
                        select(LikePostModel)
                        .where(LikePostModel.post_id == PostModel.id)
                        .where(LikePostModel.user_id == user_id)
                    ).label('is_liked'),
                )
                .order_by(PostModel.created_at.desc())
                .options(
                    joinedload(PostModel.author),
                    selectinload(PostModel.comments),
                    selectinload(PostModel.likes_relations).joinedload(LikePostModel.user),
                )
            )
        ).all()

        posts = []
        for post, is_liked in result:
            post.is_liked = is_liked
            posts.append(post)
        return posts
