"""
Event Bus for VYOM.
"""

from __future__ import annotations

from collections import defaultdict
from threading import RLock
from typing import Any, Callable


EventHandler = Callable[[Any], None]


class EventBus:
    """
    Thread-safe publish/subscribe event system.
    """

    def __init__(self) -> None:

        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)

        self._lock = RLock()

    def subscribe(

        self,

        event: str,

        handler: EventHandler,

    ) -> None:

        with self._lock:

            if handler not in self._subscribers[event]:

                self._subscribers[event].append(handler)

    def unsubscribe(

        self,

        event: str,

        handler: EventHandler,

    ) -> None:

        with self._lock:

            if event not in self._subscribers:

                return

            try:

                self._subscribers[event].remove(handler)

            except ValueError:

                return

            if not self._subscribers[event]:

                del self._subscribers[event]

    def publish(

        self,

        event: str,

        payload: Any = None,

    ) -> None:

        with self._lock:

            handlers = list(

                self._subscribers.get(

                    event,

                    [],

                )

            )

        for handler in handlers:

            handler(payload)

    def clear(

        self,

    ) -> None:

        with self._lock:

            self._subscribers.clear()

    def subscribers(

        self,

        event: str,

    ) -> int:

        with self._lock:

            return len(

                self._subscribers.get(

                    event,

                    [],

                )

            )