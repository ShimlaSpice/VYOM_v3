"""
Recommendation Repository — persists generated trade recommendations.
"""

from __future__ import annotations

from app.database.models import RecommendationRecord
from app.database.repository import Repository

_TABLE = "recommendations"


class RecommendationRepository(Repository):
    """Persists and queries RecommendationRecord records."""

    def create_table(self) -> None:
        super().create_table(
            f"""
            CREATE TABLE IF NOT EXISTS {_TABLE} (
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

    def insert(self, recommendation: RecommendationRecord) -> int:
        """Persist a recommendation and return its new row id."""
        return self._insert(_TABLE, recommendation)

    def get_latest(self, limit: int = 10) -> list[RecommendationRecord]:
        rows = self.fetchall(
            f"SELECT * FROM {_TABLE} ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return [RecommendationRecord(**self._row_to_kwargs(r)) for r in rows]

    def get_by_symbol(self, symbol: str) -> list[RecommendationRecord]:
        rows = self.fetchall(
            f"SELECT * FROM {_TABLE} WHERE symbol = ? ORDER BY id DESC",
            (symbol,),
        )
        return [RecommendationRecord(**self._row_to_kwargs(r)) for r in rows]