from abc import abstractmethod

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine

from ..connection import Connection


class SqlConnection(Connection):
    engine: AsyncEngine
    metadata: MetaData

    @abstractmethod
    async def apply_migrations(self):
        raise NotImplementedError()
