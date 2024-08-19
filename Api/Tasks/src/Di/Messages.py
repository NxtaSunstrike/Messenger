from dependency_injector import providers, containers

from Logic.Messages import Messages


class MessagesContainer(containers.DeclarativeContainer):
    
    config = providers.Configuration()

    Messages = providers.Singleton(
        Messages,
        Host = config.host,
        Port = config.port,
        Pass = config.password,
        User = config.user,
    )