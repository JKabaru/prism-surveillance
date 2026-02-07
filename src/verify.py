import pandas as pd
from src.engine.correlation_engine import PRISMCorrelationEngine
from src.engine.network_mapper import PRISMNetworkMapper
from src.engine.synthesizer import PRISMEvidenceSynthesizer

def run_verification():
    print("--- PRISM Verification Start ---")
    
    # Load Data
    p_df = pd.read_csv("data/partners.csv")
    s_df = pd.read_csv("data/subs.csv")
    c_df = pd.read_csv("data/clients.csv")
    t_df = pd.read_csv("data/trades.csv")
    
    print(f"Loaded {len(t_df)} trades across {len(c_df)} clients.")
    
    # Detection
    engine = PRISMCorrelationEngine(time_window_seconds=1.0)
    clusters = engine.detect_mirror_trades(t_df)
    rings = engine.aggregate_rings(clusters)
    
    print(f"Detected {len(clusters)} temporal clusters.")
    print(f"Identified {len(rings)} potential fraud rings.")
    
    # Attribution & Analysis
    mapper = PRISMNetworkMapper(c_df, s_df, p_df)
    synthesizer = PRISMEvidenceSynthesizer()
    
    for ring in rings:
        attr = mapper.get_attribution(ring['client_ids'])
        evidence = synthesizer.synthesize_ring(ring, attr)
        
        print(f"\n[RING FOUND: {ring['id']}]")
        print(f"Clients: {ring['client_ids']}")
        print(f"Confidence: {evidence['confidence']}")
        print(f"Hypothesis: {evidence['hypothesis']}")
        print(f"Indicators: {evidence['indicators']}")
        
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    run_verification()
