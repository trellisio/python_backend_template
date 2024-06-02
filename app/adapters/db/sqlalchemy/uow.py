from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.connections import Connections

from ..uow import Uow
from .repositories import SqlAlchemyBoardRepository


def session_factory_builder(engine: AsyncEngine, **kwargs):
    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        isolation_level="REPEATABLE READ",
        **kwargs,
    )

class SqlAlchemyUow(Uow):
    session: AsyncSession
    exampleRepository: SqlAlchemyBoardRepository

    def __init__(self, **kwargs):
        self.session_factory = session_factory_builder(Connections.db.engine, **kwargs)

    async def __aenter__(self):
        async with self.session_factory() as session:
            async with session.begin():
                self.session = session
                self.exampleRepository = SqlAlchemyBoardRepository(session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        # if nothing to rollback, nothing will happen
        await self.session.rollback()

    async def close(self):
        await self.session.close()

    async def execute(self, query: str):
        records = await self.session.execute(query)
        return records.scalars().all()