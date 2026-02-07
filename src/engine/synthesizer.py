import pandas as pd
from src.engine.agentic_engine import PRISMAgenticEngine

class PRISMEvidenceSynthesizer:
    def __init__(self):
        pass
        
    def synthesize_ring(self, ring, attribution):
        """
        Generates a summary evidence package for a detected fraud ring,
        now including agentic autonomy recommendations.
        """
        num_clients = len(ring['client_ids'])
        num_clusters = len(ring['clusters'])
        top_partner = next(iter(attribution['top_partners'])) if attribution['top_partners'] else "Unknown"
        
        # Calculate exposure (sum of profits in fraud trades)
        exposure = 0
        for cluster in ring['clusters']:
            exposure += cluster['count'] * 50 # Mock value per trade
            
        confidence = min(0.99, 0.7 + (num_clusters * 0.05))
        
        hypothesis = (
            f"Detected a coordinated mirror trading ring involving {num_clients} clients "
            f"across {len(attribution['top_subs'])} sub-affiliates. "
            f"The ring has executed {num_clusters} synchronized trading events with high temporal correlation (<1s). "
            f"Primary attribution leads to Partner {top_partner}."
        )

        # Agentic decision context
        agent = PRISMAgenticEngine()
        context = {
            "cluster_id": ring['id'],
            "confidence": confidence,
            "human_available": False # Defaulting to autonomous mode for demo
        }
        decision = agent.decide_action(context)
        
        return {
            "hypothesis": hypothesis,
            "exposure": round(exposure, 2),
            "confidence": round(confidence, 2),
            "indicators": [
                "Temporal Synchronization (<1s)",
                "Cross-Affiliate Coordination",
                "Repeated Pattern (Mirror Trading)",
                f"Concentrated Attribution: {top_partner}"
            ],
            "agent_decision": decision,
            "authorized_actions": [a.value for a in agent.get_authorized_actions(confidence)]
        }


    def synthesize_bonus_abuse(self, client_id, risk_score, trade_count):
        hypothesis = (
            f"Detected high-risk bonus abuse pattern for Client {client_id}. "
            f"Subject executed {trade_count} high-volume trades with negligible duration immediately after deposit, "
            f"consistent with 'Hit and Run' behavior."
        )
        return {
            "hypothesis": hypothesis,
            "exposure": 1000.00, # Mock exposure
            "confidence": risk_score,
            "indicators": [
                "Rapid Deposit-Trade-Withdraw Cycle",
                "High Volume / Zero Retention",
                "Abnormal Trade Duration (<60s)"
            ]
        }

    def synthesize_commission_inflation(self, sub_id, risk_score, stats):
        hypothesis = (
            f"Sub-Affiliate {sub_id} exhibits signs of commission inflation. "
            f"Generated {stats['total_trades']} trades across {stats['unique_clients']} clients with "
            f"an average duration of {int(stats['avg_duration'])}s. This pattern suggests "
            f"automated or incentivized low-quality traffic."
        )
        return {
            "hypothesis": hypothesis,
            "exposure": stats['total_volume'] * 10, # Mock commission calc
            "confidence": risk_score,
            "indicators": [
                "High Trade Frequency / Low Duration",
                "Low Profitability per Client",
                "Abnormal Client Churn"
            ]
        }
