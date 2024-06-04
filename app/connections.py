import os

from alembic import command
from alembic.config import Config
from nats import connect
from nats.aio.client import Client
from pydantic import Field
from pydantic_settings import BaseSettings
from redis.asyncio import Redis
from sqlalchemy.engine.interfaces import IsolationLevel
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, create_async_engine

from .logger import logger


class ConnectionsConfig(BaseSettings):
    # Redis
    REDIS_HOST: str = Field(description="Redis host URL", default="redis")
    REDIS_PORT: int = Field(description="Redis host port", default=6379)
    REDIS_PASSWORD: str = Field(description="Redis password", default="password")

    # Nats
    NATS_URL: str = Field(description="NATS connection URL", default="nats://nats:4222")

    # Postgres
    POSTGRES_URL: str = Field(
        description="URL to connect to Postgres",
        default="postgresql+asyncpg://user:password@postgres:5432/service_name",
    )
    POSTGRES_ISOLATION_LEVEL: IsolationLevel = Field(
        description="DB transaction isolation level", default="REPEATABLE READ"
    )


config = ConnectionsConfig()


class Connections:
    rc: Redis
    nc: Client
    pc: AsyncEngine

    @classmethod
    async def create_connections(cls):
        cls.rc = Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            password=config.REDIS_PASSWORD,
            protocol=3,
            db=0,
            decode_responses=True,
        )
        await cls.rc.ping()
        logger.info("Redis connected 🚨")

        cls.nc = await connect(config.NATS_URL)
        logger.info("NATS connected 🚨")

        cls.pc = create_async_engine(config.POSTGRES_URL, future=True)
        cls.pc.execution_options(isolation_level=config.POSTGRES_ISOLATION_LEVEL)
        logger.info("Postgres connected 🚨")

        async with cls.pc.begin() as conn:
            await apply_migrations(conn)
        logger.info("Migrations applied...🚨")

        logger.info("Connections created ⚡️")

    @classmethod
    async def close_connections(cls):
        await cls.rc.aclose()
        await cls.nc.close()
        await cls.pc.dispose()
        logger.info("Connections closed ⚡️")


async def apply_migrations(connection: AsyncConnection):
    path = os.path.abspath(
        os.path.join(
            os.getcwd(),
            "app",
            "adapters",
            "db",
            "sqlalchemy",
            "alembic.ini",
        )
    )

    def apply(connection: AsyncConnection, cfg: Config):
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, "head")

    await connection.run_sync(
        apply,
        Config(path),
    )
