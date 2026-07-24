from app.market import YahooFinanceProvider
from app.trading import TradeSetupEngine

provider = YahooFinanceProvider()

quote = provider.get_quote(
    "RELIANCE.NS",
)

engine = TradeSetupEngine()

setup = engine.generate(
    quote["last_price"],
)

print()

print("=" * 60)
print("TRADE SETUP")
print("=" * 60)

print(f"Symbol      : {quote['symbol']}")
print(f"Current     : {quote['last_price']:.2f}")
print(f"Entry       : {setup['entry']:.2f}")
print(f"Stop Loss   : {setup['stop_loss']:.2f}")
print(f"Target 1    : {setup['target1']:.2f}")
print(f"Target 2    : {setup['target2']:.2f}")
print(f"RiskReward  : 1:{setup['risk_reward']}")