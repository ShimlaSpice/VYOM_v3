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

        close = df["Close"]
        high = df["High"]
        low = df["Low"]
        volume = df["Volume"]

        # -----------------------------
        # Moving Averages
        # -----------------------------
        sma20 = close.rolling(20).mean()
        sma50 = close.rolling(50).mean()
        sma200 = close.rolling(200).mean()

        ema20 = close.ewm(
            span=20,
            adjust=False,
        ).mean()

        # -----------------------------
        # RSI
        # -----------------------------
        delta = close.diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(14).mean()

        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss.replace(0, 1e-9)

        rsi = 100 - (100 / (1 + rs))

        # -----------------------------
        # MACD
        # -----------------------------
        ema12 = close.ewm(
            span=12,
            adjust=False,
        ).mean()

        ema26 = close.ewm(
            span=26,
            adjust=False,
        ).mean()

        macd = ema12 - ema26

        signal = macd.ewm(
            span=9,
            adjust=False,
        ).mean()

        histogram = macd - signal

        # -----------------------------
        # ATR
        # -----------------------------
        tr = pd.concat(
            [
                high - low,
                (high - close.shift()).abs(),
                (low - close.shift()).abs(),
            ],
            axis=1,
        ).max(axis=1)

        atr = tr.rolling(14).mean()

        # -----------------------------
        # ADX
        # -----------------------------
        plus_dm = high.diff()

        minus_dm = -low.diff()

        plus_dm[plus_dm < 0] = 0

        minus_dm[minus_dm < 0] = 0

        atr_safe = atr.replace(0, 1e-9)

        plus_di = (
            100
            * plus_dm.rolling(14).mean()
            / atr_safe
        )

        minus_di = (
            100
            * minus_dm.rolling(14).mean()
            / atr_safe
        )

        dx = (
            (plus_di - minus_di).abs()
            / (plus_di + minus_di).replace(
                0,
                1e-9,
            )
        ) * 100

        adx = dx.rolling(14).mean()

        # -----------------------------
        # VWAP
        # -----------------------------
        typical = (
            high
            + low
            + close
        ) / 3

        vwap = (
            (typical * volume).cumsum()
            / volume.cumsum()
        )

        # -----------------------------
        # Volume Ratio
        # -----------------------------
        avg_volume = volume.rolling(20).mean()

        volume_ratio = (
            volume
            / avg_volume.replace(
                0,
                1,
            )
        )

        # -----------------------------
        # Breakout
        # -----------------------------
        breakout = (
            close.iloc[-1]
            > high.iloc[-21:-1].max()
        )

        # -----------------------------
        # Trend
        # -----------------------------
        if (
            close.iloc[-1]
            > ema20.iloc[-1]
            > sma50.iloc[-1]
        ):
            trend = "BULLISH"

        elif (
            close.iloc[-1]
            < ema20.iloc[-1]
            < sma50.iloc[-1]
        ):
            trend = "BEARISH"

        else:
            trend = "SIDEWAYS"

        # -----------------------------
        # Volatility
        # -----------------------------
        atr_percent = (
            atr.iloc[-1]
            / close.iloc[-1]
        ) * 100

        if atr_percent < 1:
            volatility = "LOW"

        elif atr_percent < 3:
            volatility = "MEDIUM"

        else:
            volatility = "HIGH"

        return {

            "close": float(close.iloc[-1]),

            "sma20": float(sma20.iloc[-1]),

            "sma50": float(sma50.iloc[-1]),

            "sma200": float(sma200.iloc[-1]),

            "ema20": float(ema20.iloc[-1]),

            "rsi": float(rsi.iloc[-1]),

            "macd": float(macd.iloc[-1]),

            "macd_signal": float(signal.iloc[-1]),

            "macd_histogram": float(histogram.iloc[-1]),

            "atr": float(atr.iloc[-1]),

            "adx": float(adx.iloc[-1]),

            "vwap": float(vwap.iloc[-1]),

            "volume_ratio": float(
                volume_ratio.iloc[-1]
            ),

            "breakout": breakout,

            "trend": trend,

            "volatility": volatility,

            "atr_percent": float(
                atr_percent
            ),
        }