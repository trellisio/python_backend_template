from typing import cast

import pytest
from sqlalchemy.future import select

from app.domain import models
from app.domain.models.user import DomainEvent
from app.infra.memory.publisher import InMemoryEventPublisher
from app.infra.sqlalchemy.uow import (
    SqlAlchemyUow,
    SqlAlchemyUserRepository,
    SqlConnection,
)


class SqlAlchemyUserRepositoryImpl(SqlAlchemyUserRepository):
    async def find_by_email(self, email: str) -> list[models.User]:
        stmt = select(models.User).where(models.User.email == email)  # type: ignore
        res = await self.session.execute(stmt)
        return cast(list[models.User], res.scalars().all())

    async def remove_by_email(self, email: str) -> list[models.User]:
        stmt = select(models.User).where(models.User.email == email)  # type: ignore
        res = await self.session.execute(stmt)
        users = cast(list[models.User], res.scalars().all())

        for user in users:
            await self.session.delete(user)

        return users


class SqlAlchemyUowImpl(SqlAlchemyUow):
    user_repository: SqlAlchemyUserRepositoryImpl

    async def __aenter__(self):
        async with self.session_factory() as session:
            async with session.begin():
                self.session = session
                self.user_repository = SqlAlchemyUserRepositoryImpl(session)


class TestRepository:
    uow: SqlAlchemyUowImpl

    @pytest.fixture(autouse=True)
    async def set_up(self):
        # create database tables
        connection = SqlConnection()
        await connection.connect()
        self.uow = SqlAlchemyUowImpl(connection, InMemoryEventPublisher())
        await self._seed_model()

        yield

        await connection.close(cleanup=True)

    async def test_find_methods_have_objects_added_to_seen(self):
        async with self.uow:
            users = await self.uow.user_repository.find_by_email(
                email="email@gmail.com"
            )
            assert len(users) == 1
            assert set(users) == self.uow.user_repository.seen

        async with self.uow:
            users = await self.uow.user_repository.find(email="email@gmail.com")
            assert len(users) == 1
            assert set(users) == self.uow.user_repository.seen

    async def test_remove_methods_have_objects_added_to_seen(self):
        async with self.uow:
            users = await self.uow.user_repository.remove_by_email(
                email="email@gmail.com"
            )
            assert len(users) == 1
            assert set(users) == self.uow.user_repository.seen

    async def test_add_methods_have_objects_added_to_seen(self):
        async with self.uow:
            user = models.User(email="some-email@gmail.com")
            await self.uow.user_repository.add(user)
            assert set([user]) == self.uow.user_repository.seen

    async def _seed_model(self, email: str = "email@gmail.com"):
        async with self.uow:
            user = models.User(email=email)
            await self.uow.user_repository.add(user)
            await self.uow.commit()


class TestUow:
    uow: SqlAlchemyUowImpl
    publisher: InMemoryEventPublisher

    @pytest.fixture(autouse=True)
    async def set_up(self):
        # create database tables
        connection = SqlConnection()
        await connection.connect()
        self.publisher = InMemoryEventPublisher()
        self.uow = SqlAlchemyUowImpl(connection, self.publisher)
        await self._seed_model()

        yield

        await connection.close(cleanup=True)

    async def test_domain_events_are_published(self):
        async with self.uow:
            users = await self.uow.user_repository.find_by_email(
                email="email@gmail.com"
            )
            assert len(users) == 1
            user = users[0]
            user.some_domain_method()
            assert user.events == [DomainEvent("email@gmail.com")]
            await self.uow.commit()

            assert self.publisher.published_messages == [
                {
                    "channel": "DomainThingHappened",
                    "payload": {"email": "email@gmail.com"},
                }
            ]

    async def test_aggregate_versions_are_auto_incremented(self):
        async with self.uow:
            users = await self.uow.user_repository.find_by_email(
                email="email@gmail.com"
            )
            assert len(users) == 1
            user = users[0]
            user.some_domain_method()

        async with self.uow:
            users = await self.uow.user_repository.find_by_email(
                email="email@gmail.com"
            )
            assert len(users) == 1
            user = users[0]
            assert user.version == 1

    async def _seed_model(self, email: str = "email@gmail.com"):
        async with self.uow:
            user = models.User(email=email)
            await self.uow.user_repository.add(user)
            await self.uow.commit()
