from dependency_injector import providers, containers

from Utils.Jwt import JWTAuth

from Settings.Config import Settings




class JWTContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["Routers.Auth", 'Routers.JWT'])

    Config = Settings()

    JWT = providers.Singleton(
        JWTAuth, 
        public_key = Config.PublicKey.read_text(),
        secret_key = Config.PrivateKey.read_text(),
        algorithm = Config.Algorithm,
        access_expire = Config.AccessExpire,
        refresh_expire = Config.RefreshExpire,
    )