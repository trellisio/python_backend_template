import pytest
from kink import di

from app.adapters import Connections


@pytest.fixture()
async def connections():
    connections: Connections = di[Connections]
    await connections.create_connections()
    yield connections
    await connections.close_connections(destroy=True)
