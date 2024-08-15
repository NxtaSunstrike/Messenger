from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy.orm import relationship

from Db.Postgres.Base import Base

if TYPE_CHECKING:
    from Db.Postgres.Models.UserModel import User


class UserAgents(Base):

    __tablename__ = 'user_agents'

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    UserUUID: Mapped[str] = mapped_column(String, ForeignKey('users.UserUUID'), nullable = False)
    UserAgent: Mapped[str] = mapped_column(nullable = False)

    User: Mapped['User'] = relationship(
        'User',
        back_populates = 'UserAgents', lazy = 'joined'
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}