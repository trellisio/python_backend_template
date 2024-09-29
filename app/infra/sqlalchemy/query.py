from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.services.ports import Query

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

    async def list_users(self) -> list[str]:
        async with self.session_factory() as session:
            res = await session.execute(text("SELECT email FROM user"))
            return [r[0] for r in res]
