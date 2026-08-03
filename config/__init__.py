"""VYOM configuration package."""

from __future__ import annotations

from config.manager import ConfigManager
from config.settings import Settings

settings = ConfigManager().settings

__all__ = [
    "ConfigManager",
    "Settings",
    "settings",
]