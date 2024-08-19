from faststream.asgi import AsgiFastStream
from faststream.rabbit import RabbitBroker, RabbitQueue

from Settings.Config import Settings

from Di.Rabbit import RabbitContainer
from Di.Messages import MessagesContainer

class Application:

    def __init__(
        self, broker: RabbitContainer, config: Settings, message: MessagesContainer
    ) -> None:
        self.rabbit: RabbitContainer = broker
        self.Config: Settings = config
        self.messages: MessagesContainer = message

    def RabbitStartup(self) -> RabbitBroker:
        self.rabbit.config.HOST.from_value(self.Config.RABBITMQ_HOST)
        self.rabbit.config.PORT.from_value(self.Config.RABBITMQ_PORT)
        self.rabbit.config.USER.from_value(self.Config.RABBITMQ_DEFAULT_USER)
        self.rabbit.config.PASSWORD.from_value(self.Config.RABBITMQ_DEFAULT_PASS)

        Broker = self.rabbit.rabbitmq()
        return Broker.Broker()
    
    def MessagesStartup(self) -> None:
        self.messages.config.host.from_value(self.Config.EMAIL_HOST)
        self.messages.config.port.from_value(self.Config.EMAIL_PORT)
        self.messages.config.user.from_value(self.Config.EMAIL_USER)
        self.messages.config.password.from_value(self.Config.EMAIL_PASSWORD)
    
    def __call__(self) -> AsgiFastStream:
        app = AsgiFastStream(
            self.RabbitStartup(),
            title='FastStream Demo', 
            version='1.0.0', 
            asyncapi_path='/docs',
        )
        return app
