from exceptions import PostNotFound
from models import PostModel
from repository import PostRepository

from .base import BaseService


class PostService(BaseService[PostRepository]):
    repo = PostRepository

    async def get_post(self, post_id: int, user_id: int = 0) -> PostModel:
        post = await self.repository.get(post_id)
        if not post:
            raise PostNotFound()

        if user_id:
            post.is_liked = await self.is_liked_by(post, user_id)

        return post

    async def get_posts(self, offset: int = 0) -> list[PostModel]:
        return await self.repository.get_all(offset)

    async def is_liked_by(self, post: PostModel, user_id: int) -> bool:
        return any(relation.user_id == user_id for relation in post.likes_relations)
