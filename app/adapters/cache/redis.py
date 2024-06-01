from typing import Mapping

from redis.asyncio import Redis

from .cache import Cache, CacheValue


class Redis(Cache):
    rc: Redis

    def __init__(self, rc: Redis):
        self.rc = rc

    async def get(self, key: str) -> str | None:
        return await self.rc.get(key)

    async def multi_get(self, keys: list[str]) -> list[str | None]:
        return await self.rc.mget(keys)

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
