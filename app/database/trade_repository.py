"""
Trade Repository — persists paper/live trade records.
"""

from __future__ import annotations

from app.database.models import TradeRecord
from app.database.repository import Repository

_TABLE = "trades"


class TradeRepository(Repository):
    """Persists and queries TradeRecord records."""

    def create_table(self) -> None:
        super().create_table(
            f"""
            CREATE TABLE IF NOT EXISTS {_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                entry_price REAL NOT NULL,
                exit_price REAL,
                pnl REAL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

    def insert(self, trade: TradeRecord) -> int:
        """Persist a trade and return its new row id."""
        return self._insert(_TABLE, trade)

    def update_trade(
        self,
        trade_id: int,
        exit_price: float,
        pnl: float,
        status: str = "CLOSED",
    ) -> None:
        self.execute(
            f"""
            UPDATE {_TABLE}
            SET exit_price = ?, pnl = ?, status = ?
            WHERE id = ?
            """,
            (exit_price, pnl, status, trade_id),
        )

    def get_open_trades(self) -> list[TradeRecord]:
        rows = self.fetchall(
            f"SELECT * FROM {_TABLE} WHERE status = 'OPEN' ORDER BY id DESC"
        )
        return [TradeRecord(**self._row_to_kwargs(r)) for r in rows]

    def get_closed_trades(self) -> list[TradeRecord]:
        rows = self.fetchall(
            f"SELECT * FROM {_TABLE} WHERE status = 'CLOSED' ORDER BY id DESC"
        )
        return [TradeRecord(**self._row_to_kwargs(r)) for r in rows]

    def get_by_symbol(self, symbol: str) -> list[TradeRecord]:
        rows = self.fetchall(
            f"SELECT * FROM {_TABLE} WHERE symbol = ? ORDER BY id DESC",
            (symbol,),
        )
        return [TradeRecord(**self._row_to_kwargs(r)) for r in rows]