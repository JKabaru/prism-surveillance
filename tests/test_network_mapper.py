import pytest
import pandas as pd
import networkx as nx
from src.engine.network_mapper import PRISMNetworkMapper

def test_graph_filtering():
    # Mock Data
    clients = pd.DataFrame([
        {"client_id": "C1", "parent_sub_id": "S1", "master_partner_id": "P1", "name": "Client 1"},
        {"client_id": "C2", "parent_sub_id": "S1", "master_partner_id": "P1", "name": "Client 2"}
    ])
    trades = pd.DataFrame([
        {"trade_id": "T1", "client_id": "C1", "symbol": "EURUSD", "direction": "Buy", "volume": 1.0},
        {"trade_id": "T2", "client_id": "C2", "symbol": "GBPUSD", "direction": "Sell", "volume": 2.0}
    ])
    
    mapper = PRISMNetworkMapper(clients, None, None)
    
    # 1. Test Symbol Filter
    G_eur = mapper.build_filtered_graph(["C1", "C2"], trades, filters={'symbol': 'EURUSD'})
    assert G_eur.nodes["C:C1"]['status'] == 'active'
    assert G_eur.nodes["C:C2"]['status'] == 'inactive'
    
    # 2. Test Direction Filter
    G_sell = mapper.build_filtered_graph(["C1", "C2"], trades, filters={'direction': 'Sell'})
    assert G_sell.nodes["C:C1"]['status'] == 'inactive'
    assert G_sell.nodes["C:C2"]['status'] == 'active'
    
    # 3. Test Volume Filter
    G_vol = mapper.build_filtered_graph(["C1", "C2"], trades, filters={'min_volume': 1.5})
    assert G_vol.nodes["C:C1"]['status'] == 'inactive'
    assert G_vol.nodes["C:C2"]['status'] == 'active'
