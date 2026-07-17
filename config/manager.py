"""
Configuration manager for VYOM.
"""

from .settings import Settings


class ConfigManager:
    """Singleton configuration manager."""

    _settings: Settings | None = None

    @classmethod
    def get_settings(cls) -> Settings:
        """Return the shared Settings instance."""
        if cls._settings is None:
            cls._settings = Settings()
        return cls._settings