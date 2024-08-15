from os import environ as env

from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import Field

BaseDir = Path('Api')

from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    POSTGRES_HOST: str = Field(env.get('POSTGRES_HOST'))
    POSTGRES_PORT: str = Field(env.get('POSTGRES_PORT'))
    POSTGRES_DB: str = Field(env.get('POSTGRES_DB'))
    POSTGRES_USER: str = Field(env.get('POSTGRES_USER'))
    POSTGRES_PASSWORD: str = Field(env.get('POSTGRES_PASSWORD'))

    REDIS_HOST: str = Field(env.get('REDIS_HOST'))
    REDIS_PORT: str = Field(env.get('REDIS_PORT'))

    RABBITMQ_USER: str = Field(env.get('RABBITMQ_DEFAULT_USER'))
    RABBITMQ_PASSWORD: str = Field(env.get('RABBITMQ_DEFAULT_PASS'))
    RABBITMQ_HOST: str = Field(env.get('RABBITMQ_HOST'))
    RABBITMQ_PORT: str = Field(env.get('RABBITMQ_PORT'))

    PublicKey: Path = BaseDir / 'AuthService' / 'jwt-public.pem'
    PrivateKey: Path = BaseDir / 'AuthService' / 'jwt-private.pem'
    Algorithm: str = Field(env.get('ALGORITHM'))
    AccessExpire: int = Field(env.get('ACCESS_EXPIRE'))
    RefreshExpire: int = Field(env.get('REFRESH_EXPIRE'))


Config = Settings()
   

