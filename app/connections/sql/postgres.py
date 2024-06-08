from alembic import command
from alembic.config import Config
from kink import inject
from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import MetaData
from sqlalchemy.engine.interfaces import IsolationLevel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.logger import logger

from ..connection import Connection
from .sql import SqlConnection


class PostgresConnectionConfig(BaseSettings):
    POSTGRES_URL: str = Field(
        description="URL to connect to Postgres",
        default="postgresql+asyncpg://user:password@postgres:5432/service_name",
    )
    DB_ISOLATION_LEVEL: IsolationLevel = Field(
        description="DB transaction isolation level", default="REPEATABLE READ"
    )
    DB_ECHO: bool = Field(
        description="Boolean for DB to echo operations", default=False
    )


@inject(alias=Connection)
class PostgresConnection(SqlConnection):
    engine: AsyncEngine
    metadata: MetaData

    def __init__(self, metadata: MetaData):
        self.metadata = metadata

    async def connect(self):
        config = PostgresConnectionConfig()
        engine = create_async_engine(
            config.POSTGRES_URL, future=True, echo=config.DB_ECHO
        )
        engine.execution_options(isolation_level=config.DB_ISOLATION_LEVEL)
        self.engine = engine

        logger.info("Postgres connected 🚨")

    async def close(self, cleanup: bool = False):
        if cleanup:
            async with self.engine.begin() as conn:
                await conn.run_sync(self.metadata.drop_all)
                
        await self.engine.dispose()
    
    async def apply_migrations(self):
        def run_upgrade(connection: AsyncEngine, cfg: Config):
            cfg.attributes["connection"] = connection
            command.upgrade(cfg, "head")

        async with self.engine.begin() as conn:
            await conn.run_sync(run_upgrade, Config("alembic.ini"))
