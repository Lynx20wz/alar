from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
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