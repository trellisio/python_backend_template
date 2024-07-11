from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain import models
from app.services.adapters import Query

from .connection import SqlConnection


class SqlAlchemyQuery(Query):
    session_factory: async_sessionmaker[AsyncSession]
    session: AsyncSession

    def __init__(self, connection: SqlConnection):
        engine = connection.read_engine
        self.session_factory = async_sessionmaker(
            engine,
            expire_on_commit=False,
        )

    async def list_users(self) -> list[models.User]:
        async with self.session_factory() as session:
            res = await session.execute("SELECT * from user")
            return res.scalars().all()
