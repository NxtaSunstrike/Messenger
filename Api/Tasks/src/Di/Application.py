from dependency_injector import containers, providers

from Settings.Config import Settings

from App.Application import Application

from Di.Rabbit import RabbitContainer
from Di.Messages import MessagesContainer





class ApplicationContainer(containers.DeclarativeContainer):


    Settings = providers.Singleton(
        Settings,
    )
    Application = providers.Singleton(
        Application,
        config = Settings.provided,
        broker = RabbitContainer,
        message = MessagesContainer
    )

