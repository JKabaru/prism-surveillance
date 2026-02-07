import pytest
import pandas as pd
from datetime import datetime, timedelta
from src.engine.correlation_engine import PRISMCorrelationEngine

def test_mirror_trade_detection():
    # Create mock trades with guaranteed mirror pattern
    base_time = datetime(2025, 1, 1, 12, 0, 0)
    trades = pd.DataFrame([
        {"trade_id": "T1", "client_id": "C1", "symbol": "EURUSD", "direction": "Buy", "entry_time": base_time},
        {"trade_id": "T2", "client_id": "C2", "symbol": "EURUSD", "direction": "Buy", "entry_time": base_time + timedelta(milliseconds=100)},
        {"trade_id": "T3", "client_id": "C3", "symbol": "EURUSD", "direction": "Buy", "entry_time": base_time + timedelta(milliseconds=200)},
        # Noise trade
        {"trade_id": "T4", "client_id": "C4", "symbol": "EURUSD", "direction": "Buy", "entry_time": base_time + timedelta(seconds=10)},
    ])
    
    engine = PRISMCorrelationEngine(time_window_seconds=1.0)
    clusters = engine.detect_mirror_trades(trades)
    
    assert len(clusters) == 1
    assert clusters[0]['count'] == 3
    assert "C1" in clusters[0]['client_ids']
    assert "C2" in clusters[0]['client_ids']
    assert "C3" in clusters[0]['client_ids']

def test_ring_aggregation():
    engine = PRISMCorrelationEngine()
    # Mock clusters
    clusters = [
        {"id": "CL1", "client_ids": ["C1", "C2"]},
        {"id": "CL2", "client_ids": ["C1", "C2"]},
        {"id": "CL3", "client_ids": ["C1", "C2"]},
    ]
    
    rings = engine.aggregate_rings(clusters)
    assert len(rings) == 1
    assert rings[0]['id'] == "RING-0"
    assert set(rings[0]['client_ids']) == {"C1", "C2"}
