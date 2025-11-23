from exceptions import CommentNotFound
from models import CommentModel
from repository import CommentRepository

from .base import BaseService


class CommentService(BaseService[CommentRepository]):
    repo = CommentRepository

    async def get_comment(self, comment_id: int) -> CommentModel:
        comment = await self.repository.get(comment_id)

        if not comment:
            raise CommentNotFound()

        return comment
