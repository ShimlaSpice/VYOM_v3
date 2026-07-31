"""
=============================================================
VYOM AI
Sprint 53

Background Worker Engine

Runs continuously without blocking UI.

Workers
-------
✓ Quote Refresh
✓ OHLC Refresh
✓ Scanner Refresh
✓ Recommendation Refresh

=============================================================
"""

from __future__ import annotations

import threading
import time
from typing import Callable


class BackgroundWorker:

    def __init__(self):

        self._threads = {}

        self._running = {}

        self._lock = threading.Lock()

    # ======================================================
    # Worker Loop
    # ======================================================

    def _loop(

        self,

        name: str,

        callback: Callable,

        interval: int,

    ):

        while self._running.get(name, False):

            try:

                callback()

            except Exception as e:

                print(

                    f"[BackgroundWorker] "

                    f"{name}: {e}"

                )

            time.sleep(interval)

    # ======================================================
    # Start Worker
    # ======================================================

    def start(

        self,

        name: str,

        callback: Callable,

        interval: int,

    ):

        with self._lock:

            if self._running.get(name):

                return

            self._running[name] = True

            thread = threading.Thread(

                target=self._loop,

                args=(

                    name,

                    callback,

                    interval,

                ),

                daemon=True,

            )

            thread.start()

            self._threads[name] = thread

    # ======================================================
    # Stop Worker
    # ======================================================

    def stop(

        self,

        name: str,

    ):

        with self._lock:

            self._running[name] = False

    # ======================================================
    # Restart
    # ======================================================

    def restart(

        self,

        name: str,

        callback: Callable,

        interval: int,

    ):

        self.stop(name)

        time.sleep(0.2)

        self.start(

            name,

            callback,

            interval,

        )

    # ======================================================
    # Running?
    # ======================================================

    def is_running(

        self,

        name: str,

    ) -> bool:

        return self._running.get(

            name,

            False,

        )

    # ======================================================
    # Running Workers
    # ======================================================

    def workers(self):

        return list(

            self._threads.keys()

        )
    # ======================================================
    # Stop All Workers
    # ======================================================

    def stop_all(self):

        with self._lock:

            for name in list(self._running.keys()):

                self._running[name] = False

    # ======================================================
    # Wait for Completion
    # ======================================================

    def join_all(

        self,

        timeout: float | None = None,

    ):

        for thread in self._threads.values():

            try:

                thread.join(timeout=timeout)

            except Exception:

                pass

    # ======================================================
    # Status
    # ======================================================

    def status(self) -> dict:

        result = {}

        for name in self._threads:

            thread = self._threads[name]

            result[name] = {

                "running": self._running.get(

                    name,

                    False,

                ),

                "alive": thread.is_alive(),

                "daemon": thread.daemon,

            }

        return result

    # ======================================================
    # Cleanup
    # ======================================================

    def cleanup(self):

        dead = []

        for name, thread in self._threads.items():

            if not thread.is_alive():

                dead.append(name)

        for name in dead:

            self._threads.pop(name, None)

            self._running.pop(name, None)


# ==========================================================
# Singleton
# ==========================================================

background_worker = BackgroundWorker()