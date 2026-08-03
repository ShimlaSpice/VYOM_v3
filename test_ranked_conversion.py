#!/usr/bin/env python3
"""
Test RankedStock conversion to verify fields are preserved.
"""

from app.recommendation.recommendation_model import Recommendation
from app.top10.models import RankedStock
from app.top10 import Top10Engine

print("\n" + "="*70)
print("RANKEDSTOCK FIELD PRESERVATION TEST")
print("="*70)

# Create a test recommendation
rec = Recommendation(
    symbol="RELIANCE",
    recommendation="BUY",
    category="LARGE_CAP",
    confidence=85,
    probability=80,
    entry=2500.0,
    stop_loss=2450.0,
    target1=2600.0,
    target2=2700.0,
    risk_level="MEDIUM",
    close=2520.0,
    sector="ENERGY",
    industry="OIL_GAS",
    ai_summary="Strong uptrend",
    reasons=["High volume", "Breakout"],
    scores={"technical": 80, "fundamental": 75},
)

print(f"\n[1] Original Recommendation:")
print(f"    symbol: {rec.symbol}")
print(f"    close: {rec.close}")
print(f"    confidence: {rec.confidence}")
print(f"    sector: {rec.sector}")

# Convert to RankedStock
ranked = RankedStock.from_recommendation(rec)

print(f"\n[2] Converted RankedStock:")
print(f"    symbol: {ranked.symbol}")
print(f"    price: {ranked.price}")
print(f"    close: {ranked.close}")
print(f"    confidence: {ranked.confidence}")
print(f"    sector: {ranked.sector}")
print(f"    ai_summary: {ranked.ai_summary}")

# Check if fields match
print(f"\n[3] Field Validation:")
assert ranked.symbol == "RELIANCE", f"Symbol mismatch: {ranked.symbol}"
assert ranked.price == 2520.0, f"Price mismatch: {ranked.price}"
assert ranked.confidence == 85, f"Confidence mismatch: {ranked.confidence}"
assert ranked.sector == "ENERGY", f"Sector mismatch: {ranked.sector}"
print("    ✓ All fields preserved correctly")

# Now test Top10Engine with a list
print(f"\n[4] Testing Top10Engine...")
engine = Top10Engine()
result = engine.generate([rec, rec, rec], limit=10)

print(f"    Returned {len(result)} ranked stocks")
if result:
    print(f"    First item symbol: {result[0].symbol}")
    print(f"    First item price: {result[0].price}")
    
print("\n" + "="*70 + "\n")
