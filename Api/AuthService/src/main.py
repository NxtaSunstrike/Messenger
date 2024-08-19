from fastapi import FastAPI

from Di.ApplicationContainer import ApplicationContainer


def Start() -> FastAPI:
    Container = ApplicationContainer()
    application = Container.Application()
    return application


app = Start()

