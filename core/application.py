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

        logger = self.container.logger

        settings = self.container.settings

        logger.info("=" * 60)

        logger.info(

            f"Starting {settings.APP_NAME} v{settings.APP_VERSION}"

        )

        logger.info("=" * 60)

        logger.success("Application initialized.")

    def shutdown(self) -> None:

        logger = self.container.logger

        logger.info("Shutting down application...")

        try:

            self.container.events.clear()

        except Exception:

            logger.exception("Failed to clear events.")

        logger.success("Application stopped.")