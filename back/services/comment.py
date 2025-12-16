from exceptions import CommentNotFound
from models import CommentModel
from repository import CommentRepository
from sqlalchemy.ext.asyncio import AsyncSession

from .post import PostService
from .base import BaseService


class CommentService(BaseService[CommentRepository]):
    repo = CommentRepository

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.post_service = PostService(session)

    def _get_comment_or_raise(self, comment: CommentModel | None) -> CommentModel:
        if not comment:
            raise CommentNotFound()

        return comment

    async def get_comment(self, comment_id: int) -> CommentModel:
        return self._get_comment_or_raise(await self.repository.get(comment_id))

    async def add_comment(self, comment: CommentModel) -> CommentModel:
        await self.post_service.get_post(comment.post_id)  # check if post exists
        return self._get_comment_or_raise(await self.repository.add(comment))
