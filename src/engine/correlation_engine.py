import pandas as pd
import numpy as np

class PRISMCorrelationEngine:
    def __init__(self, time_window_seconds=1.0):
        self.time_window_seconds = time_window_seconds
        
    def detect_mirror_trades(self, trades_df):
        """
        Detects groups of trades that are synchronized in time on the same symbol and direction.
        """
        # Ensure entry_time is datetime
        trades_df['entry_time'] = pd.to_datetime(trades_df['entry_time'])
        
        # Sort by entry time
        trades_df = trades_df.sort_values(by='entry_time').reset_index(drop=True)
        
        clusters = []
        visited = set()
        
        for i, trade in trades_df.iterrows():
            if i in visited:
                continue
                
            # Find candidate trades within the time window on the same symbol and direction
            mask = (
                (trades_df.index != i) &
                (~trades_df.index.isin(visited)) &
                (trades_df['symbol'] == trade['symbol']) &
                (trades_df['direction'] == trade['direction']) &
                (trades_df['entry_time'] >= trade['entry_time']) &
                (trades_df['entry_time'] <= trade['entry_time'] + pd.Timedelta(seconds=self.time_window_seconds))
            )
            
            group = trades_df[mask]
            if not group.empty:
                # We found a synchronized group
                cluster_ids = [trade['trade_id']] + group['trade_id'].tolist()
                cluster_clients = [trade['client_id']] + group['client_id'].tolist()
                
                # Check if it involves more than one client (internal sanity check)
                if len(set(cluster_clients)) > 1:
                    clusters.append({
                        "id": f"CLUSTER-{len(clusters)}",
                        "trade_ids": cluster_ids,
                        "client_ids": list(set(cluster_clients)),
                        "symbol": trade['symbol'],
                        "entry_time_median": trade['entry_time'],
                        "count": len(cluster_ids)
                    })
                    
                    # Mark all as visited to avoid double counting the same synchronization event
                    visited.add(i)
                    for idx in group.index:
                        visited.add(idx)
        
        return clusters

    def aggregate_rings(self, clusters):
        """
        Groups clusters into potential 'rings' if multiple clusters share the same set of clients.
        """
        from collections import defaultdict
        
        client_to_ring = {}
        rings = []
        
        for cluster in clusters:
            clients = tuple(sorted(cluster['client_ids']))
            found_ring = False
            for ring in rings:
                # If there's significant overlap in clients, merge or associate
                if set(clients).intersection(set(ring['client_ids'])):
                    ring['clusters'].append(cluster)
                    ring['client_ids'] = list(set(ring['client_ids']).union(set(clients)))
                    found_ring = True
                    break
            
            if not found_ring:
                rings.append({
                    "id": f"RING-{len(rings)}",
                    "client_ids": list(clients),
                    "clusters": [cluster]
                })
        
        # Filter rings that have multiple clusters (repeated behavior)
        active_rings = [r for r in rings if len(r['clusters']) >= 3]
        return active_rings

if __name__ == "__main__":
    # Test with generated data
    trades = pd.read_csv("data/trades.csv")
    engine = PRISMCorrelationEngine(time_window_seconds=1.0)
    clusters = engine.detect_mirror_trades(trades)
    rings = engine.aggregate_rings(clusters)
    print(f"Detected {len(clusters)} clusters and {len(rings)} rings.")
    for ring in rings:
        print(f"Ring {ring['id']}: Clients {ring['client_ids']}, Clusters: {len(ring['clusters'])}")
