from kink import inject
from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy.engine.interfaces import IsolationLevel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.logger import logger

from .connection import Connection


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

        # Apply migrations on connection
        # def run_upgrade( connection, cfg):
        #     cfg.attributes["connection"] = connection
        #     command.upgrade(cfg, "head")

        # async with pc.begin() as conn:
        #     await conn.run_sync(run_upgrade, Config("alembic.ini"))

        logger.info("Postgres connected 🚨")

    async def close(self, cleanup: bool = False):
        await self.pc.dispose()
