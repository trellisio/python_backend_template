from kink import inject
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.future import select

from app.domain import models
from app.services.interfaces.uow import Uow, UserRepository, Views

from .connection import SqlConnection


@inject(alias=UserRepository)
class SqlAlchemyUserRepository(UserRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, User: models.User) -> None:
        self.session.add(User)

    async def find(self, email: str) -> list[models.User]:
        res = await self.session.execute(
            select(models.User).where(models.User.email == email)
        )
        return res.scalars().all()

    async def remove(self, email: str) -> None:
        await self.session.execute(
            delete(models.User).where(models.User.email == email)
        )

@inject(alias=Views)
class SqlAlchemyViews(Views):
    async def list_users() -> list[models.User]:
        raise NotImplementedError()

@inject(alias=Uow)
class SqlAlchemyUow(Uow):
    # repositories
    user_repository: SqlAlchemyUserRepository
    
    # views
    views: SqlAlchemyViews

    # session
    session_factory: async_sessionmaker[AsyncSession]
    session: AsyncSession

    def __init__(self, connection: SqlConnection, views: SqlAlchemyViews):
        engine = connection.engine
        self.session_factory = async_sessionmaker(
            engine,
            expire_on_commit=False,
        )
        self.views = views

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
