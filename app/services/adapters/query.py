from abc import ABC, abstractmethod


class Query(ABC):
    @abstractmethod
    async def list_users() -> list[str]:
        raise NotImplementedError()
