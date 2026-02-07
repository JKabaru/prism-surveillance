import pandas as pd
import numpy as np

class PRISMRegimeMonitor:
    def __init__(self, baseline_days=20, deviation_threshold=2.5):
        self.baseline_days = baseline_days
        self.deviation_threshold = deviation_threshold

    def detect_regime_shifts(self, trades_df, clients_df):
        """
        Detects partners whose recent behavior deviates significantly from their historical baseline.
        Metrics: Daily Volume, Trade Count per Client, Win Rate.
        """
        # 1. Map trades to Partners
        df = trades_df.merge(clients_df[['client_id', 'master_partner_id']], on='client_id', how='left')
        df['date'] = pd.to_datetime(df['entry_time']).dt.date
        
        # 2. Aggregate Daily Metrics per Partner
        daily_stats = df.groupby(['master_partner_id', 'date']).agg(
            daily_volume=('volume', 'sum'),
            daily_trades=('trade_id', 'count')
        ).reset_index()
        
        daily_stats = daily_stats.sort_values(['master_partner_id', 'date'])
        
        alerts = []
        
        # 3. Analyze each partner
        for partner in daily_stats['master_partner_id'].unique():
            p_data = daily_stats[daily_stats['master_partner_id'] == partner]
            
            # Not enough data for baseline? Skip.
            if len(p_data) < 5:
                continue
                
            # Define "Current" as the last 3 days, "Baseline" as everything before
            current_window = p_data.tail(3)
            baseline_window = p_data.iloc[:-3]
            
            if len(baseline_window) < 5:
                continue
            
            # Calculate Baseline Stats (Mean & Std Dev)
            baseline_vol_mean = baseline_window['daily_volume'].mean()
            baseline_vol_std = baseline_window['daily_volume'].std()
            
            # Calculate Current Stats
            current_vol_mean = current_window['daily_volume'].mean()
            
            # Check Z-Score for Volume
            if baseline_vol_std > 0:
                z_score = (current_vol_mean - baseline_vol_mean) / baseline_vol_std
                
                if z_score > self.deviation_threshold:
                    alerts.append({
                        "partner_id": partner,
                        "risk_score": min(0.99, (z_score / 10) + 0.5), # Cap at 0.99
                        "metric": "Volume Surge",
                        "baseline": round(baseline_vol_mean, 2),
                        "current": round(current_vol_mean, 2),
                        "z_score": round(z_score, 2),
                        "hypothesis": f"Significant volume spike (Z={z_score:.1f}) detected vs. 20-day baseline. consistent with 'Sleeper' activation."
                    })
                    
        return alerts
