import pandas as pd
import numpy as np
from faker import Faker
import networkx as nx
import random
import os
from datetime import datetime, timedelta

fake = Faker()

class PRISMDataGenerator:
    def __init__(self, seed=42):
        self.seed = seed
        Faker.seed(seed)
        random.seed(seed)
        np.random.seed(seed)
        
    def generate_hierarchy(self, num_partners=5, subs_per_partner=3, clients_per_sub=10):
        partners = []
        subs = []
        clients = []
        
        for i in range(num_partners):
            p_id = f"P-{1000 + i}"
            partners.append({
                "partner_id": p_id,
                "name": fake.company(),
                "country": fake.country(),
                "join_date": fake.date_between(start_date="-2y", end_date="-1y"),
                "risk_profile": "Standard" # Default
            })
            
            for j in range(subs_per_partner):
                s_id = f"S-{p_id}-{100 + j}"
                
                # Introduce a "Commission Farmer" sub-affiliate
                is_commission_farmer = (i == 0 and j == 0) # Hardcode one for demo
                
                subs.append({
                    "sub_affiliate_id": s_id,
                    "parent_partner_id": p_id,
                    "name": fake.name(),
                    "region": fake.city(),
                    "is_commission_farmer": is_commission_farmer
                })
                
                # Commission farmers have MORE clients, but low quality
                current_clients_per_sub = clients_per_sub * 3 if is_commission_farmer else clients_per_sub
                
                for k in range(current_clients_per_sub):
                    c_id = f"C-{s_id}-{10000 + k}"
                    clients.append({
                        "client_id": c_id,
                        "parent_sub_id": s_id,
                        "master_partner_id": p_id,
                        "name": fake.name(),
                        "email": fake.email(),
                        "account_type": random.choice(["Standard", "Raw", "Premium"]),
                        "registration_date": fake.date_between(start_date="-1y", end_date="now")
                    })
                    
        return pd.DataFrame(partners), pd.DataFrame(subs), pd.DataFrame(clients)

    def generate_trades(self, clients_df, subs_df, num_trades_multiplier=20, mirror_fraud_groups=1, bonus_abuse_count=5, regime_shift_config=None):
        trades = []
        base_time = datetime(2025, 1, 1, 10, 0, 0)
        symbols = ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD", "ETHUSD", "Gold", "Oil"]
        
        # Helper to check if client belongs to commission farmer
        farmer_subs = subs_df[subs_df['is_commission_farmer'] == True]['sub_affiliate_id'].tolist()
        
        # Regime Shift Logic: "Sleeper" Partners
        # If config provided: {'partner_id': 'P-1004', 'start_day': 25, 'volume_mult': 5.0}
        sleeper_partners = regime_shift_config if regime_shift_config else []
        
        for _, client in clients_df.iterrows():
            is_farmed_client = client['parent_sub_id'] in farmer_subs
            
            # Check if this client belongs to a sleeper partner
            is_sleeper = False
            shift_start_date = None
            vol_mult = 1.0
            
            for sleeper in sleeper_partners:
                if client['master_partner_id'] == sleeper['partner_id']:
                    is_sleeper = True
                    shift_start_date = base_time + timedelta(days=sleeper['start_day'])
                    vol_mult = sleeper['volume_mult']
            
            # Commission Inflation: High volume of tiny trades, short duration
            if is_farmed_client:
                num_trades = random.randint(50, 100)
                avg_duration = random.randint(5, 60)
                avg_volume = 0.01
            else:
                num_trades = random.randint(5, num_trades_multiplier)
                avg_duration = random.randint(300, 3600)
                avg_volume = round(random.uniform(0.1, 2.0), 2)

            for t in range(num_trades):
                # Distribute trades over 30 days
                trade_offset_seconds = random.randint(0, 86400 * 30)
                entry_time = base_time + timedelta(seconds=trade_offset_seconds)
                
                # Apply Regime Shift if applicable
                current_vol = avg_volume
                current_dur = avg_duration
                
                if is_sleeper and entry_time > shift_start_date:
                    # THE FLIP: Suddenly increase volume and frequency (simulated here by just volume for now)
                    current_vol = avg_volume * float(vol_mult)
                    # Maybe they start churning more?
                    current_dur = max(1, int(avg_duration * 0.1)) # Drastic drop in duration
                
                duration = max(1, int(np.random.normal(current_dur, current_dur*0.2)))
                exit_time = entry_time + timedelta(seconds=duration)
                
                trades.append({
                    "trade_id": f"T-{client['client_id']}-{t}",
                    "client_id": client["client_id"],
                    "symbol": random.choice(symbols),
                    "direction": random.choice(["Buy", "Sell"]),
                    "volume": round(current_vol, 2),
                    "entry_time": entry_time,
                    "exit_time": exit_time,
                    "profit": round(random.uniform(-10, 10), 2) if is_farmed_client else round(random.uniform(-100, 150), 2),
                    "trade_type": "Legit" if not is_farmed_client else "CommissionFarming",
                    "is_fraud": False 
                })
        
        # Inject Mirror Trading (Phase 1)
        for g in range(mirror_fraud_groups):
            fraud_clients = clients_df.sample(random.randint(3, 8))["client_id"].tolist()
            ring_id = f"RING-MIRROR-{g}"
            for t in range(10): 
                entry_time = base_time + timedelta(seconds=random.randint(0, 86400 * 30))
                exit_time = entry_time + timedelta(seconds=random.randint(60, 600))
                symbol = random.choice(symbols)
                direction = random.choice(["Buy", "Sell"])
                volume = round(random.uniform(1.0, 10.0), 2)
                
                for c_id in fraud_clients:
                    jitter = random.uniform(0.001, 0.5)
                    trades.append({
                        "trade_id": f"T-FRAUD-{c_id}-{t}",
                        "client_id": c_id,
                        "symbol": symbol,
                        "direction": direction,
                        "volume": volume,
                        "entry_time": entry_time + timedelta(seconds=jitter),
                        "exit_time": exit_time + timedelta(seconds=jitter),
                        "profit": round(random.uniform(50, 500), 2),
                        "trade_type": "Mirror",
                        "is_fraud": True,
                        "fraud_ring_id": ring_id
                    })

        # Inject Bonus Abuse (Phase 2)
        bonus_abusers = clients_df.sample(bonus_abuse_count)["client_id"].tolist()
        for c_id in bonus_abusers:
             entry_time = base_time + timedelta(seconds=random.randint(0, 86400 * 5))
             trades.append({
                "trade_id": f"T-BONUS-{c_id}",
                "client_id": c_id,
                "symbol": "EURUSD",
                "direction": "Buy",
                "volume": 5.0, # Max leverage
                "entry_time": entry_time,
                "exit_time": entry_time + timedelta(seconds=30), # Quick exit
                "profit": 0,
                "trade_type": "BonusAbuse", 
                "is_fraud": True,
                "note": "Immediate Withdrawal Triggered"
             })

        return pd.DataFrame(trades)

    def save_data(self, partners, subs, clients, trades, output_dir="data"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        partners.to_csv(f"{output_dir}/partners.csv", index=False)
        subs.to_csv(f"{output_dir}/subs.csv", index=False)
        clients.to_csv(f"{output_dir}/clients.csv", index=False)
        trades.to_csv(f"{output_dir}/trades.csv", index=False)
        print(f"Data saved to {output_dir}/")

if __name__ == "__main__":
    generator = PRISMDataGenerator()
    p, s, c = generator.generate_hierarchy(num_partners=5, subs_per_partner=3, clients_per_sub=10)
    
    # Phase 4 Configuration: Partner P-1004 is a sleeper
    # They behave normally until Day 20, then explode volume by 5x
    sleeper_config = [{'partner_id': 'P-1004', 'start_day': 20, 'volume_mult': 5.0}]
    
    t = generator.generate_trades(c, s, mirror_fraud_groups=2, bonus_abuse_count=5, regime_shift_config=sleeper_config)
    generator.save_data(p, s, c, t)
