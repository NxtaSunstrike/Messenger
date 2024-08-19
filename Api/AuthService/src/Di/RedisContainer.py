from dependency_injector import providers, containers

from Db.Redis.Redis import InitializeRedisPool
from Db.Redis import RedisClient

from Settings.Config import Settings


class RedisContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["Routers.Auth"])

    Config = Settings()
    
    RedisPool = providers.Resource(
        InitializeRedisPool,
        url = f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/1",
    )

    Service = providers.Factory(
        RedisClient.Service,
        redis = RedisPool,
    )