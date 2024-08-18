from os import environ as env

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    RABBITMQ_HOST: str = Field(env.get('RABBITMQ_HOST'))
    RABBITMQ_PORT: int = Field(env.get('RABBITMQ_PORT'))
    RABBITMQ_DEFAULT_USER: str = Field(env.get('RABBITMQ_DEFAULT_USER'))
    RABBITMQ_DEFAULT_PASS: str = Field(env.get('RABBITMQ_DEFAULT_PASS'))

    EMAIL_HOST: str = Field(env.get('EMAIL_HOST'))
    EMAIL_PORT: int = Field(env.get('EMAIL_PORT'))
    EMAIL_USER: str = Field(env.get('EMAIL_USER'))
    EMAIL_PASSWORD: str = Field(env.get('EMAIL_PASSWORD'))
    