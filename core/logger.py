"""
Central logging configuration for VYOM.
"""

from pathlib import Path

from loguru import logger

from config import ConfigManager
from config.constants import LOG_FILE_NAME


class LoggerManager:
    """Central Loguru logger configuration."""

    _configured = False

    @classmethod
    def configure(cls) -> None:
        """Configure Loguru once."""
        if cls._configured:
            return

        settings = ConfigManager.get_settings()

        log_dir: Path = settings.LOG_DIR
        log_dir.mkdir(parents=True, exist_ok=True)

        logger.remove()

        # Console logging
        logger.add(
            sink=lambda msg: print(msg, end=""),
            level=settings.LOG_LEVEL,
            colorize=True,
            backtrace=True,
            diagnose=False,
        )

        # File logging
        logger.add(
            log_dir / LOG_FILE_NAME,
            level=settings.LOG_LEVEL,
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            enqueue=True,
            encoding="utf-8",
            backtrace=True,
            diagnose=False,
        )

        cls._configured = True

    @staticmethod
    def get_logger():
        """Return the configured logger."""
        if not LoggerManager._configured:
            LoggerManager.configure()
        return logger