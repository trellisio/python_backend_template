from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine

from ..connection import Connection


class SqlConnection(Connection):
    engine: AsyncEngine
    metadata: MetaData
