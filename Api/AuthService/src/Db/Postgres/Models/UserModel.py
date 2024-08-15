from typing import TYPE_CHECKING
from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, BINARY
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from Db.Postgres.Base import Base

if TYPE_CHECKING:
    from Db.Postgres.Models.IPUserModel import UserIP
    from Db.Postgres.Models.UserAvatars import UserAvatars
    from Db.Postgres.Models.UserAgents import UserAgents


class User(Base):

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    LastLogin: Mapped[str] = mapped_column(String, nullable = False)
    Password: Mapped[str] = mapped_column(String, nullable = False)
    Email: Mapped[str] = mapped_column(String, unique = True, nullable = False)
    Name: Mapped[str] = mapped_column(String, nullable = False)
    LastName: Mapped[str] = mapped_column(String, nullable = False)
    City: Mapped[str] = mapped_column(String, default = None, nullable = True)
    Birthday: Mapped[str] = mapped_column(String, default = None, nullable = True)
    Description: Mapped[str] = mapped_column(String, default = None, nullable = True)
    UserName: Mapped[str] = mapped_column(String, nullable = False)
    UserUUID: Mapped[str] = mapped_column(String, nullable = False, unique = True)


    IP: Mapped[List['UserIP']] = relationship(
        'UserIP',
        back_populates = 'User', lazy = 'joined',
    )
    
    Avatars: Mapped[List['UserAvatars']] = relationship(
        'UserAvatars',
        back_populates = 'User', lazy = 'joined'
    )

    UserAgents: Mapped[List['UserAgents']] = relationship(
        'UserAgents',
        back_populates = 'User', lazy = 'joined'
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}