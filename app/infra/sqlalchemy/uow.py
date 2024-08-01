from kink import inject
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.future import select

from app.domain import models
from app.services.adapters.uow import Uow, UserRepository

from .connection import SqlConnection


class SqlAlchemyUserRepository(UserRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, User: models.User):
        self.session.add(User)

    async def find(self, email: str) -> list[models.User]:
        res = await self.session.execute(
            select(models.User).where(models.User.email == email)
        )
        return res.scalars().all()

    async def remove(self, email: str) -> list[models.User]:
        return await self.session.execute(
            delete(models.User).where(models.User.email == email)
        )


@inject(alias=Uow)
class SqlAlchemyUow(Uow):
    # repositories
    user_repository: SqlAlchemyUserRepository

    # session
    session_factory: async_sessionmaker[AsyncSession]
    session: AsyncSession

    def __init__(self, connection: SqlConnection):
        engine = connection.update_engine
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
