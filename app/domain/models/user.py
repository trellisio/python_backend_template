from ..aggregate import Aggregate
from ..event import Event


class DomainEvent(Event):
    channel = "DomainThingHappened"

    def __init__(self, email: str):
        super().__init__(data={"email": email})


class User(Aggregate):
    email: str

    def __init__(self, email: str):
        super().__init__()
        self.email = email

    def some_domain_method(self):
        self.emit(DomainEvent(self.email))
