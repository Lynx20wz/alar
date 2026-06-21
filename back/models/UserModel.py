# pyright: reportUndefinedVariable=false

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)

    # EXTRA
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column('password', String(255))
    banner: Mapped[bytes] = mapped_column()
    avatar: Mapped[bytes] = mapped_column()
    bio: Mapped[str | None] = mapped_column(String(500))

    posts: Mapped[list['PostModel']] = relationship(back_populates='author', lazy='selectin')
    comments: Mapped[list['CommentModel']] = relationship(back_populates='author', lazy='selectin')
    social_links: Mapped[list['SocialLinkModel']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    stacks: Mapped[list['StackModel']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    like_users_relations: Mapped[list['LikeUserModel']] = relationship(
        back_populates='user', foreign_keys='LikeUserModel.user_id'
    )  # who was liked by this user
    like_by_users_relations: Mapped[list['LikeUserModel']] = relationship(
        back_populates='like_user', foreign_keys='LikeUserModel.like_user_id'
    )  # who liked this user
    like_posts_relations: Mapped[list['LikePostModel']] = relationship(
        back_populates='user', foreign_keys='LikePostModel.user_id'
    )  # what posts were liked by this user
