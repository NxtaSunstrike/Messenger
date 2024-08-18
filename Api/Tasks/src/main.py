from Di.Application import ApplicationContainer

from faststream.asgi import AsgiFastStream


def createApp() -> AsgiFastStream:
    Container = ApplicationContainer()
    App = Container.Application()
    return App

app = createApp()