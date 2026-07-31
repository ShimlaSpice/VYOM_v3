"""
Market Repository — persists point-in-time market/indicator snapshots.
"""

from __future__ import annotations

from app.database.models import MarketSnapshot
from app.database.repository import Repository

_TABLE = "market_snapshots"


class MarketRepository(Repository):
    """Persists and queries MarketSnapshot records."""

    def create_table(self) -> None:
        super().create_table(
            f"""
            CREATE TABLE IF NOT EXISTS {_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                volume INTEGER NOT NULL,
                rsi REAL,
                macd REAL,
                sma20 REAL,
                sma50 REAL,
                ema20 REAL,
                created_at TEXT NOT NULL
            )
            """
        )

    def insert(self, snapshot: MarketSnapshot) -> int:
        """Persist a snapshot and return its new row id."""
        return self._insert(_TABLE, snapshot)

    def get_latest(self, limit: int = 100) -> list[MarketSnapshot]:
        rows = self.fetchall(
            f"SELECT * FROM {_TABLE} ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return [MarketSnapshot(**self._row_to_kwargs(r)) for r in rows]

    def get_symbol_history(self, symbol: str) -> list[MarketSnapshot]:
        rows = self.fetchall(
            f"SELECT * FROM {_TABLE} WHERE symbol = ? ORDER BY id DESC",
            (symbol,),
        )
        return [MarketSnapshot(**self._row_to_kwargs(r)) for r in rows]