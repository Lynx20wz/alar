from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..core import Base


class PostModel(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column()
    content: Mapped[str]
    views: Mapped[int]
    likes: Mapped[int]
    
    author: Mapped['UserModel'] = relationship(back_populates='posts')
    comments: Mapped[list['CommentModel']] = relationship(back_populates='post')