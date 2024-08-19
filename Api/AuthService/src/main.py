from fastapi import FastAPI
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from Db.Postgres.Models.UserModel import *
from Db.Postgres.Models.IPUserModel import *
from Db.Postgres.Models.UserAgents import *
from Db.Postgres.Models.UserAvatars import *

from Di.Containers import RedisContainer
from Di.Containers import SessionContainer
from Di.Containers import PSQLContainer
from Di.Containers import JWTContainer

from Settings.Config import Settings

from Routers import Auth
from Routers import JWT


@asynccontextmanager
async def lifespan(App: FastAPI):
    Config = Settings()
    redis = RedisContainer()
    session = SessionContainer()
    psql = PSQLContainer()
    jwt = JWTContainer()

    redis.config.url.from_value(f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/1")
    session.config.url.from_value(f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/2")

    psql.config.url.from_value('postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'.format(
        USER=Config.POSTGRES_USER,
        PASSWORD=Config.POSTGRES_PASSWORD,
        HOST=Config.POSTGRES_HOST,
        PORT=Config.POSTGRES_PORT,
        DB=Config.POSTGRES_DB
    ))
    
    jwt.config.secret_key.from_value(Config.PrivateKey.read_text())
    jwt.config.algorithm.from_value(Config.Algorithm)
    jwt.config.access_expire.from_value(Config.AccessExpire)
    jwt.config.refresh_expire.from_value(Config.RefreshExpire)
    jwt.config.public_key.from_value(Config.PublicKey.read_text())

    db = psql.Db()
    await db.InitModels()

    yield

app=FastAPI(
    lifespan=lifespan,
    title='Authorization Microservice',
    version='1.0.0'
)

# App.add_middleware(LimitRequestsMiddleware)
app.include_router(Auth.router)
app.include_router(JWT.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
