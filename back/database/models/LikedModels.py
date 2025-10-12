# pyright: reportUndefinedVariable=false

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core import Base


class LikedUser(Base):
    __tablename__ = 'user_likes'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    liked_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

    user: Mapped['UserModel'] = relationship(
        foreign_keys=[user_id], back_populates='liked_users_relations'
    )
    liked_user: Mapped['UserModel'] = relationship(
        foreign_keys=[liked_user_id], back_populates='liked_by_users_relations'
    )


class LikedPost(Base):
    __tablename__ = 'post_likes'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), primary_key=True)

    user: Mapped['UserModel'] = relationship(
        back_populates='liked_posts_relations', foreign_keys=[user_id], lazy='joined'
    )
    post: Mapped['PostModel'] = relationship(
        back_populates='likes_relations', foreign_keys=[post_id], lazy='joined'
    )
