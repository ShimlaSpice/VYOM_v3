from app.market import YahooFinanceProvider
from app.trade_intelligence import (
    ATREngine,
    TradeClassifier,
    SetupGenerator,
)

provider = YahooFinanceProvider()

candles = provider.get_candles(
    "RELIANCE.NS",
    interval="1d",
    limit=60,
)

highs = [c["high"] for c in candles]
lows = [c["low"] for c in candles]
closes = [c["close"] for c in candles]

atr_engine = ATREngine()

atr = atr_engine.summary(
    highs,
    lows,
    closes,
)

classifier = TradeClassifier()

trade = classifier.classify(
    score=82,
    atr_percent=atr["atr_percent"],
    trend="BULLISH",
    sentiment="POSITIVE",
)

setup = SetupGenerator()

result = setup.generate(
    highs,
    lows,
    closes,
    trade["category"],
)

print()

print("=" * 65)
print("VYOM TRADE INTELLIGENCE")
print("=" * 65)

print(f"Price        : {atr['price']}")
print(f"ATR          : {atr['atr']}")
print(f"ATR %        : {atr['atr_percent']}%")
print(f"Volatility   : {atr['volatility']}")

print()

print(f"Category     : {trade['category']}")
print(f"Confidence   : {trade['confidence']}%")

print()

print(f"Entry        : {result['entry']}")
print(f"Stop Loss    : {result['stop_loss']}")
print(f"Target 1     : {result['target1']}")
print(f"Target 2     : {result['target2']}")
print(f"RiskReward   : 1:{result['risk_reward']}")

print()

print("Reasons")

for reason in trade["reasons"]:
    print(f"✓ {reason}")