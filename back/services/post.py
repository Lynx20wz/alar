from exceptions import PostNotFound
from models import LikePostModel, PostModel
from repositories import PostRepository

from .base import BaseService


class PostService(BaseService[PostRepository, PostModel]):
    repo = PostRepository

    def _get_post_or_raise(self, post: PostModel | None) -> PostModel:
        if not post:
            raise PostNotFound()
        return post

    async def get_post(self, post_id: int, user_id: int = 0) -> PostModel:
        post = self._get_post_or_raise(await self.repository.get(post_id))

        if user_id:
            post.is_liked = await self.is_liked_by(post, user_id)

        return post

    async def get_posts(self, offset: int = 0) -> list[PostModel]:
        return await self.repository.get_all(offset)

    async def change_like_status(self, post_id: int, user_id: int) -> bool:
        """Adds or removes a like from this user, depending on the current status.

        Args:
            post_id (int): id of the post whose status needs to be changed
            user_id (int): id of the user who is changing the status

        Returns:
            bool: the new status
        """
        post = self._get_post_or_raise(await self.get_post(post_id))

        like = LikePostModel(post_id=post_id, user_id=user_id)

        if post.is_liked:
            await self.repository.delete_like(like)
        else:
            await self.repository.add_like(like)

        post.is_liked = not post.is_liked
        return post.is_liked

    async def is_liked_by(self, post: PostModel, user_id: int) -> bool:
        return any(relation.user_id == user_id for relation in post.likes_relations)
