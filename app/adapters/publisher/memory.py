from eventemitter import EventEmitter

from .publisher import Payload, Publisher


class InMemoryEventPublisher(Publisher, EventEmitter):
    async def publish(
        self, channel: str, payload: Payload
    ):
        self.emit(channel, payload)