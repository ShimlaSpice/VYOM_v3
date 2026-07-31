"""
Central logging configuration for VYOM.
"""

from __future__ import annotations

from pathlib import Path

from loguru import logger as _loguru_logger

from config.constants import LOG_FILE_NAME
from config.settings import Settings


class LoggerManager:
    """Configures and owns a Loguru logger for the application.

    Receives Settings via constructor injection instead of reaching for a
    global config singleton, so it can be wired and tested independently.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._configured = False

    def configure(self) -> None:
        """Configure Loguru sinks (console + rotating file). Idempotent."""
        if self._configured:
            return

        log_dir: Path = self._settings.LOG_DIR
        log_dir.mkdir(parents=True, exist_ok=True)

        _loguru_logger.remove()

        # Console sink
        _loguru_logger.add(
            sink=lambda msg: print(msg, end=""),
            level=self._settings.LOG_LEVEL,
            colorize=True,
            backtrace=True,
            diagnose=False,
        )

        # Rotating file sink
        _loguru_logger.add(
            log_dir / LOG_FILE_NAME,
            level=self._settings.LOG_LEVEL,
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            enqueue=True,
            encoding="utf-8",
            backtrace=True,
            diagnose=False,
        )

        self._configured = True

    @property
    def logger(self):
        """Return the configured Loguru logger, configuring it if needed."""
        if not self._configured:
            self.configure()
        return _loguru_logger