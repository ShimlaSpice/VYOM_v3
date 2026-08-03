"""
Market Repository.

Stores and retrieves market snapshots.
"""

from __future__ import annotations

from app.database.models import MarketSnapshot
from app.database.repository import Repository

_TABLE = "market_snapshots"


class MarketRepository(Repository):

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

        self.execute(

            f"CREATE INDEX IF NOT EXISTS idx_{_TABLE}_symbol "
            f"ON {_TABLE}(symbol)"

        )

        self.execute(

            f"CREATE INDEX IF NOT EXISTS idx_{_TABLE}_created "
            f"ON {_TABLE}(created_at DESC)"

        )

    def insert(

        self,

        snapshot: MarketSnapshot,

    ) -> int:

        return self._insert(

            _TABLE,

            snapshot,

        )

    def insert_many(

        self,

        snapshots: list[MarketSnapshot],

    ) -> None:

        for snapshot in snapshots:

            self.insert(

                snapshot,

            )

    def get_latest(

        self,

        limit: int = 100,

    ) -> list[MarketSnapshot]:

        rows = self.fetchall(

            f"""
            SELECT *
            FROM {_TABLE}
            ORDER BY created_at DESC
            LIMIT ?
            """,

            (

                limit,

            ),

        )

        return [

            MarketSnapshot(

                **self._row_to_kwargs(

                    row,

                )

            )

            for row in rows

        ]

    def get_symbol_history(

        self,

        symbol: str,

        limit: int | None = None,

    ) -> list[MarketSnapshot]:

        query = f"""
        SELECT *
        FROM {_TABLE}
        WHERE symbol = ?
        ORDER BY created_at DESC
        """

        params: tuple = (

            symbol,

        )

        if limit is not None:

            query += " LIMIT ?"

            params = (

                symbol,

                limit,

            )

        rows = self.fetchall(

            query,

            params,

        )

        return [

            MarketSnapshot(

                **self._row_to_kwargs(

                    row,

                )

            )

            for row in rows

        ]

    def delete_symbol(

        self,

        symbol: str,

    ) -> None:

        self.execute(

            f"DELETE FROM {_TABLE} WHERE symbol = ?",

            (

                symbol,

            ),

        )

    def clear(

        self,

    ) -> None:

        self.execute(

            f"DELETE FROM {_TABLE}"

        )