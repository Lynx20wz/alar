from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from ..core import Base
from passlib.hash import bcrypt

from schemas import LikesInfo, LikesType


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)

    # EXTRA
    email: Mapped[str] = mapped_column(unique=True)
    _password: Mapped[str] = mapped_column('password')
    banner: Mapped[Optional[bytes]]
    avatar: Mapped[Optional[bytes]]
    bio: Mapped[Optional[str]] = mapped_column(String(100))

    posts: Mapped[list['PostModel']] = relationship(back_populates='author')
    comments: Mapped[list['CommentModel']] = relationship(back_populates='author')
    social_links: Mapped[list['SocialLinkModel']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    stacks: Mapped[list['StackModel']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    liked_users_relations: Mapped[list['LikedUser']] = relationship(
        back_populates='user', foreign_keys='LikedUser.user_id'
    )
    liked_by_users_relations: Mapped[list['LikedUser']] = relationship(
        back_populates='liked_user', foreign_keys='LikedUser.liked_user_id'
    )
    liked_posts_relations: Mapped[list['LikedPost']] = relationship(
        back_populates='user', foreign_keys='LikedPost.user_id'
    )

    @validates('username')
    def convert_lower(self, key, value):
        return value.lower()

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password: str):
        self._password = bcrypt.hash(password)

    def check_password(self, plain_password: str) -> bool:
        return bcrypt.verify(plain_password, self._password)

    @property
    def follows(self):
        return LikesInfo(
            type=LikesType.users,
            total=len(self.liked_users_relations),
            objects=[relation.liked_user for relation in self.liked_users_relations],
        )

    @property
    def followers(self):
        return LikesInfo(
            type=LikesType.users,
            total=len(self.liked_by_users_relations),
            objects=[relation.user for relation in self.liked_by_users_relations],
        )

    @property
    def liked_posts(self):
        return LikesInfo(
            type=LikesType.posts,
            total=len(self.liked_posts_relations),
            objects=[relation.post for relation in self.liked_posts_relations],
        )
