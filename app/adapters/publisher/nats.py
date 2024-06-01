import json

from nats.aio.client import Client

from .publisher import Payload, Publisher


class NatsEventPublisher(Publisher):
    nc: Client

    def __init__(self, nc: Client):
        self.nc = nc

    async def publish(self, channel: str, payload: Payload):
        # if payload is dict, turn to string and decode
        if isinstance(payload, dict):
            payload = json.dumps(payload)  # turn to string

        await self.nc.publish(channel, payload.encode())
