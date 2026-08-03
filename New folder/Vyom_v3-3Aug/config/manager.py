"""
Configuration manager for VYOM.
"""

from __future__ import annotations

from config.settings import Settings


class ConfigManager:
    """Loads and owns a single Settings instance.

    Intended to be constructed once by the dependency-injection container
    (see core.container.ApplicationContainer) and the resulting Settings
    passed down explicitly to whatever needs it, rather than accessed as
    a global singleton from arbitrary modules.
    """

    def __init__(self) -> None:
        self.settings: Settings = Settings()