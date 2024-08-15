from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

from Settings.Config import Config


class Base(DeclarativeBase):
    pass


Engine = create_async_engine(
    url = 'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'.format(
        USER = Config.POSTGRES_USER,
        PASSWORD = Config.POSTGRES_PASSWORD,
        HOST = Config.POSTGRES_HOST,
        PORT = Config.POSTGRES_PORT,
        DB = Config.POSTGRES_DB
    ),
    echo = True
)

Async_Session = sessionmaker(
    Engine, class_ = AsyncSession, expire_on_commit=False
)

async def GetSession()->AsyncGenerator[AsyncSession, None]:
    async with Async_Session() as session:
        yield session

async def InitModels():
    async with Engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)