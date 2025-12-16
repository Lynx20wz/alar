# pyright: reportUndefinedVariable=false

from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class StackModel(Base):
    __tablename__ = 'stacks'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    title: Mapped[str] = mapped_column(String(30))
    icon: Mapped[Optional[bytes]]
    url: Mapped[str]

    user: Mapped['UserModel'] = relationship(back_populates='stacks')
