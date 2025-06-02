import os
import logging
import redis.asyncio as aioredis


CACHE_URL = os.getenv('CACHE_URL', '')
logger = logging.getLogger('uvicorn.error')

class RedisCache():

    def __init__(self):
        logger.info(f'RedisCache.__init__(). Redis URL = {CACHE_URL}')
        self.redis = aioredis.Redis.from_url(CACHE_URL)

    async def connection_close(self):
        await self.redis.aclose()

    async def set(self, key, value, ex=86400):
        await self.redis.set(key, value, ex=ex)

    async def get(self, key):
        return await self.redis.get(key)

