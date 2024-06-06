from kink import inject
from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import MetaData
from sqlalchemy.engine.interfaces import IsolationLevel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.logger import logger

from ..connection import Connection
from .sql import SqlConnection


class SqliteConnectionConfig(BaseSettings):
    SQLITE_URL: str = Field(
        description="URL to connect to SQLite",
        default="sqlite+aiosqlite:///:memory:",
    )
    DB_ECHO: bool = Field(
        description="Boolean for DB to echo operations", default=False
    )
    DB_ISOLATION_LEVEL: IsolationLevel = Field(
        description="DB transaction isolation level", default="REPEATABLE READ"
    )


@inject(alias=Connection)
class SqliteConnection(SqlConnection):
    engine: AsyncEngine
    metadata: MetaData

    def __init__(self, metadata: MetaData):
        self.metadata = metadata

    async def connect(self):
        config = SqliteConnectionConfig()
        engine = create_async_engine(
            config.SQLITE_URL, future=True, echo=config.DB_ECHO
        )
        engine.execution_options(isolation_level=config.DB_ISOLATION_LEVEL)
        self.engine = engine

        logger.info("Postgres connected 🚨")

    async def close(self, cleanup: bool = False):
        await self.engine.dispose()
