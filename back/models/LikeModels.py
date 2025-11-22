# pyright: reportUndefinedVariable=false

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from db import Base


class LikeModel(Base):
    __abstract__ = True

    user_id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def user(cls) -> Mapped['UserModel']:
        return relationship(foreign_keys=[cls.user_id], back_populates='liked_users_relations')


class LikeUserModel(LikeModel):
    __tablename__ = 'user_likes'

    liked_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)

    liked_user: Mapped['UserModel'] = relationship(
        foreign_keys=[liked_user_id], back_populates='liked_by_users_relations'
    )


class LikePostModel(LikeModel):
    __tablename__ = 'post_likes'

    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), primary_key=True)

    post: Mapped['PostModel'] = relationship(
        back_populates='likes_relations', foreign_keys=[post_id], lazy='joined'
    )
