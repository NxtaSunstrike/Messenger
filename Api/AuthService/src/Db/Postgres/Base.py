from typing import AsyncGenerator

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass


class Database:


    def __init__(
        self, host: str, port: int, password: str, user: str, database: str
    ) -> None: 
        self.Engine = create_async_engine(
            url = 'postgresql+asyncpg://{user}:{password}@{hots}:{port}/{db}'.format(
                user = user, password = password, hots = host, port = port, db = database
            ), 
        echo = True)

        self.Async_Session = sessionmaker(
            bind = self.Engine, class_ = AsyncSession, expire_on_commit=False
        )

    @asynccontextmanager
    async def GetSession(self)->AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self.Async_Session()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


    async def InitModels(self) -> None:
        async with self.Engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)

