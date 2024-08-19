from typing import Any

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from Db.Postgres.Models.UserModel import *
from Db.Postgres.Models.IPUserModel import *
from Db.Postgres.Models.UserAgents import *
from Db.Postgres.Models.UserAvatars import *

from Di.SQLContainer import PSQLContainer
from Di.RedisContainer import RedisContainer
from Di.SessionContainer import SessionContainer
from Di.JWTContainer import JWTContainer

from Db.Postgres.Base import Database


class Application:

    def __init__(
        self, AuthRouter, JWTRouter, Db: Database
    ) -> None:
        self.AuthRouter = AuthRouter
        self.JWTRouter  = JWTRouter
        self.Db: Database = Db

    @asynccontextmanager
    async def lifespan(self,App: FastAPI):
        await self.Db.InitModels()
        
        PSQLContainer()
        RedisContainer()
        SessionContainer()
        JWTContainer()

        yield

    def __call__(self) -> FastAPI:
        app=FastAPI(
            lifespan=self.lifespan,
            title='Authorization Microservice',
            version='1.0.0'
        )

        
        app.include_router(self.JWTRouter)
        app.include_router(self.AuthRouter)

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        return app
