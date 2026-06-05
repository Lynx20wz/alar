from passlib.hash import sha256_crypt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)

    # EXTRA
    email: Mapped[str] = mapped_column(unique=True)
    _password: Mapped[str] = mapped_column('password')
    banner: Mapped[bytes] = mapped_column()
    avatar: Mapped[bytes] = mapped_column()
    bio: Mapped[str | None] = mapped_column(String(100))

    posts: Mapped[list['PostModel']] = relationship(back_populates='author')
    comments: Mapped[list['CommentModel']] = relationship(back_populates='author')
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

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password: str):
        self._password = sha256_crypt.hash(password)

    def check_password(self, plain_password: str) -> bool:
        return sha256_crypt.verify(plain_password, self._password)
