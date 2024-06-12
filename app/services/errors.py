from abc import ABC
from typing import TypedDict


class Detail(TypedDict):
    message: str
    field: str | None


class ServiceException(Exception, ABC):
    errors: list[Detail] | None

    def __init__(self, message: str, detail: list[Detail] | None = None):
        super().__init__(message)
        self.errors = detail if detail else None


class NoResourceException(ServiceException):
    def __init__(self, message: str = "Resource does not exist"):
        super().__init__(message)


class ResourceExistsException(ServiceException):
    def __init__(self, message: str = "Resource exists"):
        super().__init__(message)


class ValidationError(ServiceException):
    def __init__(
        self, detail: list[Detail], message: str = "Invalid parameters passed"
    ):
        super().__init__(message, detail)
