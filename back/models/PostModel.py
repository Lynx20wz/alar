# pyright: reportUndefinedVariable=false

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func, sql
from sqlalchemy.orm import Mapped, mapped_column, query_expression, relationship

from db import Base


class PostModel(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column()
    image: Mapped[bytes | None] = mapped_column()
    views: Mapped[int] = mapped_column(server_default='0')
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())

    author: Mapped['UserModel'] = relationship(back_populates='posts')
    comments: Mapped[list['CommentModel']] = relationship(back_populates='post', lazy='selectin')
    likes_relations: Mapped[list['LikePostModel']] = relationship(
        back_populates='post', lazy='selectin'
    )

    is_liked: Mapped[bool] = query_expression(default_expr=sql.false())

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
