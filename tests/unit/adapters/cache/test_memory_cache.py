import pytest

from app.adapters.cache.memory import InMemoryCache


class TestInMemoryCache:
    cache: InMemoryCache

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.cache = InMemoryCache()

    @pytest.mark.asyncio
    async def test_can_set_value(self):
        pass

    @pytest.mark.asyncio
    async def test_can_set_values(self):
        pass

    @pytest.mark.asyncio
    async def test_can_cache_value(self):
        pass

    @pytest.mark.asyncio
    async def test_can_cache_values(self):
        pass
