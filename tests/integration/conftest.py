import pytest

from app.connections import Connections


@pytest.fixture()
async def connections():
    await Connections.create_connections()
    yield Connections
    await Connections.close_connections()
