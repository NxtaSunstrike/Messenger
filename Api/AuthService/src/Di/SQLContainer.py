from dependency_injector import providers, containers

from Db.Postgres.Base import Database
from Db.Postgres.Crud.Repositories import UserRepository
from Db.Postgres.Crud.Services import UserService

from Settings.Config import Settings



class PSQLContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["Routers.Auth"])

    Config = Settings()

    Db = providers.Singleton(
        Database, 
        host = Config.POSTGRES_HOST,
        port = Config.POSTGRES_PORT,
        user = Config.POSTGRES_USER,
        password = Config.POSTGRES_PASSWORD,
        database = Config.POSTGRES_DB,
    )

    UserRepo = providers.Factory(
        UserRepository,
        session = Db.provided.GetSession,
    )

    UserSevice = providers.Factory(
        UserService,
        UserRepo = UserRepo,
    )
