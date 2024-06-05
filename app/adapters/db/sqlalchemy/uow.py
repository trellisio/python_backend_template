from kink import inject
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from ..uow import Uow
from .repositories import SqlAlchemyUserRepository


@inject(alias=Uow)
class SqlAlchemyUow(Uow):
    # repositories
    user_repository: SqlAlchemyUserRepository

    # session
    session_factory: async_sessionmaker[AsyncSession]
    session: AsyncSession

    def __init__(self, engine: AsyncEngine):
        self.session_factory = async_sessionmaker(
            engine,
            expire_on_commit=False,
        )

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
