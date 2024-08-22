from os import environ as env

from pydantic_settings import BaseSettings
from pydantic import Field


class RabbitConfig(BaseSettings):
    host: str = Field(env.get('RABBITMQ_HOST'))
    port: int = Field(env.get('RABBITMQ_PORT'))
    user: str = Field(env.get('RABBITMQ_DEFAULT_USER'))
    password: str = Field(env.get('RABBITMQ_DEFAULT_PASS'))


class RedisConfig(BaseSettings):
    host: str = Field(env.get('REDIS_HOST'))
    port: int = Field(env.get('REDIS_PORT'))


class PostgresConfig(BaseSettings):
    host: str = Field(env.get('POSTGRES_HOST'))
    port: int = Field(env.get('POSTGRES_PORT'))
    user: str = Field(env.get('POSTGRES_USER'))
    password: str = Field(env.get('POSTGRES_PASSWORD'))
    database: str = Field(env.get('POSTGRES_DB'))


class KafkaConfig(BaseSettings):
    host: str = Field(env.get('KAFKA_HOST'))
    port: int = Field(env.get('KAFKA_PORT'))
    user: str = Field(env.get('KAFKA_USER'))
    password: str = Field(env.get('KAFKA_PASSWORD'))


class GateAwayConfig(BaseSettings):
    pass