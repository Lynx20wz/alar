from repository import CommentRepository

from .base import BaseService


class CommentService(BaseService[CommentRepository]):
    repo = CommentRepository
