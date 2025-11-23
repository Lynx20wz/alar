from sqlalchemy import delete, select

from models import LikeModel, LikePostModel, LikeUserModel

from .base import BaseRepository


class LikeRepository(BaseRepository[LikeModel]):
    async def delete(self, obj: LikeModel):
        if isinstance(obj, LikePostModel):
            likeDB = await self.session.scalar(
                select(LikePostModel).where(
                    LikePostModel.user_id == obj.user_id, LikePostModel.post_id == obj.post_id
                )
            )
        elif isinstance(obj, LikeUserModel):
            likeDB = await self.session.scalar(
                select(LikeUserModel).where(
                    LikeUserModel.user_id == obj.user_id,
                    LikeUserModel.like_user_id == obj.like_user_id,
                )
            )
        else:
            return
        await self.session.delete(likeDB)
        await self.session.commit()
