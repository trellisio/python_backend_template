from kink import inject
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.future import select

from app import models
from app.services.interfaces.uow import Uow, UserRepository

from .connection import SqlConnection


@inject(alias=UserRepository)
class SqlAlchemyUserRepository(UserRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, User: models.User) -> None:
        self.session.add(User)

    async def find(self, email: str) -> models.User:
        res = await self.session.execute(
            select(models.User).where(models.User.email == email).limit(1)
        )
        return res.scalars().first()

    async def remove(self, email: str) -> None:
        await self.session.execute(
            delete(models.User).where(models.User.email == email)
        )

    async def list(self) -> list[models.User]:
        res = await self.session.execute(select(models.User))
        return res.scalars().all()


@inject(alias=Uow)
class SqlAlchemyUow(Uow):
    # repositories
    user_repository: SqlAlchemyUserRepository

    # session
    session_factory: async_sessionmaker[AsyncSession]
    session: AsyncSession

    def __init__(self, connection: SqlConnection):
        engine = connection.engine
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
