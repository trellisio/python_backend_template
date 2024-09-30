from abc import ABC, abstractmethod
from functools import wraps
from inspect import signature

from .cache import Cache


class Query(ABC):
    """Port to query views / list of objects from database
    Impl is a transactionless select stmt
    Port also implements a cache-aside strategy
    """

    _cache: Cache
    _cache_key_prefix = "__port-Query"

    _cache_list = ["list_users"]  # List of methods to be cached

    def __init__(self, cache: Cache):
        self._cache = cache
        self._cache_key_prefix = "__port_Query"
        self._decorate_to_be_cached_methods()

    @abstractmethod
    async def list_users(self) -> list[str]:
        raise NotImplementedError()

    def _decorate_to_be_cached_methods(self):
        for name in self._cache_list:
            method = getattr(self, name)

            sig = signature(method)
            parameters = sig.parameters
            keys = list(parameters.keys())

            cache_key = f"{self._cache_key_prefix}_{"_".join(keys)}"

            @wraps(method)
            async def fn(*args, **kwargs):
                result = await self._cache.get(cache_key)
                if result:
                    return result

                result = await method(*args, **kwargs)
                await self._cache.set(cache_key, result)
                return result

            setattr(self, name, fn)
