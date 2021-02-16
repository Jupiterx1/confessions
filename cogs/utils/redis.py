from logging import getLogger
from typing import Union

from aioredis import create_redis_pool as _create_redis_pool, RedisConnection


logger = getLogger('confession.redis')



class RedisConnection(object):

    config = None
    pool = None


    def __init__(self, connection:RedisConnection=None, sustain:bool=False):
        self.conn = connection
        self.sustain = sustain


    @classmethod
    def set_config(cls, config:dict):
        address = config.pop('host'), config.pop('port')
        cls.config = dict(address=address, **config)


    @classmethod
    async def create_pool(cls, config:dict):
        cls.config = config
        address = config.pop('host'), config.pop('port')
        cls.pool = await _create_redis_pool(address, **config)


    async def __aenter__(self):
        self.conn = self.pool
        return self


    async def __aexit__(self, exc_type, exc, tb):
        pass

    
    async def publish_json(self, channel:str, json:dict):
        logger.debug(f"Publishing JSON to channel {channel}: {json!s}")
        return await self.conn.publish_json(channel, json)


    async def set(self, key:str, value:str):
        logger.debug(f"Publishing Redis key:value pair with {key}:{value}")
        return await self.conn.set(key, value)

    
    async def get(self, key:str):
        v = await self.conn.get(key)
        logger.debug(f"Getting Redis key with {key}:{v!s}")
        if v:
            return v.decode()
        return v
