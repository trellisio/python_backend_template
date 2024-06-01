from pydantic import Field
from pydantic_settings import BaseSettings
from redis.asyncio import Redis

from .logger import logger


class ConnectionsConfig(BaseSettings):
    # Redis
    REDIS_HOST: str = Field(description="Redis host URL", default="redis")
    REDIS_PORT: int = Field(description="Redis host port", default=6379)
    REDIS_PASSWORD: str = Field(description="Redis password", default="password")


config = ConnectionsConfig()


class Connections:
    rc: Redis

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
        logger.info("Connections created ⚡️")

    @classmethod
    async def close_connections(cls):
        await cls.rc.aclose()
        logger.info("Connections closed ⚡️")
