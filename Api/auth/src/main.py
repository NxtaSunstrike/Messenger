from fastapi import FastAPI

import uvicorn

from apps.fastapi.fastapi import Fastapi

from apps.fastapi.routers import auth_router
from apps.faststream.rpc.routers import kafka_router
from apps.faststream.tasks.routers import task_router



app = Fastapi(
    routers = [auth_router.router, ],
    kafka = kafka_router.router,
    rabbit =task_router.router
)


