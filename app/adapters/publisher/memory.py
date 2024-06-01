from typing import Mapping

from .publisher import Payload, Publisher


class InMemoryEventPublisher(Publisher):
    published_messages: list[Mapping[str, Payload]]

    def __init__(self):
        self.published_messages = []

    async def publish(self, channel: str, payload: Payload):
        self.published_messages.append({"channel": channel, "payload": payload})
