from typing import List

from contextlib import asynccontextmanager

from faststream.asgi import AsgiFastStream

from faststream.rabbit import RabbitBroker
from faststream.rabbit.router import RabbitRouter


class Faststream:

    def __init__(
        self, rabbit: RabbitBroker,
        rabbit_routers: List[RabbitRouter],
    ) -> None:
        self.rabbit: RabbitBroker = rabbit
        self.rabbit_routers: List[RabbitRouter] = rabbit_routers


    @asynccontextmanager
    async def lifespan(self, app: AsgiFastStream):
        yield


    def __call__(self) -> AsgiFastStream:
        app = AsgiFastStream(
            self.rabbit, lifespan = self.lifespan, asyncapi_path = '/docs'
        )

        for router in self.rabbit_routers:
            self.rabbit.include_router(router)
        
        return app