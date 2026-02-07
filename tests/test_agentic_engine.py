from src.engine.agentic_engine import PRISMAgenticEngine, ConfidenceTier, AgentAction

def test_agentic_engine_decisions():
    agent = PRISMAgenticEngine()
    
    # Test High Confidence
    context_high = {"cluster_id": "RING_001", "confidence": 0.95}
    decision_high = agent.decide_action(context_high)
    assert decision_high["selected_action"] == AgentAction.FREEZE_PAYOUT_TEMP.value
    assert "High confidence" in decision_high["justification"]
    
    # Test Medium Confidence
    context_mid = {"cluster_id": "RING_002", "confidence": 0.75}
    decision_mid = agent.decide_action(context_mid)
    assert decision_mid["selected_action"] == AgentAction.DELAY_PAYOUT.value
    assert "Repeated behavioral anomalies" in decision_mid["justification"]
    
    # Test Low Confidence
    context_low = {"cluster_id": "RING_003", "confidence": 0.45}
    decision_low = agent.decide_action(context_low)
    assert decision_low["selected_action"] == AgentAction.MONITOR.value
    assert "Low risk detected" in decision_low["justification"]
    
    print("Agentic Engine tests passed!")

if __name__ == "__main__":
    test_agentic_engine_decisions()
