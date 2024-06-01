from typing import Any, Mapping

from .cache import Cache, CacheValue


class InMemoryCache(Cache):
    store: dict[str, Any]

    def __init__(self):
        self.store = {}

    async def get(self, key: str) -> str | None:
        return self.store.get(key, None)

    async def multi_get(self, keys: list[str]) -> list[str | None]:
        return [self.store.get(key, None) for key in keys]

    async def set(self, key: str, value: CacheValue) -> bool:
        self.store[key] = value
        return True

    async def multi_set(self, values: Mapping[str, CacheValue]) -> bool:
        for key, value in values.items():
            self.store[key] = value
        return True

    async def delete(self, key: str) -> bool:
        return await self.multi_delete([key])

    async def multi_delete(self, keys: list[str]) -> bool:
        for key in keys:
            result =  self.store.pop(key, False)
            if result is False:
                return False
        return True
