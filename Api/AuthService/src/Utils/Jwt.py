from jwt import JWT

from datetime import datetime, timedelta

from Settings.Config import Config


class JWTAuth:

    def __init__(self, 
        secret_key: str, algorithm: str, public_key: str, 
        access_expire: int, refresh_expire: int
    )->None:
        self.alghorithm = algorithm
        self.public_key = public_key
        self.secret_key = secret_key
        self.access_expire = access_expire
        self.refresh_expire = refresh_expire

    
    async def decodeToken(self, token: str):
        return jwt.decode(token = token, key = self.public_key, algorithms = [self.alghorithm])


    async def encodeToken(self, payload: dict, type: str):
        data = payload.copy()
        if type == 'access':
            expire = datetime.now() + timedelta(minutes=self.access_expire)
        elif type == 'refresh':
            expire = datetime.now() + timedelta(days=self.refresh_expire)
        data.update(
            dict(
                expire = expire, type = type
            )
        )
        return JWT.encode(payload = data, key = self.secret_key, alg = self.alghorithm)



jwt = JWT(
    secret_key = Config.PrivateKey.read_text(),
    algorithm = Config.Algorithm,
    public_key = Config.PublicKey.read_text(),
    access_expire = Config.AccessExpire,
    refresh_expire = Config.RefreshExpire
)