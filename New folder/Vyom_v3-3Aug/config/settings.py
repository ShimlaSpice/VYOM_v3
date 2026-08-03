"""
Global application settings for VYOM.

Loaded from environment variables / .env, with typed, sensible defaults.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.constants import APP_NAME, APP_VERSION, DATABASE_NAME, Environment


class Settings(BaseSettings):
    """Application configuration."""

    APP_NAME: str = APP_NAME
    APP_VERSION: str = APP_VERSION
    APP_AUTHOR: str = "Vinod Sharma"

    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = False

    DATA_DIR: Path = Path("data")
    ASSETS_DIR: Path = Path("assets")
    LOG_DIR: Path = Path("logs")

    DATABASE_URL: str = Field(
        default=f"sqlite:///data/{DATABASE_NAME}",
        description="SQLAlchemy-style database URL. Defaults to a file under DATA_DIR.",
    )

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        """True when running in the PRODUCTION environment."""
        return self.ENVIRONMENT is Environment.PRODUCTION