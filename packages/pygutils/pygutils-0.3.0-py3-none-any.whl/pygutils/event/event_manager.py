from collections import defaultdict

from .event_listener import EventListener


class EventManager:
    def __init__(self) -> None:
        self.__listeners: dict[str, set[EventListener]] = defaultdict(set)

    @property
    def listeners(self) -> dict[str, set[EventListener]]:
        return self.__listeners

    def subscribe(self, event: str, listener: EventListener) -> None:
        if not isinstance(listener, EventListener):
            raise TypeError(
                "listener must have a public method with signature: "
                "notify(self, event: str, *args, **kwargs)"
            )

        self.__listeners[event].add(listener)

    def unsubscribe(self, event: str, listener: EventListener) -> None:
        self.__listeners[event].discard(listener)

    def notify(self, event: str, *args, **kwargs) -> None:
        for listener in self.__listeners[event]:
            listener.notify(event, *args, **kwargs)
