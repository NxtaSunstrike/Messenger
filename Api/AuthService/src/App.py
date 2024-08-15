import typing

from fastapi import FastAPI
from fastapi import Depends

from contextlib import asynccontextmanager

from Db.Postgres.Base import InitModels

from Db.Postgres.Models.UserModel import *
from Db.Postgres.Models.IPUserModel import *
from Db.Postgres.Models.UserAgents import *
from Db.Postgres.Models.UserAvatars import *

from Middleware.RequestsMiddleware import LimitRequestsMiddleware

from Routers.Auth import AuthRouter


@asynccontextmanager
async def lifespan(App: FastAPI):
    await InitModels()
    yield

App=FastAPI(
    lifespan=lifespan,
    title='Authorization Microservice',
    version='1.0.0'
)

# App.add_middleware(LimitRequestsMiddleware)
App.include_router(AuthRouter)