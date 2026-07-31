"""
Application lifecycle controller for VYOM.

Thin wrapper responsible for startup/shutdown sequencing around the
ApplicationContainer. main.py depends only on initialize() / shutdown().
"""

from __future__ import annotations

from core.container import ApplicationContainer


class Application:
    """Owns the ApplicationContainer and manages its lifecycle."""

    def __init__(self) -> None:
        self.container = ApplicationContainer()

    def initialize(self) -> None:
        """Log application startup. Services are already wired by the
        container's constructor; this exists to preserve main.py's
        existing initialize()/shutdown() lifecycle contract."""
        logger = self.container.logger
        settings = self.container.settings

        logger.info("=" * 60)
        logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
        logger.info("=" * 60)
        logger.success("Application initialized.")

    def shutdown(self) -> None:
        """Gracefully shut down the application."""
        self.container.logger.info("Shutting down application...")
        self.container.events.clear()
        self.container.logger.success("Application stopped.")