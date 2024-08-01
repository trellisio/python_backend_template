from .event import Event


class Aggregate:
    events: list[Event]

    def __init__(self):
        self.events = []

    def emit(self, event: Event):
        self.events.append(event)
