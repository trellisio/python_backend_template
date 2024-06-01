from nats import connect
from nats.aio.client import Client
from pydantic import Field
from pydantic_settings import BaseSettings
from redis.asyncio import Redis

from .logger import logger


class ConnectionsConfig(BaseSettings):
    # Redis
    REDIS_HOST: str = Field(description="Redis host URL", default="redis")
    REDIS_PORT: int = Field(description="Redis host port", default=6379)
    REDIS_PASSWORD: str = Field(description="Redis password", default="password")
    
    # Nats
    NATS_URL: str = Field(description="NATS connection URL", default="nats://nats:4222")


config = ConnectionsConfig()


class Connections:
    rc: Redis
    nc: Client

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
        logger.info("Connections created ⚡️")

    @classmethod
    async def close_connections(cls):
        await cls.rc.aclose()
        await cls.nc.close()
        logger.info("Connections closed ⚡️")
