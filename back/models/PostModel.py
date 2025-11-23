# pyright: reportUndefinedVariable=false

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from schemas import LikesInfo, LikesType


class PostModel(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(unique=True)
    content: Mapped[str]
    image: Mapped[Optional[bytes]]
    views: Mapped[int] = mapped_column(server_default='0')
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())

    author: Mapped['UserModel'] = relationship(back_populates='posts', lazy='joined')
    comments: Mapped[list['CommentModel']] = relationship(back_populates='post', lazy='joined')
    likes_relations: Mapped[list['LikePostModel']] = relationship(back_populates='post', lazy='joined')
    
    is_liked: bool = False

    @property
    def likes(self):
        return LikesInfo(
            type=LikesType.users,
            total=len(self.likes_relations),
            objects=[relation.user for relation in self.likes_relations],
        )

    @property
    def has_image(self) -> bool:
        return bool(self.image)
