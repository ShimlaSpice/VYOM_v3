"""
Complete Market Pipeline.

UI
 ↓
Scanner  (bulk-prefetches the whole universe, filters to candidates)
 ↓
Recommendation Pipeline  (parallel, per-candidate)
 ↓
Top10
"""

from __future__ import annotations

import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import perf_counter

from app.market.provider_manager import ProviderManager
from app.pipeline.recommendation_pipeline import RecommendationPipeline
from app.scanner.scanner import ScannerEngine
from app.top10 import Top10Engine

_DEFAULT_NEWS = {"sentiment": "NEUTRAL", "confidence": 0.50, "headlines": []}


class MarketPipeline:

    def __init__(self):
        self.provider = ProviderManager()
        self.provider.connect()
        self.scanner  = ScannerEngine(self.provider)
        self.top10    = Top10Engine()
        # One RecommendationPipeline per worker thread to avoid shared state
        self._workers = 8

    def _make_pipeline(self) -> RecommendationPipeline:
        return RecommendationPipeline()

    # ------------------------------------------------------------------
    def run(self, filters: dict | None = None):
        if filters is None:
            filters = {"universe": "NIFTY50", "top": 10}

        t0 = perf_counter()

        # ── 1. Scan (scanner already bulk-prefetches the universe) ──────
        scan_result = self.scanner.scan(filters=filters)
        candidates  = scan_result.candidates
        if not candidates:
            return []

        symbols = [c.symbol for c in candidates]
        print(f"[PIPELINE] {len(symbols)} candidates after scan ({perf_counter()-t0:.1f}s)")

        # ── 2. Pre-fetch fundamentals for all candidates in parallel ────
        t1 = perf_counter()
        with ThreadPoolExecutor(max_workers=min(len(symbols), 12)) as ex:
            list(ex.map(lambda s: self.provider.get_fundamentals(s), symbols))
        print(f"[PIPELINE] Fundamentals prefetched ({perf_counter()-t1:.1f}s)")

        # ── 3. Build recommendations in parallel ────────────────────────
        t2        = perf_counter()
        results   = []
        n_workers = min(len(candidates), self._workers)

        def _build(candidate):
            pipeline = self._make_pipeline()   # thread-local instance
            sym = candidate.symbol
            try:
                candles = self.provider.get_candles(sym, interval="1d", limit=100)
                if len(candles) < 50:
                    return None
                fundamentals = self.provider.get_fundamentals(sym) or {}
                news         = self.provider.get_news(sym) or _DEFAULT_NEWS
                rec = pipeline.build(
                    candidate=candidate,
                    candles=candles,
                    fundamentals=fundamentals,
                    news=news,
                    sector=fundamentals.get("sector", "Unknown"),
                )
                if rec is not None:
                    print(f"[OK] {sym}")
                return rec
            except Exception:
                return None

        with ThreadPoolExecutor(max_workers=n_workers) as ex:
            futures = {ex.submit(_build, c): c for c in candidates}
            for fut in as_completed(futures):
                rec = fut.result()
                if rec is not None:
                    results.append(rec)

        print(f"[PIPELINE] {len(results)} recommendations built ({perf_counter()-t2:.1f}s)")

        results.sort(
            key=lambda x: (getattr(x, "confidence", 0), getattr(x, "probability", 0)),
            reverse=True,
        )

        for rec in results[:3]:
            print(f"[RECS] {getattr(rec,'symbol','?')} - {getattr(rec,'recommendation','?')} ({getattr(rec,'confidence',0)}%)")

        ranked = self.top10.generate(results, limit=filters.get("top", 10))

        print(f"\n[TOP10] {len(ranked)} ranked  |  total {perf_counter()-t0:.1f}s")
        for item in ranked[:3]:
            print(f"[TOP10] {getattr(item,'symbol','?')} - {getattr(item,'price',0)}")

        return ranked

        if filters is None:

            filters = {
                "universe": "NIFTY50",
                "top": 10,
            }

        scan_result = self.scanner.scan(
            filters=filters,
        )

        candidates = scan_result.candidates

        if not candidates:
            return []

        symbols = [
            c.symbol
            for c in candidates
        ]

        self.provider.prefetch(
            symbols=symbols,
            period="6mo",
            interval="1d",
        )

        recommendations = []

        for candidate in candidates:

            print(f"[PIPELINE] {candidate.symbol}")

            try:

                candles = self.provider.get_candles(
                    symbol=candidate.symbol,
                    interval="1d",
                    limit=100,
                )

                if len(candles) < 50:
                    print(f"[SKIP] {candidate.symbol} (Not enough candles)")
                    continue

                fundamentals = self.provider.get_fundamentals(
                    candidate.symbol,
                ) or {}

                news = self.provider.get_news(
                    candidate.symbol,
                ) or {
                    "sentiment": "NEUTRAL",
                    "confidence": 0.50,
                    "headlines": [],
                }

                recommendation = self.pipeline.build(
                    candidate=candidate,
                    candles=candles,
                    fundamentals=fundamentals,
                    news=news,
                    sector=fundamentals.get(
                        "sector",
                        "Unknown",
                    ),
                )

                if recommendation is None:
                    print(f"[SKIP] {candidate.symbol} (No recommendation)")
                    continue

                print(f"[OK] {candidate.symbol}")

                recommendations.append(
                    recommendation,
                )

            except Exception:

                print(f"[FAILED] {candidate.symbol}")

                import traceback
                traceback.print_exc()

        recommendations.sort(
            key=lambda x: (
                getattr(x, "confidence", 0),
                getattr(x, "probability", 0),
            ),
            reverse=True,
        )

        print(f"\nGenerated {len(recommendations)} recommendations.\n")
        
        for rec in recommendations[:3]:
            print(f"[RECS] {getattr(rec, 'symbol', '?')} - {getattr(rec, 'recommendation', '?')} ({getattr(rec, 'confidence', 0)}%)")

        ranked = self.top10.generate(
            recommendations,
            limit=filters.get(
                "top",
                10,
            ),
        )
        
        print(f"\n[TOP10] Returned {len(ranked)} ranked stocks")
        for item in ranked[:3]:
            print(f"[TOP10] {getattr(item, 'symbol', '?')} - {getattr(item, 'price', 0)}")
        
        return ranked