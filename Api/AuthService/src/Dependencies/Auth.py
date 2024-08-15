import json

from typing import Dict
from typing import Tuple

import uuid
import random

from datetime import datetime

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import Request

from Db.Redis.RedisClient import AuthCache
from Db.Redis.RedisClient import UserCache
from Db.Postgres.Crud.Cruds import getItem
from Db.Postgres.Crud.Cruds import createItem
from Db.Postgres.Base import GetSession

from sqlalchemy.ext.asyncio import AsyncSession

from Shemas.User.CreateUser import CreateUser
from Shemas.User.CreateUser import ConfirmUser as Confirm

class CheckUser:
    def __init__(self) -> None:
        pass

    async def __call__(
            self, User: CreateUser, session: AsyncSession = Depends(GetSession)
    )-> Dict | CreateUser:
        if (data:=await UserCache.getItem(key = User.Email)):
            return data
        if  (data:=await getItem.GetUser(email = User.Email, session = session)):
            return data
        return User

checkUser = CheckUser()


class CreateUser:
    def __init__(self) -> None:
        pass  

    async def __call__(
        self, exists: CheckUser = Depends(checkUser),
    ) -> dict | HTTPException:
        if isinstance(exists, dict):
            raise HTTPException(status_code=401, detail="User already exists")
        Code = int(''.join((random.sample('123456789', 6))))
        result: Dict = exists.model_dump()
        result.update(
            dict(
                LastLogin = str(datetime.now()),
                UserUUID = str(uuid.uuid4())
            )
        )
        await AuthCache.CreateItem(
            key = exists.Email, value = dict(
                code = Code,
                data = result
            )
        )
        return dict(Code = Code)
    
createUser = CreateUser()


class ConfirmUser:
    def __init__(self) -> None:
        self.WrongCodes: Dict[Tuple[str, str] : int] = {}

    async def __call__(
        self, request: Request, User: Confirm,
        session: AsyncSession = Depends(GetSession)
    )->Dict | HTTPException:
        UserIp = request.client.host
        Session: Dict = await AuthCache.getItem(key = User.Email)
        
        if not Session:
            raise HTTPException(status_code = 400, detail = 'Session not found')
        if Session['code'] == User.ConfirmationCode:
            await createItem.CreateUser(User = Session['data'], session = session)
            await UserCache.CreateItem(key = User.Email, value = Session)
            await AuthCache.DeleteItem(key = User.Email)
            if (User.Email, UserIp) in self.WrongCodes:
                del self.WrongCodes[(User.Email, UserIp)]
            return dict(
                message = 'User created Successful',
                data = Session
            )
        else:
            if not (User.Email, UserIp) in self.WrongCodes:
                self.WrongCodes[(User.Email, UserIp)] = 1

            if self.WrongCodes[(User.Email, UserIp)] == 2 or 1:
                self.WrongCodes[(User.Email, UserIp)] += 1

            if self.WrongCodes[(User.Email, UserIp)] == 3:
                await AuthCache.DeleteItem(key = User.Email)
                del self.WrongCodes[(User.Email, UserIp)]
                raise HTTPException(
                    status_code = 429,
                    detail = 'try register again'
                )
           
confirmUser = ConfirmUser()


class LoginUser:
    def __init__(self) -> None:
        pass

    async def __call__(
        exists: Depends
    )-> Dict | HTTPException:
        return ...