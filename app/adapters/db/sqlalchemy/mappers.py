from sqlalchemy.orm import registry

from app import models

from .tables import user

mapper_registry = registry()

user_mapper = mapper_registry.map_imperatively(models.User, user)