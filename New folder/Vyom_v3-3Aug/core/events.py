"""
Event Bus for VYOM.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable


EventHandler = Callable[[Any], None]


class EventBus:
    """
    Simple publish/subscribe event system.
    """

    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(
        self,
        event: str,
        handler: EventHandler,
    ) -> None:
        self._subscribers[event].append(handler)

    def publish(
        self,
        event: str,
        payload: Any = None,
    ) -> None:
        for handler in self._subscribers.get(event, []):
            handler(payload)

    def clear(self) -> None:
        self._subscribers.clear()