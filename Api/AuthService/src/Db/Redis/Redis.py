from typing import AsyncIterator

from redis.asyncio import Redis, from_url


async def InitializeRedisPool(url: str) -> AsyncIterator[Redis]:
    redis = from_url(url = url, encoding="utf-8", decode_responses=True)
    yield redis
    await redis.close()
    await redis.wait_closed()