from app.config import config

from .connection import *

# Inject specific adapters based on ENVIRONMENT
match config.ENVIRONMENT:
    case "local":
        from .cache.memory import *
        from .db.sqlalchemy import *
        from .publisher.memory import *
    case _:
        from .cache.redis import *
        from .db.sqlalchemy import *
        from .publisher.nats import *
