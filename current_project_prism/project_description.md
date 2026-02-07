# PRISM — Predictive Risk & Instability Surveillance Module
## AI-Powered Partner & Affiliate Fraud Detection

---

## 📖 Executive Summary
**PRISM** is an AI-powered partner fraud intelligence system that detects coordinated affiliate fraud by analyzing networks, timing correlations, and business behavior patterns rather than isolated transactions. 

It identifies fraud rings spanning multiple affiliates and sub-affiliate levels, automatically assembles defensible evidence packages, and enables **same-day fraud containment** instead of multi-week manual investigations. PRISM is designed specifically for partner fraud scenarios where activity is relational, deliberate, and engineered to stay below traditional detection thresholds.

---

## 🛑 The Problem
> **Partner and affiliate fraud is not client fraud.**

Unlike typical client-side theft, fraudulent partners exploit commission structures and referral incentives. They understand the rules, distribute activity across dozens of accounts, and deliberately remain just under single-account detection thresholds.

### Key Fraud Patterns at Scale:
* **Coordinated opposite trading** across multiple affiliates.
* **Mirror trading** with identical timing across “unrelated” clients.
* **Bonus abuse** via deposit–trade–withdraw behavior.
* **Commission inflation** through sub-affiliate gaming.

The core challenge is not alerting—it is **attribution and proof**. By the time patterns are manually uncovered, commissions have already been paid. Partner fraud is relational and pattern-based, not transactional—and manual review cannot scale.

---

## 💡 Core Insight
**Independent partners and clients cannot repeatedly behave as a synchronized system over time.**

PRISM detects fraud by identifying persistent temporal coordination and behavioral similarity across accounts that should be independent. This shifts the detection paradigm from:
* **"Is this account suspicious?"** to
* **"Which network is acting as one entity, and who controls it?"**



---

## ⚙️ Core Capabilities

### 1. Network-Based Fraud Detection
PRISM continuously analyzes trade logs to detect:
* **Opposite trading:** Accounts opening opposite positions on the same instrument within $\leq 1$ second.
* **Mirror trading:** Accounts trading the same instruments with highly correlated entry/exit timing.
* **Temporal correlation:** Repeated synchronization across dozens of events.

Detected accounts are clustered and mapped through the full hierarchy:  
**Client → Sub-Affiliate → Partner.**

### 2. Business Behaviour Analysis
PRISM evaluates partner-level behavior, not just trades:
* **Bonus abuse patterns:** Deposit → minimal trade → immediate withdrawal.
* **Client quality scoring:** Retention, trade diversity, and lifecycle depth.
* **Commission anomalies:** Earnings inconsistent with organic volume and retention.

### 3. Explainable Investigation Support
For each detected fraud ring, PRISM automatically generates a complete investigation package:
* **Fraud hypothesis:** Plain English summary of the scheme.
* **Network graph:** Visual partner attribution mapping.
* **Timeline:** Chronological evidence of coordinated behavior.
* **Confidence score:** Based on matched indicators and statistical correlation.

#### Example Output:
> **High Confidence (92%)** > **Scheme:** Coordinated Opposite Trading  
> **Scope:** 7 partners, 23 sub-affiliates, 184 clients  
> **Estimated Exposure:** $8,400  
> **Action:** Freeze affiliate payouts; escalate for review.

### 4. Proactive Pattern Discovery
PRISM establishes historical baselines for healthy partner behavior. When a partner’s behavior shifts into a regime matching known fraud signatures, it triggers a **pre-fraud signal**, enabling intervention before losses scale.

---

## 🤖 Autonomous Operation with Human Authority
PRISM balances speed with defensibility:
* **Detection & Evidence:** Fully automated to avoid investigation bottlenecks.
* **Containment:** Confidence-tiered actions prevent overreaction.
* **Governance:** Human reviewers audit, override, and refine thresholds.

---

## 🏗️ Technical Stack (Live Demo Scope)

| Component | Technology |
| :--- | :--- |
| **Backend** | Python (FastAPI) |
| **Analysis** | Pandas / NumPy (Temporal correlation engine) |
| **Mapping** | NetworkX (Hierarchy + fraud cluster attribution) |
| **AI Layer** | DeepSeek via OpenRouter (Evidence synthesis) |
| **Frontend** | Streamlit (Rapid dashboarding) |

### Demo "Steel Thread" Workflow:
**Coordinated trading → Network mapping → Evidence synthesis → Actionable Brief.**

---

## 🤖 PRISM — Agentic AI Design Addendum

### Reframing the AI Contract for Autonomous-When-Unattended Operation
*This replaces the previous “explain-only” guarantee while staying enterprise-defensible.*

#### 1. Reframed Principle
**PRISM’s AI may act autonomously only within pre-authorized, reversible, confidence-bounded operational envelopes — and must always leave a complete evidentiary trail for later human judgment.**

This enables agent-like behavior without surrendering control.

#### 2. Agent Responsibility Boundaries
*   **Allowed:** Advance investigation state, trigger pre-approved containment (e.g., temp freeze), escalate monitoring, generate investigation artifacts.
*   **Never Allowed:** Declare fraud conclusively, permanently penalize partners, modify commission rules, override policy thresholds, take irreversible actions.

#### 3. Action Envelope Model
PRISM uses confidence-tiered autonomy envelopes:
*   **Low Confidence:** Observational (Log, monitor, annotate).
*   **Medium Confidence:** Preventive (Increase scrutiny, delay payouts, notify).
*   **High Confidence:** Containment (Temporarily freeze payouts, lock escalation).

*All autonomous actions are policy-defined, time-bounded, and reversible.*

#### 4. Corrected Design Guarantee
PRISM’s AI can autonomously progress investigations and execute reversible containment actions within pre-approved policy boundaries, while reserving final judgment and irreversible decisions for humans. This is true agent behavior, not a chatbot.