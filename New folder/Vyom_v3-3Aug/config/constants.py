"""
Application-wide constants for VYOM.
"""

from enum import Enum


class Environment(str, Enum):
    """Application environments."""

    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Exchange(str, Enum):
    """Supported stock exchanges."""

    NSE = "NSE"
    BSE = "BSE"


class MarketStatus(str, Enum):
    """Market states."""

    PRE_OPEN = "PRE_OPEN"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    POST_CLOSE = "POST_CLOSE"


APP_NAME = "VYOM"
APP_VERSION = "3.0.0"

DEFAULT_TIMEZONE = "Asia/Kolkata"

MARKET_OPEN_TIME = "09:15"
MARKET_CLOSE_TIME = "15:30"

DATABASE_NAME = "vyom_v3.db"

LOG_FILE_NAME = "vyom_v3.log"