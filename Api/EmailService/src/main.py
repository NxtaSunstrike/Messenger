from contextlib import asynccontextmanager

from faststream import FastStream


app = FastStream()

@asynccontextmanager
async def lifespan(app):
    yield



