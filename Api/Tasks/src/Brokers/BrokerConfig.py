from faststream.rabbit import RabbitBroker, RabbitRouter


class RabbitConfig:

    def __init__(
        self, User: str, Password: str, Host: str, Port: int, router: RabbitRouter
    ) -> None:
        self.User: str = User
        self.Password: str = Password
        self.Host: str = Host
        self.Port: int = Port
        self.router: RabbitRouter = router


    def Broker(self) -> RabbitBroker:

        Broker = RabbitBroker(
            url=f"amqp://{self.User}:{self.Password}@{self.Host}:{self.Port}/",
        )
        Broker.include_router(router = self.router)
        return Broker
