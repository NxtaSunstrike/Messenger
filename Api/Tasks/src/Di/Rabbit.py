from dependency_injector import containers, providers

from Brokers.BrokerConfig import RabbitConfig

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
