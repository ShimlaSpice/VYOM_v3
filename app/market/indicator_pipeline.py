"""
===========================================================
VYOM AI
Sprint 53

Central Indicator Pipeline

Every indicator is calculated ONLY ONCE.

Scanner
Recommendation Engine
Jarvis
Emotion Engine
Universal Search
Trade Engine

All consume this pipeline.

===========================================================
"""

from __future__ import annotations

import pandas as pd
import numpy as np


class IndicatorPipeline:

    """
    Central Indicator Engine
    """

    def __init__(self):

        pass

    # =====================================================
    # Public
    # =====================================================

    def process(self, df: pd.DataFrame) -> pd.DataFrame:

        if df is None:

            return pd.DataFrame()

        if df.empty:

            return df

        df = df.copy()

        self._ema(df)
        self._sma(df)
        self._rsi(df)
        self._atr(df)
        self._macd(df)
        self._adx(df)
        self._volume(df)
        self._momentum(df)
        self._breakout(df)

        return df

    # =====================================================
    # EMA
    # =====================================================

    def _ema(self, df):

        df["ema9"] = df["close"].ewm(span=9).mean()

        df["ema20"] = df["close"].ewm(span=20).mean()

        df["ema50"] = df["close"].ewm(span=50).mean()

        df["ema200"] = df["close"].ewm(span=200).mean()

    # =====================================================
    # SMA
    # =====================================================

    def _sma(self, df):

        df["sma20"] = df["close"].rolling(20).mean()

        df["sma50"] = df["close"].rolling(50).mean()

        df["sma100"] = df["close"].rolling(100).mean()

        df["sma200"] = df["close"].rolling(200).mean()

    # =====================================================
    # RSI
    # =====================================================

    def _rsi(self, df, period=14):

        delta = df["close"].diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(period).mean()

        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss.replace(0, np.nan)

        df["rsi"] = 100 - (100 / (1 + rs))

    # =====================================================
    # ATR
    # =====================================================

    def _atr(self, df, period=14):

        hl = df["high"] - df["low"]

        hc = (df["high"] - df["close"].shift()).abs()

        lc = (df["low"] - df["close"].shift()).abs()

        tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)

        df["atr"] = tr.rolling(period).mean()

    # =====================================================
    # MACD
    # =====================================================

    def _macd(self, df):

        ema12 = df["close"].ewm(span=12).mean()

        ema26 = df["close"].ewm(span=26).mean()

        df["macd"] = ema12 - ema26

        df["macd_signal"] = df["macd"].ewm(span=9).mean()

        df["macd_histogram"] = (

            df["macd"]

            - df["macd_signal"]

        )

    # =====================================================
    # ADX
    # =====================================================

    def _adx(self, df, period=14):

        plus_dm = df["high"].diff()

        minus_dm = -df["low"].diff()

        plus_dm[plus_dm < 0] = 0

        minus_dm[minus_dm < 0] = 0

        tr = pd.concat(

            [

                df["high"] - df["low"],

                (df["high"] - df["close"].shift()).abs(),

                (df["low"] - df["close"].shift()).abs(),

            ],

            axis=1,

        ).max(axis=1)

        atr = tr.rolling(period).mean()

        plus_di = (

            100

            * plus_dm.rolling(period).sum()

            / atr

        )

        minus_di = (

            100

            * minus_dm.rolling(period).sum()

            / atr

        )

        dx = (

            (plus_di - minus_di).abs()

            /

            (plus_di + minus_di)

        ) * 100

        df["adx"] = dx.rolling(period).mean()
    # =====================================================
    # Volume
    # =====================================================

    def _volume(self, df):

        df["volume_sma20"] = (

            df["volume"]

            .rolling(20)

            .mean()

        )

        df["volume_ratio"] = (

            df["volume"]

            /

            df["volume_sma20"]

        )

        df["high_volume"] = (

            df["volume_ratio"] > 1.5

        )

    # =====================================================
    # Momentum
    # =====================================================

    def _momentum(self, df):

        df["momentum_5"] = (

            df["close"]

            -

            df["close"].shift(5)

        )

        df["momentum_10"] = (

            df["close"]

            -

            df["close"].shift(10)

        )

        df["roc"] = (

            df["close"].pct_change(10)

            * 100

        )

    # =====================================================
    # Breakout
    # =====================================================

    def _breakout(self, df):

        df["highest20"] = (

            df["high"]

            .rolling(20)

            .max()

        )

        df["lowest20"] = (

            df["low"]

            .rolling(20)

            .min()

        )

        df["breakout_up"] = (

            df["close"]

            >=

            df["highest20"]

        )

        df["breakout_down"] = (

            df["close"]

            <=

            df["lowest20"]

        )

    # =====================================================
    # Latest Values
    # =====================================================

    def latest(self, df: pd.DataFrame) -> dict:

        if df is None or df.empty:

            return {}

        row = df.iloc[-1]

        return {

            "close": float(row["close"]),

            "ema9": float(row.get("ema9", np.nan)),

            "ema20": float(row.get("ema20", np.nan)),

            "ema50": float(row.get("ema50", np.nan)),

            "ema200": float(row.get("ema200", np.nan)),

            "sma20": float(row.get("sma20", np.nan)),

            "sma50": float(row.get("sma50", np.nan)),

            "sma100": float(row.get("sma100", np.nan)),

            "sma200": float(row.get("sma200", np.nan)),

            "rsi": float(row.get("rsi", np.nan)),

            "atr": float(row.get("atr", np.nan)),

            "macd": float(row.get("macd", np.nan)),

            "macd_signal": float(

                row.get("macd_signal", np.nan)

            ),

            "macd_histogram": float(

                row.get("macd_histogram", np.nan)

            ),

            "adx": float(row.get("adx", np.nan)),

            "volume": float(row.get("volume", np.nan)),

            "volume_ratio": float(

                row.get("volume_ratio", np.nan)

            ),

            "roc": float(row.get("roc", np.nan)),

            "momentum_5": float(

                row.get("momentum_5", np.nan)

            ),

            "momentum_10": float(

                row.get("momentum_10", np.nan)

            ),

            "breakout_up": bool(

                row.get("breakout_up", False)

            ),

            "breakout_down": bool(

                row.get("breakout_down", False)

            ),

        }


# =========================================================
# Singleton
# =========================================================

indicator_pipeline = IndicatorPipeline()