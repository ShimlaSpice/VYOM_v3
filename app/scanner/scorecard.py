"""
Weighted Scoring Engine.
"""

from __future__ import annotations


class ScoreCard:

    WEIGHTS = {
        "sma": 10,
        "ema": 10,
        "rsi": 15,
        "macd": 15,
        "momentum": 15,
        "volume": 10,
        "breakout": 15,
        "risk": 10,
    }

    def __init__(self):

        self.score = 0
        self.reasons: list[str] = []

    def add(
        self,
        category: str,
        passed: bool,
        reason: str,
    ):

        if passed:

            self.score += self.WEIGHTS[category]

            self.reasons.append(reason)

    @property
    def total(self):

        return self.score