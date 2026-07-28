"""
Market Repository.
"""

from __future__ import annotations

from app.database.models import MarketSnapshot
from app.database.repository import Repository


class MarketRepository(Repository):

    def create_table(

        self,

    ) -> None:

        super().create_table(

            """
            CREATE TABLE IF NOT EXISTS market_snapshots (

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

    def insert(

        self,

        snapshot: MarketSnapshot,

    ) -> None:

        self.execute(

            """
            INSERT INTO market_snapshots (

                symbol,

                price,

                volume,

                rsi,

                macd,

                sma20,

                sma50,

                ema20,

                created_at

            )

            VALUES (

                ?, ?, ?, ?, ?, ?, ?, ?, ?

            )
            """,

            (

                snapshot.symbol,

                snapshot.price,

                snapshot.volume,

                snapshot.rsi,

                snapshot.macd,

                snapshot.sma20,

                snapshot.sma50,

                snapshot.ema20,

                snapshot.created_at,

            ),

        )

    def get_latest(

        self,

        limit: int = 100,

    ):

        return self.fetchall(

            """
            SELECT *

            FROM market_snapshots

            ORDER BY id DESC

            LIMIT ?
            """,

            (

                limit,

            ),

        )

    def get_symbol_history(

        self,

        symbol: str,

    ):

        return self.fetchall(

            """
            SELECT *

            FROM market_snapshots

            WHERE symbol = ?

            ORDER BY id DESC
            """,

            (

                symbol,

            ),

        )