import pytest
import pandas as pd
import io
from src.data.loader import PRISMDataLoader

def test_get_required_columns():
    loader = PRISMDataLoader()
    req = loader.get_required_columns()
    assert "Trades" in req
    assert "volume" in req["Trades"]

def test_load_from_files_with_mapping():
    loader = PRISMDataLoader()
    
    # User has 'UserID' instead of 'client_id'
    c_csv = io.BytesIO(b"UserID,parent_sub_id\nC-1,S-1")
    p_csv = io.BytesIO(b"partner_id,name\nP-1,Partner A")
    s_csv = io.BytesIO(b"sub_affiliate_id,parent_partner_id\nS-1,P-1")
    t_csv = io.BytesIO(b"trade_id,client_id,entry_time,symbol,direction,volume\nT-1,C-1,2025-01-01,EURUSD,Buy,1.0")
    
    mapping = {"Clients": {"UserID": "client_id"}}
    
    p, s, c, t = loader.load_from_files(p_csv, s_csv, c_csv, t_csv, column_mapping=mapping)
    
    assert "client_id" in c.columns
    assert c.iloc[0]["client_id"] == "C-1"

def test_load_from_files_invalid_schema():
    loader = PRISMDataLoader()
    
    # Missing 'name' column
    p_csv = io.BytesIO(b"partner_id\nP-1") 
    s_csv = io.BytesIO(b"sub_affiliate_id,parent_partner_id\nS-1,P-1")
    c_csv = io.BytesIO(b"client_id,parent_sub_id\nC-1,S-1")
    t_csv = io.BytesIO(b"trade_id,client_id,entry_time,symbol,direction,volume\nT-1,C-1,2025-01-01,EURUSD,Buy,1.0")

    with pytest.raises(ValueError, match="Missing required columns: name"):
        loader.load_from_files(p_csv, s_csv, c_csv, t_csv)

def test_load_from_db_mock():
    loader = PRISMDataLoader()
    
    success, msg = loader.load_from_db("postgresql://mock-db")
    assert success is True
    assert "Connected" in msg
    
    success, msg = loader.load_from_db("mysql://real-db")
    assert success is False
    assert "failed" in msg
