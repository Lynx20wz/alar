from exceptions import PostNotFound
from models import PostModel
from models.LikeModels import LikePostModel
from repositories import PostRepository

from .base import BaseService


class PostService(BaseService[PostRepository, PostModel]):
    repo = PostRepository

    async def get_post(self, post_id: int, user_id: int | None = None) -> PostModel | None:
        return await self.repository.get(post_id, user_id)

    async def get_posts(self, offset: int = 0, user_id: int | None = None) -> list[PostModel]:
        return await self.repository.get_all(offset, user_id)

    async def change_like_status(self, post_id: int, user_id: int) -> bool:
        """Adds or removes a like from this user, depending on the current status.

        Args:
            post_id (int): id of the post whose status needs to be changed
            user_id (int): id of the user who is changing the status

        Returns:
            bool: the new status
        """
        post = await self.get_post(post_id)

        if not post:
            raise PostNotFound(object_id=post_id)

        like = LikePostModel(post_id=post_id, user_id=user_id)

        if post.is_liked:
            await self.repository.delete_like(like)
        else:
            await self.repository.add_like(like)

        post.is_liked = not post.is_liked
        return post.is_liked
