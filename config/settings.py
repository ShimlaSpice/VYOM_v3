"""
Global application settings for VYOM.
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    APP_NAME: str = "VYOM"
    APP_VERSION: str = "3.0.0"
    APP_AUTHOR: str = "Vinod Sharma"

    DEBUG: bool = False

    DATABASE_URL: str = "sqlite:///database/vyom_v3.db"

    LOG_LEVEL: str = "INFO"
    LOG_DIR: Path = Path("logs")

    DATA_DIR: Path = Path("data")
    ASSETS_DIR: Path = Path("assets")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )