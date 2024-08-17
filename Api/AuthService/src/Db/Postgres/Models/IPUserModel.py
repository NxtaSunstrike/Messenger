from typing import TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Db.Postgres.Base import Base

if TYPE_CHECKING:
    from Db.Postgres.Models.UserModel import User

class UserIP(Base):

    __tablename__ = 'users_ip'

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    UserUUID: Mapped[str] = mapped_column(ForeignKey('users.UserUUID'))
    UserIP: Mapped[str] = mapped_column(String)

    User: Mapped['User'] = relationship(
        'User',
        back_populates='IP', lazy='joined'
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}