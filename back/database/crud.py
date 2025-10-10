from sqlalchemy import select, exists, update
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import *
from .core import *


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
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user.id

    async def get_user(self, session: AsyncSession, user: UserModel) -> UserModel | None:
        userDB = await session.scalar(
            select(UserModel)
            .where(UserModel.username == user.username)
            .options(
                joinedload(UserModel.stacks),
                joinedload(UserModel.social_links),
                selectinload(UserModel.posts).joinedload(PostModel.comments),
                selectinload(UserModel.comments).joinedload(CommentModel.author),
                selectinload(UserModel.liked_by_users_relations).joinedload(LikedUser.user),
                selectinload(UserModel.liked_users_relations).joinedload(LikedUser.liked_user),
                selectinload(UserModel.liked_posts_relations).joinedload(LikedPost.post),
            )
        )
        if not userDB:
            return None
        return userDB

    async def update_user(self, session: AsyncSession, user_id: int, **fields):
        if not fields:
            return

        stmt = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(**fields)
            .execution_options(synchronize_session='fetch')
        )

        await session.execute(stmt)
        await session.commit()

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
                    exists(
                        select(LikedPost)
                        .where(LikedPost.post_id == PostModel.id)
                        .where(LikedPost.user_id == user_id)
                    ).label('is_liked'),
                )
                .order_by(PostModel.created_at.desc())
                .options(
                    joinedload(PostModel.author),
                    selectinload(PostModel.comments),
                    selectinload(PostModel.likes_relations).joinedload(LikedPost.user),
                )
            )
        ).all()

    async def get_post(self, session: AsyncSession, post_id: int) -> PostModel | None:
        return await session.scalar(
            select(PostModel)
            .where(PostModel.id == post_id)
            .options(
                joinedload(PostModel.author),
                selectinload(PostModel.comments),
                selectinload(PostModel.likes_relations).joinedload(LikedPost.user),
            )
        )

    # Comment
    async def add_comment(self, session: AsyncSession, comment: CommentModel) -> int:
        session.add(comment)
        await session.commit()
        await session.refresh(comment)
        return comment.id

    async def get_comments(self, session: AsyncSession) -> list[CommentModel]:
        return (
            await session.scalars(select(CommentModel).order_by(CommentModel.created_at.desc()))
        ).all()

    async def get_comment(self, session: AsyncSession, comment_id: int) -> CommentModel | None:
        return await session.scalar(select(CommentModel).where(CommentModel.id == comment_id))
