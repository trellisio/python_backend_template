from typing import Mapping

from kink import inject
from redis.asyncio import Redis

from app.services.ports.cache import Cache, CacheValue

from .connection import RedisConnection


@inject(alias=Cache)
class RedisCache(Cache):
    rc: Redis

    def __init__(self, connection: RedisConnection):
        self.rc = connection.rc

    async def get(self, key: str) -> str | None:
        return await self.rc.get(key)

    async def multi_get(self, keys: list[str]) -> list[str | None]:
        result = await self.rc.mget(keys)
        return result.decode("utf-8")

    async def set(self, key: str, value: CacheValue, ttl: int | None = None) -> bool:
        ok = await self.rc.set(key, value, ex=ttl)
        return bool(ok)

    async def multi_set(self, values: Mapping[str, CacheValue]) -> bool:
        ok = await self.rc.mset(values)
        return bool(ok)

    async def delete(self, key: str) -> bool:
        return await self.multi_delete([key])

    async def multi_delete(self, keys: list[str]) -> bool:
        ok = await self.rc.delete(*keys)
        return bool(ok)
