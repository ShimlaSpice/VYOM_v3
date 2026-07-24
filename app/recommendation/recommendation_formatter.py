"""
Recommendation Formatter.

Converts Recommendation object into
human-readable output.
"""

from __future__ import annotations

from app.recommendation.recommendation_model import Recommendation


class RecommendationFormatter:

    def format(
        self,
        recommendation: Recommendation,
    ) -> str:

        lines = []

        lines.append("=" * 70)
        lines.append(f"{recommendation.symbol}")
        lines.append("=" * 70)

        lines.append(
            f"Recommendation : {recommendation.recommendation}"
        )

        lines.append(
            f"Category       : {recommendation.category}"
        )

        lines.append(
            f"Confidence     : {recommendation.confidence}%"
        )

        lines.append("")

        lines.append(
            f"Entry          : ₹{recommendation.entry:.2f}"
        )

        lines.append(
            f"Stop Loss      : ₹{recommendation.stop_loss:.2f}"
        )

        lines.append(
            f"Target 1       : ₹{recommendation.target1:.2f}"
        )

        lines.append(
            f"Target 2       : ₹{recommendation.target2:.2f}"
        )

        lines.append(
            f"Risk Reward    : 1:{recommendation.risk_reward}"
        )

        lines.append(
            f"Risk Level     : {recommendation.risk_level}"
        )

        lines.append("")
        lines.append("-" * 70)
        lines.append("SCORE BREAKDOWN")
        lines.append("-" * 70)

        for key, value in recommendation.scores.items():

            lines.append(
                f"{key.title():20} : {value}"
            )

        lines.append("")
        lines.append("-" * 70)
        lines.append("REASONS")
        lines.append("-" * 70)

        for reason in recommendation.reasons:

            lines.append(f"✓ {reason}")

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)