import jwt

from datetime import datetime, timedelta


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
            expire = str(datetime.now() + timedelta(minutes=self.access_expire))
        elif type == 'refresh':
            expire = str(datetime.now() + timedelta(days=self.refresh_expire))
        data.update(
            dict(
                expire = expire, type = type
            )
        )
        return jwt.encode(payload = data, key = self.secret_key, algorithm = self.alghorithm)

