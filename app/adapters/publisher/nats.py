import json

from kink import di, inject
from nats import connect
from nats.aio.client import Client
from pydantic import Field
from pydantic_settings import BaseSettings

from app.logger import logger

from ..connection import Connection
from .publisher import Payload, Publisher


class NatsConnectionConfig(BaseSettings):
    NATS_URL: str = Field(description="NATS connection URL", default="nats://nats:4222")


@inject(alias=Connection)
class NatsConnection(Connection):
    nc: Client

    async def connect(self):
        config = NatsConnectionConfig()
        nc = await connect(config.NATS_URL)

        self.nc = nc
        di[Client] = nc

        logger.info("Nats connected 🚨")

    async def close(self, cleanup: bool = False):
        await self.nc.close()


@inject(alias=Publisher)
class NatsEventPublisher(Publisher):
    nc: Client

    def __init__(self, nc: Client):
        self.nc = nc

    async def publish(self, channel: str, payload: Payload):
        # if payload is dict, turn to string and decode
        if isinstance(payload, dict):
            payload = json.dumps(payload)  # turn to string

        await self.nc.publish(channel, payload.encode())
