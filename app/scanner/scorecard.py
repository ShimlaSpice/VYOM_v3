"""
Weighted Scoring Engine.
"""

from __future__ import annotations


class ScoreCard:

    WEIGHTS = {

        "sma20": 8,

        "sma50": 10,

        "ema20": 8,

        "rsi": 12,

        "macd": 15,

        "relative_strength": 15,

        "volume": 10,

        "breakout": 12,

        "risk": 10,

    }

    def __init__(self):

        self.score = 0

        self.max_score = sum(

            self.WEIGHTS.values()

        )

        self.reasons: list[str] = []

    def add(

        self,

        category: str,

        passed: bool,

        reason: str,

    ):

        if not passed:

            return

        self.score += self.WEIGHTS.get(

            category,

            0,

        )

        self.reasons.append(

            reason,

        )

    @property
    def total(

        self,

    ) -> int:

        return self.score

    @property
    def percentage(

        self,

    ) -> float:

        if self.max_score == 0:

            return 0.0

        return round(

            (self.score / self.max_score) * 100,

            2,

        )