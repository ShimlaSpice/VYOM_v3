"""
Dependency Injection Container for VYOM.

Owns and wires together the application's shared, long-lived services.
Every module we rebuild (market data, scanner, intelligence,
recommendation, trading, UI) receives its dependencies from this
container rather than reaching for global singletons.
"""

from __future__ import annotations

from typing import Any

from app.database import Database, Repositories, create_all_tables
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

        self.database = Database(self._database_path())
        self.repositories: Repositories = create_all_tables(self.database)

        # Services wired module-by-module as we rebuild VYOM.
        self.market_data: Any | None = None
        self.scanner: Any | None = None
        self.ai_analyst: Any | None = None
        self.paper_trader: Any | None = None
        self.dashboard: Any | None = None

    def _database_path(self) -> str:
        """Derive the SQLite file path from Settings.DATABASE_URL."""
        prefix = "sqlite:///"
        url = self.settings.DATABASE_URL
        return url[len(prefix):] if url.startswith(prefix) else url

    @property
    def logger(self):
        """Return the configured Loguru logger."""
        return self._logger_manager.logger

    def shutdown(self) -> None:
        """Release container-owned resources."""
        self.database.close()