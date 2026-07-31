"""
Portfolio Repository — persists current portfolio holdings.

Unlike trades/recommendations/snapshots (append-only history), a
portfolio position is one evolving row per symbol: as price or quantity
changes, we update the existing row rather than inserting a new one.
`symbol` is UNIQUE for this reason, and writes go through `upsert`.
"""

from __future__ import annotations

from app.database.models import PortfolioRecord
from app.database.repository import Repository

_TABLE = "portfolio"


class PortfolioRepository(Repository):
    """Persists and queries PortfolioRecord holdings."""

    def create_table(self) -> None:
        super().create_table(
            f"""
            CREATE TABLE IF NOT EXISTS {_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL UNIQUE,
                quantity INTEGER NOT NULL,
                average_price REAL NOT NULL,
                current_price REAL NOT NULL,
                market_value REAL NOT NULL,
                unrealized_pnl REAL NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

    def upsert(self, holding: PortfolioRecord) -> None:
        """Insert a new holding, or update the existing row for that
        symbol if one already exists."""
        self.execute(
            f"""
            INSERT INTO {_TABLE} (
                symbol, quantity, average_price, current_price,
                market_value, unrealized_pnl, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(symbol) DO UPDATE SET
                quantity = excluded.quantity,
                average_price = excluded.average_price,
                current_price = excluded.current_price,
                market_value = excluded.market_value,
                unrealized_pnl = excluded.unrealized_pnl,
                created_at = excluded.created_at
            """,
            (
                holding.symbol,
                holding.quantity,
                holding.average_price,
                holding.current_price,
                holding.market_value,
                holding.unrealized_pnl,
                holding.created_at,
            ),
        )

    def get_all(self) -> list[PortfolioRecord]:
        rows = self.fetchall(f"SELECT * FROM {_TABLE} ORDER BY symbol ASC")
        return [PortfolioRecord(**self._row_to_kwargs(r)) for r in rows]

    def get_by_symbol(self, symbol: str) -> PortfolioRecord | None:
        row = self.fetchone(f"SELECT * FROM {_TABLE} WHERE symbol = ?", (symbol,))
        return PortfolioRecord(**self._row_to_kwargs(row)) if row else None

    def remove(self, symbol: str) -> None:
        """Remove a holding entirely (e.g. position fully closed)."""
        self.execute(f"DELETE FROM {_TABLE} WHERE symbol = ?", (symbol,))