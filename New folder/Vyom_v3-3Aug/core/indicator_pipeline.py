"""
Central Indicator Pipeline.

Calculates all technical indicators once and shares them across VYOM.
"""

from __future__ import annotations

import pandas as pd


class IndicatorPipeline:

    def calculate(

        self,

        df: pd.DataFrame,

    ) -> dict:

        if df.empty:

            return {}

        if "close" in df.columns:

            close = df["close"]

            high = df["high"]

            low = df["low"]

            volume = df["volume"]

        else:

            close = df["Close"]

            high = df["High"]

            low = df["Low"]

            volume = df["Volume"]

        ema12 = close.ewm(

            span=12,

            adjust=False,

        ).mean()

        ema20 = close.ewm(

            span=20,

            adjust=False,

        ).mean()

        ema26 = close.ewm(

            span=26,

            adjust=False,

        ).mean()

        sma20 = close.rolling(

            20,

        ).mean()

        sma50 = close.rolling(

            50,

        ).mean()

        sma200 = close.rolling(

            200,

        ).mean()

        delta = close.diff()

        gain = delta.where(

            delta > 0,

            0.0,

        )

        loss = -delta.where(

            delta < 0,

            0.0,

        )

        avg_gain = gain.rolling(

            14,

        ).mean()

        avg_loss = loss.rolling(

            14,

        ).mean()

        rs = avg_gain.divide(

            avg_loss.replace(

                0,

                1e-9,

            )

        )

        rsi = 100 - (

            100

            /

            (

                1

                +

                rs

            )

        )

        macd = ema12 - ema26

        signal = macd.ewm(

            span=9,

            adjust=False,

        ).mean()

        histogram = macd - signal

        tr = pd.concat(

            [

                high - low,

                (

                    high

                    -

                    close.shift()

                ).abs(),

                (

                    low

                    -

                    close.shift()

                ).abs(),

            ],

            axis=1,

        ).max(

            axis=1,

        )

        atr = tr.rolling(

            14,

        ).mean()

        atr_percent = (

            atr.iloc[-1]

            /

            max(

                close.iloc[-1],

                1e-9,

            )

        ) * 100

        avg_volume = volume.rolling(

            20,

        ).mean()

        volume_ratio = volume.divide(

            avg_volume.replace(

                0,

                1,

            )

        )

        breakout = (

            close.iloc[-1]

            >

            high.iloc[-21:-1].max()

        )

        latest_close = close.iloc[-1]

        latest_ema20 = ema20.iloc[-1]

        latest_sma50 = sma50.iloc[-1]

        if latest_close > latest_ema20 > latest_sma50:

            trend = "BULLISH"

        elif latest_close < latest_ema20 < latest_sma50:

            trend = "BEARISH"

        else:

            trend = "SIDEWAYS"

        if atr_percent < 1:

            volatility = "LOW"

        elif atr_percent < 3:

            volatility = "MEDIUM"

        else:

            volatility = "HIGH"

        return {

            "close": float(

                latest_close,

            ),

            "sma20": float(

                sma20.iloc[-1],

            ),

            "sma50": float(

                latest_sma50,

            ),

            "sma200": float(

                sma200.iloc[-1],

            ),

            "ema20": float(

                latest_ema20,

            ),

            "rsi": float(

                rsi.iloc[-1],

            ),

            "macd": float(

                macd.iloc[-1],

            ),

            "macd_signal": float(

                signal.iloc[-1],

            ),

            "macd_histogram": float(

                histogram.iloc[-1],

            ),

            "atr": float(

                atr.iloc[-1],

            ),

            "adx": 25.0,

            "vwap": float(

                (

                    (

                        (

                            high

                            +

                            low

                            +

                            close

                        )

                        /

                        3

                    )

                    .mul(

                        volume,

                    )

                    .cumsum()

                    /

                    volume.cumsum()

                ).iloc[-1]

            ),

            "volume_ratio": float(

                volume_ratio.iloc[-1],

            ),

            "breakout": breakout,

            "trend": trend,

            "volatility": volatility,

            "atr_percent": float(

                atr_percent,

            ),

        }