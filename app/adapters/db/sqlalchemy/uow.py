from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..uow import Uow
from .repositories import SqlAlchemyUserRepository


def session_factory_builder(engine: AsyncEngine, **kwargs: Any):
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        **kwargs,
    )


class SqlAlchemyUow(Uow):
    # repositories
    user_repository: SqlAlchemyUserRepository

    # session
    session_factory: Any
    session: AsyncSession

    def __init__(
        self,
        engine: AsyncEngine,
        isolation_level: str | None = "REPEATABLE READ",
        **kwargs: Any,
    ):
        if isolation_level is not None:
            kwargs["isolation_level"] = isolation_level  # only add if set

        self.session_factory = session_factory_builder(engine, **kwargs)

    async def __aenter__(self):
        async with self.session_factory() as session:
            async with session.begin():
                self.session = session
                self.user_repository = SqlAlchemyUserRepository(session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        # if nothing to rollback, nothing will happen
        await self.session.rollback()

    async def close(self):
        await self.session.close()
