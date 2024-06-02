from sqlalchemy.orm import registry

from app import models

from .tables import board

mapper_registry = registry()

example_mapper = mapper_registry.map_imperatively(models.Board, board)