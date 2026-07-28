"""
Trade Repository.
"""

from __future__ import annotations

from app.database.models import TradeRecord
from app.database.repository import Repository


class TradeRepository(Repository):

    def create_table(

        self,

    ) -> None:

        super().create_table(

            """
            CREATE TABLE IF NOT EXISTS trades (

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

    def insert(

        self,

        trade: TradeRecord,

    ) -> None:

        self.execute(

            """
            INSERT INTO trades (

                symbol,

                side,

                quantity,

                entry_price,

                exit_price,

                pnl,

                status,

                created_at

            )

            VALUES (

                ?, ?, ?, ?, ?, ?, ?, ?

            )
            """,

            (

                trade.symbol,

                trade.side,

                trade.quantity,

                trade.entry_price,

                trade.exit_price,

                trade.pnl,

                trade.status,

                trade.created_at,

            ),

        )

    def update_trade(

        self,

        trade_id: int,

        exit_price: float,

        pnl: float,

        status: str = "CLOSED",

    ) -> None:

        self.execute(

            """
            UPDATE trades

            SET

                exit_price = ?,

                pnl = ?,

                status = ?

            WHERE id = ?
            """,

            (

                exit_price,

                pnl,

                status,

                trade_id,

            ),

        )

    def get_open_trades(

        self,

    ):

        return self.fetchall(

            """
            SELECT *

            FROM trades

            WHERE status = 'OPEN'

            ORDER BY id DESC
            """

        )

    def get_closed_trades(

        self,

    ):

        return self.fetchall(

            """
            SELECT *

            FROM trades

            WHERE status = 'CLOSED'

            ORDER BY id DESC
            """

        )

    def get_by_symbol(

        self,

        symbol: str,

    ):

        return self.fetchall(

            """
            SELECT *

            FROM trades

            WHERE symbol = ?

            ORDER BY id DESC
            """,

            (

                symbol,

            ),

        )