import pytest

from app.adapters import Connections
from app.adapters.cache.redis import RedisCache


class TestRedisCache:
    cache: RedisCache

    @pytest.fixture(autouse=True)
    def set_up(self, connections: Connections):
        self.cache = RedisCache(connections.rc)

    async def test_can_set_value(self):
        res = await self.cache.set("service", "service_name")
        assert res is True

    async def test_can_set_values(self):
        res = await self.cache.multi_set(
            {"service": "service_name", "name": "developer", "company": "trellis"}
        )
        assert res is True

    async def test_can_cache_value(self):
        await self.cache.set("service", "service_name")
        res = await self.cache.get("service")
        assert res == "service_name"

    async def test_can_cache_values(self):
        await self.cache.multi_set(
            {"service": "service_name", "name": "developer", "company": "trellis"}
        )
        res = await self.cache.get("service")
        assert res == "service_name"
        res = await self.cache.get("name")
        assert res == "developer"
        res = await self.cache.get("company")
        assert res == "trellis"

    async def test_can_delete_value(self):
        await self.cache.set("service", "service_name")
        await self.cache.delete("service")
        res = await self.cache.get("service")
        assert res is None

    async def test_can_delete_values(self):
        await self.cache.multi_set(
            {"service": "service_name", "name": "developer", "company": "trellis"}
        )
        await self.cache.multi_delete(["service", "name", "company"])
        res = await self.cache.get("service")
        assert res is None
        res = await self.cache.get("name")
        assert res is None
        res = await self.cache.get("company")
        assert res is None
