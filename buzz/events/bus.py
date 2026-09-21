"""Small in-process event bus; replaceable with a durable broker later."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

from buzz.events.models import BuzzEvent

EventHandler = Callable[[BuzzEvent], None]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, kind: str, handler: EventHandler) -> None:
        self._handlers[kind].append(handler)

    def publish(self, event: BuzzEvent) -> None:
        for handler in tuple(self._handlers.get(event.kind, ())):
            handler(event)
