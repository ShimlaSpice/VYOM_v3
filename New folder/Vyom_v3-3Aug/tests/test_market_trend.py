from app.market import YahooFinanceProvider
from app.market.market_trend import MarketTrendEngine

provider = YahooFinanceProvider()

engine = MarketTrendEngine(provider)

market = engine.analyze()

print()

print("========== MARKET ==========")
print(f"Trend : {market['trend']}")
print(f"Close : {market['close']:.2f}")
print(f"SMA20 : {market['sma20']:.2f}")
print(f"EMA20 : {market['ema20']:.2f}")