from models import CommentModel

from .base import BaseRepository


class CommentRepository(BaseRepository[CommentModel]):
    model = CommentModel
