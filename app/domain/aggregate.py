from .event import Event


class Aggregate:
    version: int
    events: list[Event]

    def __init__(self):
        self.version = 0
        self.events = []

    def emit(self, event: Event):
        self.events.append(event)
