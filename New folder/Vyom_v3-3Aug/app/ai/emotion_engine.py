"""
Sprint 54
Emotion Engine
"""

from __future__ import annotations


class EmotionEngine:

    def evaluate(

        self,

        market_change: float,

        vix: float,

        breadth: float,

        momentum: float,

        news_sentiment: float,

    ) -> dict:

        fear = max(

            0,

            min(

                100,

                int(

                    (vix * 4)

                    + max(

                        0,

                        -market_change * 15,

                    )

                ),

            ),

        )

        greed = max(

            0,

            min(

                100,

                int(

                    momentum * 10

                    + max(

                        0,

                        market_change * 15,

                    )

                ),

            ),

        )

        fomo = max(

            0,

            min(

                100,

                int(

                    greed * 0.6

                    + momentum * 4,

                ),

            ),

        )

        panic = max(

            0,

            min(

                100,

                int(

                    fear * 0.7

                    + vix,

                ),

            ),

        )

        emotion = max(

            0,

            min(

                100,

                int(

                    (

                        greed

                        + breadth * 100

                        + news_sentiment * 100

                        +

                        (

                            100

                            - fear

                        )

                    )

                    / 4

                ),

            ),

        )

        if emotion >= 75:

            label = "Extreme Greed"

            discipline = "High Caution"

        elif emotion >= 60:

            label = "Greed"

            discipline = "Moderate"

        elif emotion >= 40:

            label = "Neutral"

            discipline = "Normal"

        elif emotion >= 25:

            label = "Fear"

            discipline = "Be Patient"

        else:

            label = "Extreme Fear"

            discipline = "Opportunity"

        return {

            "fear": fear,

            "greed": greed,

            "fomo": fomo,

            "panic": panic,

            "breadth": round(

                breadth,

                2,

            ),

            "momentum": round(

                momentum,

                2,

            ),

            "news": round(

                news_sentiment,

                2,

            ),

            "emotion": emotion,

            "label": label,

            "discipline": discipline,

        }