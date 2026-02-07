import pytest
import pandas as pd
from src.data.data_generator import PRISMDataGenerator

def test_hierarchy_generation():
    generator = PRISMDataGenerator(seed=42)
    p, s, c = generator.generate_hierarchy(num_partners=2, subs_per_partner=2, clients_per_sub=5)
    
    assert len(p) == 2
    assert len(s) == 4
    assert len(c) == 20
    assert "master_partner_id" in c.columns
    assert "parent_sub_id" in c.columns

def test_trade_generation_with_fraud():
    generator = PRISMDataGenerator(seed=42)
    p, s, c = generator.generate_hierarchy(num_partners=2, subs_per_partner=2, clients_per_sub=5)
    t = generator.generate_trades(c, mirror_fraud_groups=1)
    
    assert len(t[t['is_fraud'] == True]) > 0
    assert "fraud_ring_id" in t.columns
    # Check if entry_time is correctly formatted
    assert pd.api.types.is_datetime64_any_dtype(t['entry_time'])
