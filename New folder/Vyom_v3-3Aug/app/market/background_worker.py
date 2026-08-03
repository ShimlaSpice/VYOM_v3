"""
Background Worker
Sprint 53
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable


class BackgroundWorker:

    def __init__(self):

        self._threads: list[threading.Thread] = []

        self._running = False

    def start(self):

        self._running = True

    def stop(self):

        self._running = False

        for thread in self._threads:

            if thread.is_alive():

                thread.join(timeout=1)

        self._threads.clear()

    def submit(

        self,

        func: Callable,

        *args,

        **kwargs,

    ):

        thread = threading.Thread(

            target=func,

            args=args,

            kwargs=kwargs,

            daemon=True,

        )

        thread.start()

        self._threads.append(

            thread,

        )

        return thread

    def schedule(

        self,

        interval: float,

        func: Callable,

        *args,

        **kwargs,

    ):

        def worker():

            while self._running:

                try:

                    func(

                        *args,

                        **kwargs,

                    )

                except Exception:

                    pass

                time.sleep(

                    interval,

                )

        thread = threading.Thread(

            target=worker,

            daemon=True,

        )

        thread.start()

        self._threads.append(

            thread,

        )

        return thread

    @property
    def running(

        self,

    ):

        return self._running


background_worker = BackgroundWorker()
