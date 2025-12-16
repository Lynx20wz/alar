# pyright: reportUndefinedVariable=false

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class SocialLinkModel(Base):
    __tablename__ = 'social_links'
    __table_args__ = (UniqueConstraint('user_id', 'platform', name='uq_user_platform'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    platform: Mapped[str] = mapped_column(String(30))
    url: Mapped[str] = mapped_column(String(255))

    user: Mapped['UserModel'] = relationship(back_populates='social_links')
