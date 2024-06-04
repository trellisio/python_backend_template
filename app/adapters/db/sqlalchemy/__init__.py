from sqlalchemy.orm import registry

from app import models

from .tables import user
from .uow import SqlAlchemyUow

# register mapping between table and domain models
mapper_registry = registry()
user_mapper = mapper_registry.map_imperatively(models.User, user)

__all__ = ["SqlAlchemyUow"]
