import json

from typing import Dict

from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy import select, delete, update, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from Db.Postgres.Base import GetSession
from Db.Postgres.Models.UserModel import User as UserModel

from Shemas.User.CreateUser import CreateUser as UserInfo


class CreateItem:

    @staticmethod
    async def CreateUser(
        User: Dict,
        session: AsyncSession = Depends(GetSession)
    )->JSONResponse:
        await session.execute(insert(UserModel).values(User))
        await session.commit()
        return dict(
            status_code = 200,
            message = dict(message = "User created successfully"),
            content = dict(data = User)
        )
    
createItem = CreateItem()
    

class DeleteItem:

    @staticmethod
    async def DeletUser(
        UUID: str,
        session: AsyncSession = Depends(GetSession)
    )->JSONResponse:
        await session.execute(delete(UserModel).where(UserModel.UserUUID == UUID))
        await session.commit()
        return JSONResponse(
            status_code = 200,
            message = dict(message =  "User deleted successfully"),
            content = dict(data = UUID)
        )
    

class GetItem:

    @staticmethod
    async def GetUser(
        UUID: str | None = None, email: str | None = None,
        session: AsyncSession = Depends(GetSession)
    )-> Dict:
        if email:
            query = await session.execute(select(UserModel).where(UserModel.Email == email)
                        .options(selectinload(UserModel.IP))
                        .options(selectinload(UserModel.UserAgents))
                        .options(selectinload(UserModel.Avatars))
                        )
        elif UUID:
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
    
        

getItem = GetItem()

