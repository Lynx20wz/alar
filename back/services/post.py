from repository import PostRepository

from .base import BaseService


class PostService(BaseService[PostRepository]):
    repo = PostRepository
