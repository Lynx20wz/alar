# pyright: reportUndefinedVariable=false

from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core import Base


class CommentModel(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    author: Mapped['UserModel'] = relationship(back_populates='comments', lazy='selectin')
    post: Mapped['PostModel'] = relationship(back_populates='comments', lazy='selectin')
