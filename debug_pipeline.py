#!/usr/bin/env python3
import traceback
from app.pipeline.market_pipeline import MarketPipeline

try:
    pipeline = MarketPipeline()
    result = pipeline.run({'universe': 'NIFTY50', 'top': 10})
except Exception as e:
    print(f'ERROR: {e}')
    traceback.print_exc()
    result = []

print(f'\n[DEBUG] Result type: {type(result).__name__}')
print(f'[DEBUG] Result count: {len(result)}')

for i, item in enumerate(result[:3]):
    print(f'\n[Row {i}]')
    print(f'  Type: {type(item).__name__}')
    print(f'  Symbol: {getattr(item, "symbol", "MISSING")}')
    print(f'  Price: {getattr(item, "price", "MISSING")}')
    print(f'  Close: {getattr(item, "close", "MISSING")}')
    print(f'  Confidence: {getattr(item, "confidence", "MISSING")}')
    print(f'  Has slots: {hasattr(item, "__slots__")}')
    if hasattr(item, "__dict__"):
        print(f'  Dict keys: {list(item.__dict__.keys())[:5]}')
