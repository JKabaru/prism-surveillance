# PRISM — Product Requirements Document (PRD)
## AI-Powered Partner & Affiliate Fraud Detection
**Status:** Ideation Mode · Long-Term Reference

---

## 1. Problem Definition
### 1.1 Core Problem
Partner and affiliate fraud operates as coordinated systems, not isolated bad actors. Existing detection approaches focus on single-account anomalies, which are insufficient against adversaries who:
* **Distribute activity** across many clients and sub-affiliates.
* **Operate just below** per-account thresholds.
* **Exploit mechanics** (commission, bonus, referral) intentionally.
* **Design behavior** to look “statistically normal” in isolation.

**The result:** Late detection, weak attribution, and post-payment losses.

### 1.2 Explicit Problem Statement
The organization lacks a scalable way to:
1.  Detect persistent coordination across accounts that should be independent.
2.  Attribute suspicious behavior to a controlling partner or network.
3.  Assemble defensible, explainable proof quickly enough to act before payouts.

> **Key takeaway:** This is not an alerting problem. It is an **attribution + evidence + timing** problem.

---

## 2. Intended Users & Operating Constraints
### 2.1 Primary Users
* **Partner Risk / Fraud Analysts:** Need fast, defensible insight; cannot manually investigate large graphs.
* **Compliance & Audit Stakeholders:** Require explainability and traceability to justify actions.
* **Risk Leadership:** Needs confidence-weighted decisions, not raw alerts.

### 2.2 Constraints
* **No fully autonomous punitive actions:** Human authority is always required.
* **Explainability:** Evidence must be auditable.
* **Scale:** Must handle hierarchical partner structures beyond manual review capacity.

---

## 3. Assumptions & Unknowns
### 3.1 Assumptions
* Trade-level timestamps and affiliate attribution data exist.
* Affiliate hierarchies are known (**Client → Sub-Affiliate → Partner**).
* Repeated temporal coordination across independent accounts is statistically rare and indicates fraud.

### 3.2 Unknowns
* Acceptable false-positive rate per confidence tier.
* Variance in "normal" trading behavior across different regions.
* Latency tolerance between detection and necessary action.

---

## 4. Product Scope & Non-Goals
### 4.1 In Scope
* Detection of coordinated partner behavior.
* Network-based attribution and clustering.
* Automated evidence assembly (Briefs/Graphs).
* Analyst-facing investigation interface.

### 4.2 Explicit Non-Goals
* Client KYC or individual identity fraud detection.
* Real-time trade blocking.
* Black-box ML decisioning without explanation.

---

## 5. Phased Development Roadmap

### Phase 0 — Framing & Baselines
* **Goal:** Define “normal” partner behavior.
* **Tasks:** Identify baseline metrics for trade timing, lifecycle depth, and retention curves.

### Phase 1 — Steel Thread #1 (Core Demo)
* **Goal:** Prove end-to-end value on one fraud pattern.
* **Scope:** Input logs → Detect mirror trading → Cluster networks → Output evidence package.

### Phase 2 — Business Behavior Layer
* **Goal:** Differentiate fraud from legitimate high performance.
* **Tasks:** Bonus abuse detection, commission vs. retention inconsistency analysis.

### Phase 3 — Proactive Detection
* **Goal:** Move from reactive to predictive.
* **Tasks:** Historical baselining per partner and regime shift detection.

### Phase 4 — Learning & Refinement
* **Goal:** System improves with use.
* **Tasks:** Capture confirmed cases for threshold tuning; feedback loop into detection logic.

---

## 6. Success Metrics & Failure Conditions
### 6.1 Success Metrics
* **Time to attribution:** Reduced from weeks to minutes.
* **Pre-payout detection rate:** % of fraud caught before commission is paid.
* **Explainability score:** Reviewer confidence without needing to escalate.

### 6.2 Failure Conditions
* High-confidence flags are routinely overturned by humans.
* Detection consistently lags behind payout dates.
* System generates alerts without clear attribution to a partner.

---

## 7. Confidence & Action Framework
Human override is mandatory at all tiers.

| Confidence Tier | Characteristics | Allowed Actions | AI Autonomy Level |
| :--- | :--- | :--- | :--- |
| **Low** | Weak correlation, limited repetition | Log, monitor, annotate | Observational |
| **Medium** | Repeated patterns, partial attribution | Increase scrutiny, delay payouts, notify | Preventive |
| **High** | Persistent coordination, clear hierarchy | Temporarily freeze payouts, lock escalation | Containment |

---

## 8. Agent Responsibility Boundaries
### 8.1 What the AI Agent Is Allowed to Do
*   Advance an investigation state.
*   Trigger pre-approved, reversible containment actions.
*   Escalate monitoring intensity.
*   Queue cases for priority human review.
*   Generate and attach official investigation artifacts.

### 8.2 What the AI Agent Is Never Allowed to Do
*   Declare fraud conclusively.
*   Permanently penalize partners.
*   Modify commission rules.
*   Override policy thresholds.
*   Take irreversible actions.

---

## 9. Updated AI Agent Contracts
### 9.1 Input Object: `FraudClusterAgentContext`
Requires `cluster_id`, `confidence_tier`, `authorized_actions`, and `operational_state` (e.g., `human_available: false`).

### 9.2 Output Object: `AgentDecisionRecord`
The agent outputs a machine-executable `AgentDecisionRecord` including `selected_action`, `justification`, and `required_human_followup: true`.


---

## 8. Evidence Standards (Non-Negotiable)
Each investigation **must** include:
1.  **Plain-English** fraud hypothesis.
2.  **Visual network** attribution.
3.  **Temporal evidence** of coordination.
4.  **Statistical support** (not just heuristics).
5.  **Commission exposure** estimate.

---

## 9. Long-Term Vision
PRISM is a decision-support system for adversarial partner behavior. Its success is measured by earlier intervention, stronger defensibility, and reduced financial risk. 

**The system should make one thing easy: Answering “Who is really behind this behavior?” with confidence.**