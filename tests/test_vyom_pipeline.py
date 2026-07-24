"""
VYOM V3 Complete Pipeline Test
"""

from app.market import (
    YahooFinanceProvider,
    MarketEngine,
)

from app.scanner.technical_indicators import TechnicalIndicators

from app.trade_intelligence import (
    ATREngine,
    TradeClassifier,
    SetupGenerator,
)

from app.intelligence import (
    TechnicalEngine,
    FundamentalEngine,
    NewsEngine,
    SectorEngine,
    RiskEngine,
    ConfidenceEngine,
)

from app.recommendation import (
    RecommendationEngineV2,
    RecommendationFormatter,
)

# ==========================================================
# MARKET
# ==========================================================

provider = YahooFinanceProvider()

market = MarketEngine(provider)

symbol = "RELIANCE.NS"

candles = market.load_history(
    symbol=symbol,
    interval="1d",
    limit=60,
)

if not candles:

    print("No market data found.")

    raise SystemExit

# ==========================================================
# PRICE DATA
# ==========================================================

closes = [c["close"] for c in candles]
highs = [c["high"] for c in candles]
lows = [c["low"] for c in candles]
volumes = [c["volume"] for c in candles]

# ==========================================================
# TECHNICAL INDICATORS
# ==========================================================

sma20 = TechnicalIndicators.sma(
    closes,
    20,
)

ema20 = TechnicalIndicators.ema(
    closes,
    20,
)

rsi = TechnicalIndicators.rsi(
    closes,
)

macd, signal = TechnicalIndicators.macd(
    closes,
)

avg_volume = TechnicalIndicators.average_volume(
    volumes,
)

breakout = TechnicalIndicators.breakout(
    highs,
    closes[-1],
)

volume_spike = volumes[-1] > (avg_volume * 1.5)

# ==========================================================
# ATR
# ==========================================================

atr_engine = ATREngine()

atr_summary = atr_engine.summary(
    highs,
    lows,
    closes,
)

# ==========================================================
# TRADE CLASSIFICATION
# ==========================================================

classifier = TradeClassifier()

trade = classifier.classify(

    score=82,

    atr_percent=atr_summary["atr_percent"],

    trend="BULLISH",

    sentiment="POSITIVE",

)

# ==========================================================
# TRADE SETUP
# ==========================================================

setup = SetupGenerator().generate(

    highs,

    lows,

    closes,

    trade["category"],

)

# ==========================================================
# TECHNICAL INTELLIGENCE
# ==========================================================

technical = TechnicalEngine().evaluate(

    score=20,

    rsi=rsi,

    macd=macd,

    sma=closes[-1] > sma20,

    ema=closes[-1] > ema20,

    breakout=breakout,

    volume=volume_spike,

)

# ==========================================================
# FUNDAMENTALS
# ==========================================================

fundamental = FundamentalEngine().evaluate(

    pe=22,

    eps=65,

    roe=18,

    debt_to_equity=45,

    market_cap=1_800_000_000_000,

)

# ==========================================================
# NEWS
# ==========================================================

news = NewsEngine().evaluate(

    sentiment="POSITIVE",

    confidence=0.90,

    headlines=[

        {
            "title": "Positive Quarterly Results"
        },

        {
            "title": "Broker Upgrade"
        },

        {
            "title": "Expansion Plans"
        },

    ],

)

# ==========================================================
# SECTOR
# ==========================================================

sector = SectorEngine().evaluate(

    sector="Energy",

)

# ==========================================================
# RISK
# ==========================================================

risk = RiskEngine().evaluate(

    atr_percent=atr_summary["atr_percent"],

    volatility=atr_summary["volatility"],

    risk_reward=setup["risk_reward"],

)

# ==========================================================
# CONFIDENCE
# ==========================================================

confidence = ConfidenceEngine().calculate(

    technical=technical["score"],

    fundamental=fundamental["score"],

    news=news["score"],

    sector=sector["score"],

    relative_strength=8,

    market=8,

    risk=risk["score"],

)

# ==========================================================
# FINAL RECOMMENDATION
# ==========================================================

recommendation = RecommendationEngineV2().generate(

    symbol=symbol,

    technical=technical,

    fundamental=fundamental,

    news=news,

    sector=sector,

    risk=risk,

    confidence=confidence,

    trade_setup=setup,

    trade_type=trade,

)

# ==========================================================
# OUTPUT
# ==========================================================

formatter = RecommendationFormatter()

print()

print("=" * 80)
print("VYOM COMPLETE PIPELINE")
print("=" * 80)
print()

print(
    formatter.format(
        recommendation
    )
)

print()

print("=" * 80)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 80)