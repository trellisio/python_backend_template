from abc import ABC, abstractmethod

from app.domain.models import User


class Query(ABC):
    @abstractmethod
    async def list_users() -> list[User]:
        raise NotImplementedError()
