from abc import ABC, abstractmethod
from typing import Mapping

type CacheValue = str | int | float | bool


class Cache(ABC):
    @abstractmethod
    async def get(self, key: str) -> str | None:
        raise NotImplementedError()

    @abstractmethod
    async def multi_get(self, keys: list[str]) -> list[str | None]:
        raise NotImplementedError()

    @abstractmethod
    async def set(self, key: str, value: CacheValue) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def multi_set(self, values: Mapping[str, CacheValue]) -> list[bool]:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, key: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def multi_delete(self, keys: list[str]) -> list[bool]:
        raise NotImplementedError()
