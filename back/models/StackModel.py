# pyright: reportUndefinedVariable=false

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class StackModel(Base):
    __tablename__ = 'stacks'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    title: Mapped[str] = mapped_column(String(30))
    icon: Mapped[bytes | None] = mapped_column()
    url: Mapped[str] = mapped_column()

    user: Mapped['UserModel'] = relationship(back_populates='stacks')
