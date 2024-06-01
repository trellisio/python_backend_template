import pytest

from app.adapters.cache.memory import InMemoryCache
from app.adapters.cache.redis import RedisCache
from app.connections import Connections


class TestInMemoryCache:
    cache: InMemoryCache

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.cache = InMemoryCache()

    @pytest.mark.asyncio
    async def test_can_set_value(self):
        res = await self.cache.set("service", "service_name")
        assert res is True
        assert self.cache.store.get("service", None) == "service_name"

    @pytest.mark.asyncio
    async def test_can_set_values(self):
        res = await self.cache.multi_set(
            [("service", "service_name"), ("name", "developer"), ["company", "trellis"]]
        )
        assert len(res) == 3
        assert res == [True, True, True]
        assert self.cache.store.get("service", None) == "service_name"
        assert self.cache.store.get("name", None) == "developer"
        assert self.cache.store.get("company", None) == "trellis"

    @pytest.mark.asyncio
    async def test_can_cache_value(self):
        await self.cache.set("service", "service_name")
        res = await self.cache.get("service")
        assert res == "service_name"

    @pytest.mark.asyncio
    async def test_can_cache_values(self):
        await self.cache.multi_set(
            [("service", "service_name"), ("name", "developer"), ["company", "trellis"]]
        )
        res = await self.cache.get("service")
        assert res == "service_name"
        res = await self.cache.get("name")
        assert res == "developer"
        res = await self.cache.get("company")
        assert res == "trellis"

    @pytest.mark.asyncio
    async def test_can_delete_value(self):
        await self.cache.set("service", "service_name")
        await self.cache.delete("service")
        res = await self.cache.get("service")
        assert res is None

    @pytest.mark.asyncio
    async def test_can_delete_values(self):
        await self.cache.multi_set(
            [("service", "service_name"), ("name", "developer"), ["company", "trellis"]]
        )
        await self.cache.multi_delete(["service", "name", "company"])
        res = await self.cache.get("service")
        assert res is None
        res = await self.cache.get("name")
        assert res is None
        res = await self.cache.get("company")
        assert res is None


class TestRedisCache(TestInMemoryCache):
    cache: RedisCache

    @pytest.fixture(autouse=True)
    def set_up(self, Connections: Connections):
        self.cache = RedisCache(Connections.rc)
