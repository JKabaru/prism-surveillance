from typing import List, Dict, Optional
import enum

class ConfidenceTier(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class AgentAction(enum.Enum):
    MONITOR = "monitor"
    ANNOTATE = "annotate"
    LOG = "log"
    DELAY_PAYOUT = "delay_payout"
    NOTIFY = "notify"
    INCREASE_SCRUTINY = "increase_scrutiny"
    FREEZE_PAYOUT_TEMP = "freeze_payout_temp"
    LOCK_ESCALATION = "lock_escalation"
    ESCALATE_REVIEW = "escalate_review"

class PRISMAgenticEngine:
    """
    Core engine for managing agentic autonomy within authorized operational envelopes.
    """
    
    ACTION_ENVELOPES = {
        ConfidenceTier.LOW: [AgentAction.MONITOR, AgentAction.LOG, AgentAction.ANNOTATE],
        ConfidenceTier.MEDIUM: [AgentAction.INCREASE_SCRUTINY, AgentAction.DELAY_PAYOUT, AgentAction.NOTIFY],
        ConfidenceTier.HIGH: [AgentAction.FREEZE_PAYOUT_TEMP, AgentAction.LOCK_ESCALATION, AgentAction.ESCALATE_REVIEW]
    }

    def __init__(self):
        self.history: List[Dict] = []

    def get_authorized_actions(self, confidence: float) -> List[AgentAction]:
        """Returns allowed actions based on confidence score."""
        tier = self._get_tier(confidence)
        # Higher tiers include lower tier actions
        actions = []
        if tier == ConfidenceTier.HIGH:
            actions.extend(self.ACTION_ENVELOPES[ConfidenceTier.HIGH])
            actions.extend(self.ACTION_ENVELOPES[ConfidenceTier.MEDIUM])
            actions.extend(self.ACTION_ENVELOPES[ConfidenceTier.LOW])
        elif tier == ConfidenceTier.MEDIUM:
            actions.extend(self.ACTION_ENVELOPES[ConfidenceTier.MEDIUM])
            actions.extend(self.ACTION_ENVELOPES[ConfidenceTier.LOW])
        else:
            actions.extend(self.ACTION_ENVELOPES[ConfidenceTier.LOW])
        return actions

    def decide_action(self, context: Dict) -> Dict:
        """
        Maps FraudClusterAgentContext to AgentDecisionRecord.
        
        context: {
            "cluster_id": str,
            "confidence": float,
            "human_available": bool,
        Determines the most effective authorized action based on confidence.
        Returns a detailed decision record with reasoning logs for transparency.
        """
        confidence = context.get('confidence', 0.0)
        cluster_id = context.get('cluster_id', 'unknown')
        
        # Reasoning Step 1: Filter Authorization
        authorized = self.get_authorized_actions(confidence)
        tier = self._get_tier(confidence)
        
        reasoning_logs = [
            f"Analyzing risk for cluster {cluster_id}...",
            f"Calculated confidence: {confidence:.2f} ({tier.value} Tier)",
            f"Authorized actions for this tier: {[a.value for a in authorized]}"
        ]
        
        # Reasoning Step 2: Policy Alignment
        selected_action = AgentAction.MONITOR
        if tier == ConfidenceTier.HIGH:
            selected_action = AgentAction.FREEZE_PAYOUT_TEMP
            reasoning_logs.append("High confidence threshold met. Escalating to TEMPORARY_FREEZE.")
        elif tier == ConfidenceTier.MEDIUM:
            selected_action = AgentAction.DELAY_PAYOUT
            reasoning_logs.append("Medium confidence detected. Applying DELAY_PAYOUT policy for review.")
        else:
            reasoning_logs.append("Low confidence/insufficient evidence. Maintaining MONITOR state.")
        
        # Reasoning Step 3: Reversibility Audit
        decision = {
            "selected_action": selected_action.value,
            "justification": self._generate_justification(selected_action, context),
            "confidence_alignment": f"Aligned with {tier.value} confidence envelope",
            "reasoning_logs": reasoning_logs,
            "reversibility_note": "Action is time-bounded (72h) and fully reversible.",
            "action_duration_hours": 72,
            "required_human_followup": True,
            "generated_artifacts": ["investigation_brief", "network_graph"],
            "interjected": False,
            "status": "EXECUTED"
        }
        
        self.history.append({
            "cluster_id": cluster_id,
            "decision": decision,
            "timestamp": "2026-02-07" # Simplified
        })
        
        return decision

    def _get_tier(self, confidence: float) -> ConfidenceTier:
        if confidence >= 0.9:
            return ConfidenceTier.HIGH
        elif confidence >= 0.7:
            return ConfidenceTier.MEDIUM
        else:
            return ConfidenceTier.LOW

    def _generate_justification(self, action: AgentAction, context: Dict) -> str:
        if action == AgentAction.FREEZE_PAYOUT_TEMP:
            return f"High confidence correlation ({context.get('confidence', 0)*100:.1f}%) warrants immediate containment to limit financial exposure."
        if action == AgentAction.DELAY_PAYOUT:
            return f"Repeated behavioral anomalies detected. Delaying payout for secondary validation."
        return "Low risk detected. Continuing observational monitoring."
