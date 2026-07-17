"""
Main application controller for VYOM.
"""

from loguru import logger

from config import ConfigManager
from core.logger import LoggerManager


class Application:
    """Main application lifecycle controller."""

    def __init__(self) -> None:
        self.settings = ConfigManager.get_settings()

    def initialize(self) -> None:
        """Initialize all core components."""

        LoggerManager.configure()

        logger.info("=" * 60)
        logger.info(f"Starting {self.settings.APP_NAME} v{self.settings.APP_VERSION}")
        logger.info("=" * 60)

        logger.info("Configuration loaded.")
        logger.info("Logging initialized.")

    def run(self) -> None:
        """Run the application."""

        self.initialize()

        logger.success("Application started successfully.")

        # UI startup will be added here.
        # Scheduler will be added here.
        # Database initialization will be added here.

    def shutdown(self) -> None:
        """Gracefully shut down the application."""

        logger.info("Shutting down application...")
        logger.success("Application stopped.")