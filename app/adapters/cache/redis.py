from typing import Mapping

from kink import di, inject
from pydantic import Field
from pydantic_settings import BaseSettings
from redis.asyncio import Redis

from app.logger import logger

from ..connection import Connection
from .cache import Cache, CacheValue


class RedisConnectionConfig(BaseSettings):
    REDIS_HOST: str = Field(description="Redis host URL", default="redis")
    REDIS_PORT: int = Field(description="Redis host port", default=6379)
    REDIS_PASSWORD: str = Field(description="Redis password", default="password")


@inject(alias=Connection)
class RedisConnection(Connection):
    rc: Redis
    
    async def connect(self):
        config = RedisConnectionConfig()
        rc = Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            password=config.REDIS_PASSWORD,
            protocol=3,
            db=0,
            decode_responses=True,
        )
        
        self.rc = rc
        di[Redis] = rc
        
        await rc.ping()
        
        logger.info("Redis connected 🚨")
    
    async def close(self):
        await self.rc.aclose()


@inject(alias=Cache)
class RedisCache(Cache):
    rc: Redis

    def __init__(self, rc: Redis):
        self.rc = rc

    async def get(self, key: str) -> str | None:
        return await self.rc.get(key)

    async def multi_get(self, keys: list[str]) -> list[str | None]:
        return await self.rc.mget(keys).decode("utf-8")

    async def set(self, key: str, value: CacheValue) -> bool:
        ok = await self.rc.set(key, value)
        if ok:
            return ok
        raise Exception(f"Unable to set val {value} for key {key}")

    async def multi_set(self, values: Mapping[str, CacheValue]) -> list[bool]:
        ok = await self.rc.mset(values)
        if ok:
            return ok
        raise Exception(f"Unable to mset for {values}")

    async def delete(self, key: str) -> bool:
        return await self.multi_delete([key])

    async def multi_delete(self, keys: list[str]) -> list[bool]:
        ok = await self.rc.delete(*keys)
        if ok:
            return ok
        raise Exception(f"Unable to delete for {keys}")
