from app.connections import Connections

from .cache import Cache
from .cache.redis import RedisCache
from .publisher import Publisher
from .publisher.nats import NatsEventPublisher


class Adapters:
    cache: Cache
    publisher: Publisher

    def __init__(self):
        self.cache = RedisCache(Connections.rc)
        self.publisher = NatsEventPublisher(Connections.nc)
