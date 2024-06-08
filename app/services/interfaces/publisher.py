from abc import ABC, abstractmethod
from typing import Any

Payload = dict[str, Any] | str


class Publisher(ABC):
    @abstractmethod
    async def publish(self, channel: str, payload: Payload):
        raise NotImplementedError()
