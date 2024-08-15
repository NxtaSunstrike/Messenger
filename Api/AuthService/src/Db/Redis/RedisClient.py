import json

from typing import Dict

import redis.asyncio as AIORedis

from Settings.Config import Config

from Utils.JsonUtils import BytesEncoder


class RedisClient:

    def __init__(self, url: str) -> None:
        self.Redis = AIORedis.from_url(url)


    async def CreateItem(self, key: str, value: Dict) -> None:
        result = json.dumps(value)
        await self.Redis.set(key, result)
        return dict(
            message = f'Item {key} created successful'
        )
    
    
    async def getItem(self, key: str) -> json:
        result = await self.Redis.get(key)
        if result:
            result = json.loads(result)
        return result
    

    async def DeleteItem(self, key: str) -> None:
        await self.Redis.delete(key)
        return dict(
            message = f'Item {key} deleted successful'
        )
    
AuthCache = RedisClient('redis://{HOST}:{port}/1'.format(
    HOST = Config.REDIS_HOST,
    port = Config.REDIS_PORT
))
UserCache = RedisClient('redis://{HOST}:{port}/2'.format(
    HOST = Config.REDIS_HOST,
    port = Config.REDIS_PORT
))