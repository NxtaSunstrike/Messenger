from typing import Dict

from sqlalchemy import select, delete, update, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from Db.Postgres.Models.UserModel import User as UserModel
from Db.Postgres.Models.IPUserModel import UserIP

from Shemas.User.CreateUser import CreateUser as UserInfo


class UserRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.sessionFactory = session


    async def CreateUser(self, User: Dict)->Dict:
        async with self.sessionFactory() as session:
            await session.execute(insert(UserModel).values(User))
            await session.commit()
            return dict(
                status_code = 200,
                message = dict(message = "User created successfully"),
                content = dict(data = User)
            )
    

    async def DeleteUser(self, UUID: str)->Dict:
        async with self.sessionFactory() as session:
            await session.execute(delete(UserModel).where(UserModel.UserUUID == UUID))
            await session.commit()
            return dict(
                status_code = 200,
                message = dict(message =  "User deleted successfully"),
                content = dict(data = UUID)
            )
    

    async def GetUser(self, UUID: str)-> Dict:
        async with self.sessionFactory() as session:
        
            query = await session.execute(select(UserModel).where(UserModel.UserUUID == UUID)
                        .options(selectinload(UserModel.IP))
                        .options(selectinload(UserModel.UserAgents))
                        .options(selectinload(UserModel.Avatars))
                        )  
            result = query.scalars().first()
            if result:
                data = dict(
                    User = result.as_dict(),
                    UserIp = [ip.as_dict() for ip in result.IP],
                    UserAgent = [UserAgent.as_dict() for UserAgent in result.UserAgents],
                    UserAvatar = [Avatars.as_dict() for Avatars in result.UserAgents]
                )
                return data
            return dict()
    

    async def CheckUser(self, email: str)-> Dict:
        async with self.sessionFactory() as session:
            query = await session.execute(select(UserModel).where(UserModel.Email == email))
            result = query.scalars().first()
            if result:
                return dict(User = result.as_dict())
            return dict()


    async def AddIp(self, UUID: str, Ip: str)-> Dict:
        async with self.sessionFactory() as session:
            await session.execute(insert(UserIP).values(UserUUID = UUID, UserIP = Ip))
            await session.commit()
            return dict(
                status_code = 200,
                message = dict(message = "Ip added successfully"),
                content = dict(data = Ip)
            )
