from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core import Base

from schemas import LikesInfo


class PostModel(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str]
    content: Mapped[str]
    views: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    author: Mapped['UserModel'] = relationship(back_populates='posts', lazy='joined')
    comments: Mapped[list['CommentModel']] = relationship(back_populates='post', lazy='subquery')

    likes_relations: Mapped[list['LikedPost']] = relationship(back_populates='post', lazy='joined')

    @property
    def likes(self):
        return LikesInfo(total=len(self.likes_relations), users=[relation.user for relation in self.likes_relations])
