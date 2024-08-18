from dependency_injector import containers, providers

f

from Routers import Rabbit


class RabbitContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    rabbitmq = providers.Singleton(
        RabbitConfig,
        router = Rabbit.router,
        Host=config.HOST,
        Port=config.PORT,
        User=config.USER,
        Password=config.PASSWORD,
    )