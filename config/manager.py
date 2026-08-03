"""Configuration manager for VYOM."""

from __future__ import annotations

from threading import Lock

from config.settings import Settings


class ConfigManager:
    """Thread-safe singleton wrapper around application settings."""

    _instance: Settings | None = None
    _lock = Lock()

    def __init__(self) -> None:
        self._settings = self.__class__.get_settings()

    @property
    def settings(self) -> Settings:
        return self._settings

    @classmethod
    def get_settings(cls) -> Settings:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = Settings()
        return cls._instance

    @classmethod
    def reload(cls) -> Settings:
        with cls._lock:
            cls._instance = Settings()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        with cls._lock:
            cls._instance = None