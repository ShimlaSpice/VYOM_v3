"""
Dependency Injection Container for VYOM.

Owns and wires together the application's shared, long-lived services.
Every module we rebuild (market data, scanner, intelligence,
recommendation, trading, UI) receives its dependencies from this
container rather than reaching for global singletons. This keeps the
container as the single place that documents what VYOM is made of.
"""

from __future__ import annotations

from typing import Any

from config.manager import ConfigManager
from config.settings import Settings
from core.events import EventBus
from core.logger import LoggerManager


class ApplicationContainer:
    """Central dependency container for VYOM."""

    def __init__(self) -> None:
        self._config = ConfigManager()
        self.settings: Settings = self._config.settings

        self._logger_manager = LoggerManager(self.settings)
        self._logger_manager.configure()

        self.events = EventBus()

        # Services wired module-by-module as we rebuild VYOM. Declared
        # here (typed, unset) so this container stays authoritative on
        # the application's composition even before each service exists.
        self.market_data: Any | None = None
        self.scanner: Any | None = None
        self.ai_analyst: Any | None = None
        self.paper_trader: Any | None = None
        self.dashboard: Any | None = None

    @property
    def logger(self):
        """Return the configured Loguru logger."""
        return self._logger_manager.logger