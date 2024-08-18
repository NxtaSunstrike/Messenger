from Di.Application import ApplicationContainer


def createApp():
    Container = ApplicationContainer()
    App = Container.Application()
    return App

app = createApp()