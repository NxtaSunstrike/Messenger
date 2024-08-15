from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from Db.Postgres.Base import Base

if TYPE_CHECKING:
    from Db.Postgres.Models.UserModel import User


class UserAvatars(Base):
    
    __tablename__ = 'user_avatars'

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    UserUUID: Mapped[str] = mapped_column(ForeignKey('users.UserUUID'))
    PhotoUUID: Mapped[str] = mapped_column(String, unique = True)
    PhotoPath: Mapped[str] = mapped_column(String, nullable = False)

    User: Mapped['User'] = relationship(
        'User',
        back_populates = 'Avatars', lazy = 'joined',
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}