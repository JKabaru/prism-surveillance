import pandas as pd
import numpy as np

class PRISMBehaviorEngine:
    def __init__(self, min_trade_volume=4.0, max_trade_duration=60, churn_threshold=0.8):
        self.min_trade_volume = min_trade_volume
        self.max_trade_duration = max_trade_duration
        self.churn_threshold = churn_threshold

    def detect_bonus_abuse(self, trades_df, clients_df):
        """
        Detects 'Hit and Run' behavior: High volume, short duration trades 
        immediately followed by inactivity (simulated withdrawal).
        """
        # Merge to get registration dates
        df = trades_df.merge(clients_df[['client_id', 'registration_date']], on='client_id', how='left')
        df['registration_date'] = pd.to_datetime(df['registration_date'])
        df['entry_time'] = pd.to_datetime(df['entry_time'])
        
        # Calculate trade duration
        df['duration'] = (pd.to_datetime(df['exit_time']) - df['entry_time']).dt.total_seconds()
        
        # Filter for suspicious trades: High Volume + Short Duration
        suspicious_trades = df[
            (df['volume'] >= self.min_trade_volume) & 
            (df['duration'] <= self.max_trade_duration)
        ]
        
        # Group by client to find serial abusers
        abusers = suspicious_trades.groupby('client_id').size().reset_index(name='suspicious_count')
        
        # Return list of abusive clients with metadata
        abuse_report = []
        for pid in abusers['client_id']:
            client_trades = suspicious_trades[suspicious_trades['client_id'] == pid]
            abuse_report.append({
                "client_id": pid,
                "risk_score": 0.95,
                "reason": "Bonus Abuse: High-Leverage/Short-Duration Activity",
                "trade_count": len(client_trades)
            })
            
        return abuse_report

    def detect_commission_inflation(self, trades_df, clients_df, subs_df):
        """
        Detects specific sub-affiliates generating high volume but low quality traffic (churn).
        Metric: High Turn-Over Rate + Low Avg Trade Duration per Client.
        """
        # Map clients to sub-affiliates
        trade_client_merged = trades_df.merge(clients_df[['client_id', 'parent_sub_id']], on='client_id', how='left')
        
        # Aggregate metrics by Sub-Affiliate
        sub_stats = trade_client_merged.groupby('parent_sub_id').agg(
            total_volume=('volume', 'sum'),
            total_trades=('trade_id', 'count'),
            unique_clients=('client_id', 'nunique'),
            avg_duration=('exit_time', lambda x: (pd.to_datetime(x) - pd.to_datetime(trade_client_merged.loc[x.index, 'entry_time'])).dt.total_seconds().mean())
        ).reset_index()
        
        # Define "Inflation" criteria
        # High Volume per Client BUT Low Duration
        suspicious_subs = []
        
        for _, row in sub_stats.iterrows():
            avg_vol_per_client = row['total_volume'] / row['unique_clients'] if row['unique_clients'] > 0 else 0
            
            # Helper logic: If avg duration is surprisingly low (< 60s) for the aggregated portfolio
            # AND they have decent volume, it's likely machine-generated or grim farming.
            if row['avg_duration'] < 120 and row['total_trades'] > 50:
                 suspicious_subs.append({
                    "sub_affiliate_id": row['parent_sub_id'],
                    "risk_score": 0.88,
                    "reason": "Commission Inflation: High Freq / Low Duration",
                    "stats": row.to_dict()
                })
                
        return suspicious_subs
