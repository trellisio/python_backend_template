from kink import inject
from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy.engine.interfaces import IsolationLevel

from .connection import Connection


class SqlConnectionConfig(BaseSettings):
    DB_URL: str = Field(
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
class SqlConnection(Connection):
    pass