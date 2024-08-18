from typing import Dict
from datetime import datetime
from uuid import uuid4

import os

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi import Request

from random import sample

from Shemas.User.CreateUser import CreateUser as Create
from Shemas.User.CreateUser import ConfirmUser as Confirm
from Shemas.User.CreateUser import Login

from dependency_injector.wiring import inject, Provide

from Di.Containers import PSQLContainer
from Di.Containers import RedisContainer
from Di.Containers import SessionContainer
from Di.Containers import JWTContainer

from Db.Postgres.Crud.Services import UserService
from Db.Redis.RedisClient import Service

from Utils.Jwt import JWTAuth
from datetime import timedelta


router = APIRouter()

@router.post("/CreateUser", response_model=None)
@inject
async def CreateUser(
    User: Create, 
    PSQLService: UserService = Depends(Provide[PSQLContainer.UserSevice]),
    RedisService: Service = Depends(Provide[RedisContainer.Service]),
    AuthSession: Service = Depends(Provide[SessionContainer.AuthSession])
):
    if await RedisService.getUser(key = User.Email):
        raise HTTPException(status_code=401, detail="User already exists")
    elif await PSQLService.CheckUser(email = User.Email):
        raise HTTPException(status_code=401, detail="User already exists")
    ConfirmationCode = int(''.join(sample('123456789', 6)))
    await AuthSession.CreateUser(
        key = User.Email, value = dict(
            Code = ConfirmationCode,
            User = User.model_dump()
        )
    )
    return JSONResponse(
        status_code=200,
        content=dict(
            ConfirmationCode = ConfirmationCode
        )
    )


@router.post("/ConfirmUser", response_model=None)
@inject
async def ConfirmUser(
    User: Confirm, request: Request, response: Response,
    PSQLService: UserService = Depends(Provide[PSQLContainer.UserSevice]),
    RedisService: Service = Depends(Provide[RedisContainer.Service]),
    AuthSession: Service = Depends(Provide[SessionContainer.AuthSession]),
    JWTService: JWTAuth = Depends(Provide[JWTContainer.JWT])
):
    session: Dict = await AuthSession.getUser(key = User.Email)
    if not session:
        raise HTTPException(status_code=401, detail="Session not found")
    
    Date = str(datetime.now())
    UUID = str(uuid4())
    UserIp = str(request.client.host)

    if User.Code != session['Code']:
        raise HTTPException(status_code=401, detail="Invalid confirmation code")
    
    result: Dict = session['User']
    result.update(
        updatedData:= dict(
            LastLogin = Date,
            UserUUID = UUID
        )
    )
    AccessToken = await JWTService.encodeToken(payload=updatedData, type='access')
    RefreshToken = await JWTService.encodeToken(payload=dict(UUID = UUID), type='refresh')
    await AuthSession.DeleteUser(key = User.Email)
    await RedisService.CreateUser(key = User.Email, value = result)
    await PSQLService.CreateUser(User = result)
    await PSQLService.AddIp(UUID = UUID, Ip = UserIp)
    response.set_cookie(
        key='RefreshToken', value=RefreshToken, httponly=False, expires = 60*60*24*30
    )
    return JSONResponse(
        status_code=200,
        content=dict(
            User = result,
            AccessToken = AccessToken
        )
    )


@router.post("/Login", response_model=None)
@inject
async def Login(
    UserModel: Login, response: Response,
    JWTService: JWTAuth = Depends(Provide[JWTContainer.JWT]),
    PSQLService: UserService = Depends(Provide[PSQLContainer.UserSevice]),
    RedisService: Service = Depends(Provide[RedisContainer.Service])
):
    User = await RedisService.getUser(key = UserModel.Email)
    if not User:
        raise HTTPException(status_code=401, detail="User not found")
    
    User = await PSQLService.CheckUser(email = UserModel.Email)
    if not User:
        raise HTTPException(status_code=401, detail="User not found")
    
    if UserModel.Password != User['User']['Password']:
        raise HTTPException(status_code=401, detail="Invalid password")
    UUID = User['User']['UserUUID']
    Date = str(datetime.now())
    RefreshToken = await JWTService.encodeToken(
        payload=dict(UUID = UUID), type='refresh'
    )
    AccessToken = await JWTService.encodeToken(
        payload = dict(UUID = UUID, LastLogin = Date), type='access'
    )
    response.set_cookie(
        key='RefreshToken', value=RefreshToken, httponly=False, expires = 60*60*24*30
    )
    return JSONResponse(
        status_code=200,
        content=dict(
           User = User,
           AccessToken = AccessToken
        )
    )

