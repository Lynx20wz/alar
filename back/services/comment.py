from sqlalchemy.ext.asyncio import AsyncSession

from exceptions import CommentNotFound, PostNotFound
from models import CommentModel
from repositories import CommentRepository

from .base import BaseService
from .post import PostService


class CommentService(BaseService[CommentRepository, CommentModel]):
    repo = CommentRepository

    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.post_service: PostService = PostService(session)

    async def get_comment(self, comment_id: int) -> CommentModel | None:
        return await self.repository.get(comment_id)

    async def add_comment(self, comment: CommentModel) -> CommentModel:
        post = await self.post_service.get_post(comment.post_id)  # check if post exists

        if not post:
            raise PostNotFound(object_id=comment.post_id)

        return await self.repository.add(comment)
