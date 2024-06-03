from app.connections import Connections

from .cache import Cache
from .cache.redis import RedisCache
from .db import Uow
from .db.sqlalchemy import SqlAlchemyUow
from .publisher import Publisher
from .publisher.nats import NatsEventPublisher


class Adapters:
    cache: Cache
    publisher: Publisher
    uow: Uow

    def __init__(self):
        self.cache = RedisCache(Connections.rc)
        self.publisher = NatsEventPublisher(Connections.nc)
        self.uoq = SqlAlchemyUow(Connections.pc)
