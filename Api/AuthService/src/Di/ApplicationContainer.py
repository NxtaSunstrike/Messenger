from dependency_injector import providers, containers

from App.Application import Application
from Di.SQLContainer import PSQLContainer

from Routers.Auth import router as AuthRouter
from Routers.JWT import router as JWTRouter







class ApplicationContainer(containers.DeclarativeContainer):

    

    Application = providers.Singleton(
        Application,
        AuthRouter = AuthRouter,
        JWTRouter = JWTRouter,
        Db = PSQLContainer.Db,
    )