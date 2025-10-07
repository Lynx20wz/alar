from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from ..core import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    banner: Mapped[Optional[bytes]]
    avatar: Mapped[Optional[bytes]]

    posts: Mapped[list['PostModel']] = relationship(back_populates='author')
    comments: Mapped[list['CommentModel']] = relationship(back_populates='author')
    social_links: Mapped[list['SocialLink']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )
    liked_users_relations: Mapped[list['LikedUser']] = relationship(
        back_populates='user', foreign_keys='LikedUser.user_id'
    )

    liked_by_users_relations: Mapped[list['LikedUser']] = relationship(
        back_populates='liked_user', foreign_keys='LikedUser.liked_user_id', lazy='selectin'
    )

    liked_posts_relations: Mapped[list['LikedPost']] = relationship(
        back_populates='user', foreign_keys='LikedPost.user_id'
    )

    @property
    def follows(self):
        return [relation.liked_user for relation in self.liked_users_relations]

    @property
    def followers(self):
        return [relation.user for relation in self.liked_by_users_relations]

    @property
    def liked_posts(self):        
        return [relation.post for relation in self.liked_posts_relations]

    @validates('username')
    def convert_lower(self, key, value):
        return value.lower()
