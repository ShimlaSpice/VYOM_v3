"""
Recommendation Repository.
"""

from __future__ import annotations

from app.database.models import RecommendationRecord
from app.database.repository import Repository


class RecommendationRepository(Repository):

    def create_table(

        self,

    ) -> None:

        super().create_table(

            """
            CREATE TABLE IF NOT EXISTS recommendations (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT NOT NULL,

                recommendation TEXT NOT NULL,

                category TEXT NOT NULL,

                confidence INTEGER NOT NULL,

                entry REAL,

                stop_loss REAL,

                target1 REAL,

                target2 REAL,

                risk_reward REAL,

                created_at TEXT NOT NULL

            )
            """

        )

    def insert(

        self,

        recommendation: RecommendationRecord,

    ) -> None:

        self.execute(

            """
            INSERT INTO recommendations (

                symbol,

                recommendation,

                category,

                confidence,

                entry,

                stop_loss,

                target1,

                target2,

                risk_reward,

                created_at

            )

            VALUES (

                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?

            )
            """,

            (

                recommendation.symbol,

                recommendation.recommendation,

                recommendation.category,

                recommendation.confidence,

                recommendation.entry,

                recommendation.stop_loss,

                recommendation.target1,

                recommendation.target2,

                recommendation.risk_reward,

                recommendation.created_at,

            ),

        )

    def get_latest(

        self,

        limit: int = 10,

    ):

        return self.fetchall(

            """
            SELECT *

            FROM recommendations

            ORDER BY id DESC

            LIMIT ?
            """,

            (

                limit,

            ),

        )

    def get_by_symbol(

        self,

        symbol: str,

    ):

        return self.fetchall(

            """
            SELECT *

            FROM recommendations

            WHERE symbol = ?

            ORDER BY id DESC
            """,

            (

                symbol,

            ),

        )