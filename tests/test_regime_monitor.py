import pytest
import pandas as pd
import numpy as np
from src.engine.regime_monitor import PRISMRegimeMonitor

def test_regime_shift_detection():
    # Use a lower threshold for testing
    monitor = PRISMRegimeMonitor(baseline_days=5, deviation_threshold=2.0)
    
    # Create synthetic trade data for a partner
    trades = []
    base_date = pd.to_datetime("2025-01-01")
    
    # Baseline: 10 days, variable trades/day, vol=1.0
    for day in range(10):
        # Vary the number of trades per day to create variance in daily_volume
        num_trades = 10 + (1 if day % 2 == 0 else -1)
        for i in range(num_trades):
            trades.append({
                "trade_id": f"T-B{day}-{i}", 
                "client_id": "C1", 
                "volume": 1.0, 
                "entry_time": base_date + pd.Timedelta(days=day)
            })
            
    # Spike: 3 days, 10 trades/day, vol=10.0
    for day in range(10, 13):
        for i in range(10):
            trades.append({
                "trade_id": f"T-S{day}-{i}", 
                "client_id": "C1", 
                "volume": 10.0, 
                "entry_time": base_date + pd.Timedelta(days=day)
            })
            
    trades_df = pd.DataFrame(trades)
    clients_df = pd.DataFrame([{"client_id": "C1", "master_partner_id": "P-TEST"}])
    
    alerts = monitor.detect_regime_shifts(trades_df, clients_df)
    
    assert len(alerts) == 1
    assert alerts[0]['partner_id'] == "P-TEST"
    assert alerts[0]['z_score'] > 2.0
