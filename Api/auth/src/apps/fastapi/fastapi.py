from typing import List

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import APIRouter

from faststream.rabbit.fastapi import RabbitRouter
from faststream.confluent.fastapi import KafkaRouter



class Fastapi:

    def __init__(
        self, routers: List[APIRouter], kafka:  KafkaRouter, rabbit: RabbitRouter
    ) -> None:
        self.routers: List[APIRouter] = routers
        self.kafka: KafkaRouter = kafka
        self.rabbit: RabbitRouter = rabbit

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        async with(
            self.kafka.lifespan_context(app),
            self.rabbit.lifespan_context(app),
        ):
            yield
        yield

    def __call__(self) -> FastAPI:
        app = FastAPI(lifespan=self.lifespan)

        for router in self.routers:
            app.include_router(router)
        app.include_router(self.kafka)
        app.include_router(self.rabbit)

        return app
        