import pytest
import pandas as pd
from src.engine.behavior_engine import PRISMBehaviorEngine

def test_bonus_abuse_detection():
    engine = PRISMBehaviorEngine()
    
    # Mock Data: Client deposits, buys huge, exits fast
    clients = pd.DataFrame([
        {"client_id": "C1", "registration_date": "2025-01-01"}
    ])
    
    trades = pd.DataFrame([
        {
            "trade_id": "T1", "client_id": "C1", "volume": 5.0, 
            "entry_time": "2025-01-02 10:00:00", 
            "exit_time": "2025-01-02 10:00:10" # 10s duration
        }
    ])
    
    report = engine.detect_bonus_abuse(trades, clients)
    assert len(report) == 1
    assert report[0]['client_id'] == "C1"

def test_commission_inflation_detection():
    engine = PRISMBehaviorEngine()
    
    # Mock Data: Sub has many trades, many clients, but low duration
    subs = pd.DataFrame([{"sub_affiliate_id": "S1"}])
    clients = pd.DataFrame([
        {"client_id": f"C{i}", "parent_sub_id": "S1"} for i in range(10)
    ])
    
    trades = []
    for i in range(100): # 100 trades
        trades.append({
            "trade_id": f"T{i}", 
            "client_id": f"C{i%10}", 
            "volume": 0.01,
            "entry_time": "2025-01-01 10:00:00",
            "exit_time": "2025-01-01 10:00:30" # 30s avg duration
        })
    trades_df = pd.DataFrame(trades)
    
    suspicious = engine.detect_commission_inflation(trades_df, clients, subs)
    
    assert len(suspicious) == 1
    assert suspicious[0]['sub_affiliate_id'] == "S1"
    assert suspicious[0]['stats']['total_trades'] == 100
