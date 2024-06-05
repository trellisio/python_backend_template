import pytest

from app.adapters import Connections
from app.adapters.publisher.nats import NatsEventPublisher


class TestNatsPublisher:
    publisher: NatsEventPublisher

    @pytest.fixture(autouse=True)
    def set_up(self, connections: Connections):
        self.publisher = NatsEventPublisher(connections.nc)

    async def test_can_publish_string_event(self):
        await self.publisher.publish("event", "test")

    async def test_can_publish_dict_event(self):
        payload = {"subject": "event", "field": "bar"}
        await self.publisher.publish("event", payload)
