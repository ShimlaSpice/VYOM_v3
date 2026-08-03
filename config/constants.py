"""
Application-wide constants for VYOM.
"""

from __future__ import annotations

from enum import Enum


class Environment(str, Enum):

    DEVELOPMENT = "development"

    TESTING = "testing"

    PRODUCTION = "production"


class Exchange(str, Enum):

    NSE = "NSE"

    BSE = "BSE"


class MarketStatus(str, Enum):

    PRE_OPEN = "PRE_OPEN"

    OPEN = "OPEN"

    CLOSED = "CLOSED"

    POST_CLOSE = "POST_CLOSE"


APP_NAME = "VYOM"

APP_VERSION = "3.0.0"

DEFAULT_TIMEZONE = "Asia/Kolkata"

DEFAULT_CURRENCY = "INR"

DEFAULT_MARKET = Exchange.NSE

MARKET_OPEN_TIME = "09:15"

MARKET_CLOSE_TIME = "15:30"

DATABASE_NAME = "vyom_v3.db"

LOG_FILE_NAME = "vyom_v3.log"

DEFAULT_SCAN_LIMIT = 10

DEFAULT_CANDLE_LIMIT = 100

DEFAULT_HISTORY_PERIOD = "6mo"

DEFAULT_INTERVAL = "1d"

MAX_SCAN_WORKERS = 12

MAX_PIPELINE_WORKERS = 8