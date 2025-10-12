# pyright: reportUndefinedVariable=false

from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core import Base

from schemas import LikesInfo, LikesType


class PostModel(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(unique=True)
    content: Mapped[str]
    image: Mapped[Optional[bytes]]
    views: Mapped[int] = mapped_column(server_default='0')
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    _is_liked: bool = False
    
    @property
    def is_liked(self) -> bool:
        return self._is_liked
    
    @is_liked.setter
    def is_liked(self, value: bool):
        self._is_liked = value

    def is_liked_by(self, user_id: int) -> bool:
        self._is_liked = any(relation.user_id == user_id for relation in self.likes_relations)
        return self._is_liked

    author: Mapped['UserModel'] = relationship(back_populates='posts', lazy='joined')
    comments: Mapped[list['CommentModel']] = relationship(back_populates='post', lazy='joined')
    likes_relations: Mapped[list['LikedPost']] = relationship(back_populates='post', lazy='joined')

    @property
    def likes(self):
        return LikesInfo(
            type=LikesType.users,
            total=len(self.likes_relations),
            objects=[relation.user for relation in self.likes_relations],
        )
        
    @property
    def hasImage(self) -> bool:
        return bool(self.image)
