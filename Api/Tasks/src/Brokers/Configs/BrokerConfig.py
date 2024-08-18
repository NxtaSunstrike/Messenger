from faststream.rabbit import RabbitBroker, RabbitRouter


class RabbitConfig:

    def __init__(self, 
        User: str, Password: str, Host: str, Port: str, router: RabbitRouter
    ) -> None:
        self.User = User
        self.Password = Password
        self.Host = Host
        self.Port = Port
        self.router = router


    def Broker(self) -> RabbitBroker:
        Broker = RabbitBroker(
            url=f"amqp://{self.User}:{self.Password}@{self.Host}:{self.Port}/",
        )
        Broker.include_router(router = self.router)
        return Broker
