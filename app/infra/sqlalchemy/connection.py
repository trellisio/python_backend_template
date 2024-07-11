from os import path

from alembic import command
from alembic.config import Config
from kink import inject
from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy.engine.interfaces import IsolationLevel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.logger import logger

from ..connection import Connection
from .tables import add_model_mappings, metadata, remove_model_mappings


class SqlConnectionConfig(BaseSettings):
    DB_URL: str = Field(
        description="URL to connect to Postgres",
        default="sqlite+aiosqlite:///:memory:",
        examples=[
            "postgresql+asyncpg://user:password@postgres:5432/service_name",
            "sqlite+aiosqlite:///:memory:",
        ],
    )
    DB_ISOLATION_LEVEL: IsolationLevel = Field(
        description="DB transaction isolation level", default="REPEATABLE READ"
    )
    DB_ECHO: bool = Field(
        description="Boolean for DB to echo operations", default=False
    )


@inject(alias=Connection)
class SqlConnection(Connection):
    update_engine: AsyncEngine
    read_engine: AsyncEngine

    async def connect(self):
        config = SqlConnectionConfig()

        self.update_engine = create_async_engine(
            config.DB_URL, future=True, echo=config.DB_ECHO
        )
        self.update_engine.execution_options(isolation_level=config.DB_ISOLATION_LEVEL)

        self.read_engine = create_async_engine(
            config.DB_URL, future=True, echo=config.DB_ECHO
        )
        self.read_engine.execution_options(isolation_level="READ COMMITTED")

        await self.apply_migrations()
        add_model_mappings()

        logger.info("Database connected 🚨")

    async def close(self, cleanup: bool = False):
        if cleanup:
            async with self.update_engine.begin() as conn:
                remove_model_mappings()
                for table in metadata.sorted_tables:
                    await conn.execute(table.delete())
                    await conn.commit()

        await self.update_engine.dispose()
        await self.read_engine.dispose()

    async def apply_migrations(self):
        def run_upgrade(connection: AsyncEngine, cfg: Config):
            cfg.attributes["connection"] = connection
            command.upgrade(cfg, "head")

        async with self.update_engine.begin() as conn:
            await conn.run_sync(
                run_upgrade,
                Config(path.join("app", "infra", "sqlalchemy", "alembic.ini")),
            )
