"""
Dependency Injection Container for VYOM.
"""

from __future__ import annotations

from config.manager import ConfigManager
from core.logger import LoggerManager
from core.events import EventBus

class ApplicationContainer:
    """
    Central dependency container.

    Creates and owns all shared services.
    """

    def __init__(self) -> None:
        self._config = ConfigManager()
        self._settings = self._config.settings

        self._logger = LoggerManager(self._settings)
        self._logger.configure()
        self.events = EventBus()    
        # Services (Sprint 2 placeholders)
        self.scanner = None
        self.market_data = None
        self.ai_analyst = None
        self.paper_trader = None
        self.dashboard = None

    @property
    def settings(self):
        return self._settings

    @property
    def logger(self):
        return self._logger.logger