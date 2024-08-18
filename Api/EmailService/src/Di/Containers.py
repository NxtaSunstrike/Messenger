from dependency_injector import containers, providers


class BaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()