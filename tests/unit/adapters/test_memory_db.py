import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app import models
from app.adapters.db.sqlalchemy import SqlAlchemyUow
from app.adapters.db.sqlalchemy.tables import metadata

DB_URL = "sqlite+aiosqlite:///:memory:"


class TestInMemoryDb:
    engine: AsyncEngine = create_async_engine(DB_URL, future=True)
    uow: SqlAlchemyUow

    @pytest.fixture(autouse=True)
    async def set_up(self):
        # create database tables
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)

        self.uow = SqlAlchemyUow(self.engine, isolation_level=None)

    async def test_can_insert_model(self):
        async with self.uow:
            user = models.User(email="email@gmail.com")
            await self.uow.user_repository.add(user)
            await self.uow.commit()

    # @pytest.mark.asyncio
    # async def test_can_select_model(self):
    #     pass

    # @pytest.mark.asyncio
    # async def test_can_list_models(self):
    #     pass

    # @pytest.mark.asyncio
    # async def test_can_remove_model(self):
    #     pass

    # @pytest.mark.asyncio
    # async def test_can_rollback(self):
    #     pass

    # @pytest.mark.asyncio
    # async def test_rollback_occurs_when_commit_not_called(self):
    #     pass

    # @pytest.mark.asyncio
    # async def test_rollback_occurs_when_error_is_raised(self):
    #     pass
