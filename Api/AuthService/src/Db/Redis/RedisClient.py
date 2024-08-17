import json

from typing import Dict

from redis.asyncio import Redis


class Service:

    def __init__(self, redis: Redis) -> None:
        self._redis = redis


    async def CreateUser(self, key: str, value: Dict) -> None:
        result = json.dumps(value)
        await self._redis.set(name = key, value = result)
        return dict(
            message = f'Item {key} created successful'
        )
    
    
    async def getUser(self, key: str) -> json:
        result = await self._redis.get(name = key)
        if result:
            result = json.loads(result)
        return result
    

    async def DeleteUser(self, key: str) -> None:
        await self._redis.delete(key)
        return dict(
            message = f'Item {key} deleted successful'
        )
    

    
