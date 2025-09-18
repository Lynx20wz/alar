from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core import Base


class CommentModel(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    content: Mapped[str]
    
    author: Mapped['UserModel'] = relationship(back_populates='comments')
    post: Mapped['PostModel'] = relationship(back_populates='comments')