from sqlalchemy import select, exists
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt

from .models import *
from .core import *
from exceptions import NotCorrectPassword, UserNotFound


class DataBaseCrud:
    instance_ = None

    def __new__(cls):
        if cls.instance_ is None:
            cls.instance_ = super().__new__(cls)
        return cls.instance_

    def __init__(self, engine=engine):
        self.engine = engine
        self.session_maker = sm

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # user
    async def add_user(self, session: AsyncSession, user: UserModel) -> int:
        user.password = bcrypt.hash(user.password)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user.id

    async def get_user(
        self, session: AsyncSession, user: UserModel, check_password: bool = False
    ) -> UserModel | None:
        userDB = await session.scalar(
            select(UserModel)
            .where(UserModel.username == user.username)
            .options(
                joinedload(UserModel.social_links),
                selectinload(UserModel.posts).joinedload(PostModel.comments),
                selectinload(UserModel.comments).joinedload(CommentModel.author),
                selectinload(UserModel.liked_by_users_relations).joinedload(LikedUser.user),
                selectinload(UserModel.liked_users_relations).joinedload(LikedUser.liked_user),
                selectinload(UserModel.liked_posts_relations).joinedload(LikedPost.post),
            )
        )
        if not userDB:
            raise UserNotFound()
        elif check_password and not bcrypt.verify(user.password, userDB.password):
            raise NotCorrectPassword()
        return userDB

    async def get_user_by_id(self, session: AsyncSession, userid: int) -> UserModel | None:
        return await session.get(UserModel, userid)

    # Likes
    async def add_like(self, session: AsyncSession, like: LikedPost | LikedUser):
        session.add(like)
        await session.commit()

    async def remove_like(self, session: AsyncSession, like: LikedPost | LikedUser):
        session.delete(like)
        await session.commit()

    # Post
    async def add_post(self, session: AsyncSession, post: PostModel):
        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post.id

    async def get_posts(self, session: AsyncSession, user_id: int) -> list[PostModel]:
        return (
            await session.scalars(
                select(
                    PostModel,
                    exists()
                    .where(LikedPost.post_id == PostModel.id)
                    .where(LikedPost.user_id == user_id)
                    .label('is_liked'),
                )
                .order_by(PostModel.created_at.desc())
                .options(
                    joinedload(PostModel.author),
                    selectinload(PostModel.comments),
                    selectinload(PostModel.likes_relations).joinedload(LikedPost.user),
                )
            )
        ).all()

    async def get_post(self, session: AsyncSession, post_id: int, user_id: int) -> PostModel | None:
        return await session.scalar(
            select(
                PostModel,
                exists()
                .where(LikedPost.post_id == PostModel.id)
                .where(LikedPost.user_id == user_id)
                .label('is_liked'),
            )
            .where(PostModel.id == post_id)
            .options(
                joinedload(PostModel.author),
                selectinload(PostModel.comments),
                selectinload(PostModel.likes_relations).joinedload(LikedPost.user),
            )
        )
