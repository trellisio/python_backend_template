from alembic import command
from alembic.config import Config
from kink import di, inject
from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy.engine.interfaces import IsolationLevel
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from app.logger import logger

from ...connection import Connection
from ..uow import Uow
from .repositories import SqlAlchemyUserRepository


class PostgresConnectionConfig(BaseSettings):
    POSTGRES_URL: str = Field(
        description="URL to connect to Postgres",
        default="postgresql+asyncpg://user:password@postgres:5432/service_name",
    )
    POSTGRES_ISOLATION_LEVEL: IsolationLevel = Field(
        description="DB transaction isolation level", default="REPEATABLE READ"
    )
    DB_ECHO: bool = Field(
        description="Boolean for DB to echo operations", default=False
    )


@inject(alias=Connection)
class PostgresConnection(Connection):
    pc: AsyncEngine
    
    async def connect(self):
        config = PostgresConnectionConfig()
        pc = create_async_engine(config.POSTGRES_URL, future=True, echo=config.DB_ECHO)
        pc.execution_options(isolation_level=config.POSTGRES_ISOLATION_LEVEL)
        
        self.pc = pc
        di[AsyncEngine] = pc

        # Apply migrations on connection
        # def run_upgrade( connection, cfg):
        #     cfg.attributes["connection"] = connection
        #     command.upgrade(cfg, "head")

        # async with pc.begin() as conn:
        #     await conn.run_sync(run_upgrade, Config("alembic.ini"))
        
        logger.info("Postgres connected 🚨")
    
    async def close(self):
        await self.pc.dispose()


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
