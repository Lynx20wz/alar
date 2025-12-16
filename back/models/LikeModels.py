# pyright: reportUndefinedVariable=false

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class LikeModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


class LikeUserModel(LikeModel):
    __tablename__ = 'user_likes'

    like_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['UserModel'] = relationship(
        foreign_keys='LikeUserModel.user_id',
        back_populates='like_users_relations',
    )
    like_user: Mapped['UserModel'] = relationship(
        foreign_keys=like_user_id,
        back_populates='like_by_users_relations',
    )


class LikePostModel(LikeModel):
    __tablename__ = 'post_likes'

    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))

    user: Mapped['UserModel'] = relationship(
        foreign_keys='LikePostModel.user_id',
        back_populates='like_posts_relations',
    )
    post: Mapped['PostModel'] = relationship(
        foreign_keys=post_id,
        back_populates='likes_relations',
    )
