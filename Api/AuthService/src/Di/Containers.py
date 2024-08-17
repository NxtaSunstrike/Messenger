from dependency_injector import providers, containers

from Db.Redis.Redis import InitializeRedisPool
from Db.Redis import RedisClient

from Db.Postgres.Base import Database
from Db.Postgres.Crud.Repositories import UserRepository
from Db.Postgres.Crud.Services import UserService

from Utils.Jwt import JWTAuth


class RedisContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["Routers.Auth"])

    config = providers.Configuration()
    
    RedisPool = providers.Resource(
        InitializeRedisPool,
        url = config.url,
    )

    Service = providers.Factory(
        RedisClient.Service,
        redis = RedisPool,
    )


class SessionContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["Routers.Auth"])

    config = providers.Configuration()

    RedisPool = providers.Resource(
        InitializeRedisPool,
        url = config.url,
    )

    AuthSession = providers.Factory(
        RedisClient.Service,
        redis = RedisPool,
    )
      

class PSQLContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["Routers.Auth"])

    config = providers.Configuration()

    Db = providers.Singleton(Database, url = config.url)

    UserRepo = providers.Factory(
        UserRepository,
        session = Db.provided.GetSession,
    )

    UserSevice = providers.Factory(
        UserService,
        UserRepo = UserRepo,
    )


class JWTContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["Routers.Auth", 'Routers.JWT'])

    config = providers.Configuration()

    JWT = providers.Singleton(
        JWTAuth, 
        public_key = config.public_key,
        secret_key = config.secret_key,
        algorithm = config.algorithm,
        access_expire = config.access_expire,
        refresh_expire = config.refresh_expire,
    )