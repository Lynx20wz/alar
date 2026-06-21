from typing import override

from sqlalchemy import delete, exists, select
from sqlalchemy.orm import with_expression

from models import LikePostModel, PostModel

from .base import BaseRepository


class PostRepository(BaseRepository[PostModel]):
    model: type[PostModel] = PostModel

    def _with_is_liked(self, query, user_id: int | None):
        if user_id is None:
            return query

        is_liked_expr = exists().where(
            LikePostModel.post_id == PostModel.id,
            LikePostModel.user_id == user_id,
        )
        return query.options(with_expression(PostModel.is_liked, is_liked_expr))

    @override
    async def get(self, id: int, user_id: int | None = None) -> PostModel | None:
        query = select(PostModel).where(PostModel.id == id)
        query = self._with_is_liked(query, user_id)
        return await self.session.scalar(query)

    @override
    async def get_all(self, offset: int, user_id: int | None = None) -> list[PostModel]:
        query = select(PostModel).limit(10).offset(offset)
        query = self._with_is_liked(query, user_id)
        result = await self.session.scalars(query)
        return list(result)

    async def add_like(self, like: LikePostModel):
        self.session.add(like)
        await self.session.commit()

    async def delete_like(self, like: LikePostModel):
        _ = await self.session.execute(
            delete(LikePostModel).where(
                LikePostModel.post_id == like.post_id, LikePostModel.user_id == like.user_id
            )
        )
        await self.session.commit()

    async def get_all_for_user(self, user_id: int) -> list[PostModel]:
        return list(
            await self.session.scalars(
                select(PostModel)
                .where(PostModel.author_id == user_id)
                .order_by(PostModel.created_at.desc())
            )
        )
