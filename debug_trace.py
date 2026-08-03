#!/usr/bin/env python3
"""
Debug script to trace recommendation flow from pipeline to UI table.
"""

import sys
from app.pipeline.market_pipeline import MarketPipeline
from app.top10.models import RankedStock

print("\n" + "="*70)
print("VYOM PIPELINE DEBUG TRACE")
print("="*70)

try:
    print("\n[1] Running pipeline...")
    pipeline = MarketPipeline()
    result = pipeline.run({'universe': 'NIFTY50', 'top': 10})
    
    print(f"\n[2] Pipeline returned: type={type(result).__name__}, count={len(result) if result else 0}")
    
    if result and len(result) > 0:
        for idx, item in enumerate(result[:3]):
            print(f"\n[3.{idx}] Item {idx}:")
            print(f"       Type: {type(item).__name__}")
            print(f"       Has __slots__: {hasattr(item, '__slots__')}")
            print(f"       Has __dict__: {hasattr(item, '__dict__')}")
            
            # Try to extract all fields
            fields = ['symbol', 'price', 'close', 'confidence', 'recommendation', 'entry', 'target', 'stop_loss', 'sector', 'industry']
            for field in fields:
                val = getattr(item, field, f"<MISSING:{field}>")
                print(f"       {field}: {val}")
            
            # If it has __dict__, show all keys
            if hasattr(item, '__dict__'):
                print(f"       __dict__ keys: {list(item.__dict__.keys())}")
                
    print("\n[4] Now simulating table extraction...")
    if result:
        for row, stock in enumerate(result[:2]):
            print(f"\n[TABLE] Row {row}:")
            print(f"         Type: {type(stock).__name__}")
            
            symbol = getattr(stock, "symbol", "")
            price = getattr(stock, "price", 0)
            close = getattr(stock, "close", 0)
            confidence = getattr(stock, "confidence", 0)
            
            print(f"         symbol={symbol}, price={price}, close={close}, conf={confidence}")
            
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*70 + "\n")
