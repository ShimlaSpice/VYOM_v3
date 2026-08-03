from __future__ import annotations

from types import SimpleNamespace

from app.scanner.scanner import ScannerEngine


class StubProvider:
    def prefetch(self, symbols, period="3mo", interval="1d") -> None:
        return None

    def get_market_context(self, symbol):
        if symbol == "^NSEI":
            return SimpleNamespace(change_percent=0.5)
        return SimpleNamespace(
            close=150.0,
            volume=200000,
            change_percent=1.2,
            indicators={
                "volume_ratio": 1.2,
                "sma20": 140.0,
                "sma50": 135.0,
                "ema20": 138.0,
                "rsi": 55.0,
                "macd": 1.0,
                "macd_signal": 0.2,
                "breakout": True,
            },
        )


def test_scanner_handles_partial_indicator_data():
    scanner = ScannerEngine(StubProvider())

    candidate = scanner._scan_symbol("RELIANCE", 100.0, 200.0, 0.0)

    assert candidate is not None
    assert candidate.symbol == "RELIANCE"
    assert candidate.score >= 0
