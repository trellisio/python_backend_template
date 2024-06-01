import pytest

from app.adapters.publisher.memory import InMemoryEventPublisher


class TestInMemoryPublisher:
    publisher: InMemoryEventPublisher

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.publisher = InMemoryEventPublisher()

    @pytest.mark.asyncio
    async def test_can_publish_string_event(self):
        await self.publisher.publish("event", "test")

        assert len(self.publisher.published_messages) == 1
        assert self.publisher.published_messages[0] == {
            "channel": "event",
            "payload": "test",
        }

    @pytest.mark.asyncio
    async def test_can_publish_dict_event(self):
        payload = {"subject": "event", "field": "bar"}
        await self.publisher.publish("event", payload)

        assert len(self.publisher.published_messages) == 1
        assert self.publisher.published_messages[0] == {
            "channel": "event",
            "payload": payload,
        }
