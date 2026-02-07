# PRISM — Synthetic Data Generation Framework
### Tailored for Fraud Detection Prototyping & Hackathon Demos

---

## 1. Core Principles of the Data Framework

### Hierarchical Structure
* **Chain:** Master Partner → Sub-Affiliate → Clients.
* **Metadata:** Each layer contains IDs, locations, joining dates, and tiers.
* **Goal:** Enables deep network-based fraud detection and multi-level attribution.



### Event-Centric Temporal Data
* **Events:** Trade execution, deposits, withdrawals, and bonus claims.
* **Precision:** Millisecond-level timestamps to simulate "lockstep" behavior.
* **Coherence:** Legitimate activity remains statistically coherent and randomized.

### Realistic Distributions
* **Trade Volumes:** Mimic real synthetic indices or forex market distributions.
* **Financials:** Varying deposit frequencies and amounts per client.
* **Platform Rules:** Bonus claims follow logic such as "minimum trade volume before withdrawal."

### Fraud Pattern Injection
* **Opposite Trading:** Pairs or groups with inverse trade directions on the same instrument.
* **Mirror Trading:** Synchronized entries/exits across different sub-affiliates.
* **Bonus Abuse:** The "Deposit → Minimal Trade → Immediate Withdrawal" chain.
* **Commission Inflation:** High referral-to-trade ratios within specific sub-networks.

### Noise, Variance, and Labeling
* **Human Element:** Random time offsets and activity gaps to mimic realistic behavior.
* **Detection Testing:** Tagging events with `fraud_type`, `fraud_ring_id`, and `master_partner_id` for precision/recall evaluation.

---

## 2. Recommended Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python | Core generation and manipulation logic. |
| **Data Logic** | Pandas / NumPy | Structured tables and time-series simulation. |
| **Graphing** | NetworkX | Simulating partner/sub-affiliate relationship graphs. |
| **Mock Data** | Faker | Generating realistic names, emails, and IDs. |
| **Export** | CSV / Parquet | Standard formats for PRISM ingestion and API simulation. |

---

## 3. Synthetic Data Generation Pipeline

### Step 1: Define Entities
* **Master Partners:** 5–10 entities.
* **Sub-Affiliates:** 3–5 per Partner.
* **Clients:** 10–50 per Sub-Affiliate.

### Step 2: Generate Legitimate Activity
* Simulate random deposits and trades with realistic volatility.
* Distribute volume from small to medium sizes.

### Step 3: Inject Fraud Patterns
* **Opposite Trading:** Match client pairs across affiliates; invert their trades.
* **Mirror Trading:** Synchronize trades with a $\pm 5\text{ms}$ noise jitter.
* **Commission Gaming:** Inflate activity specifically within one sub-affiliate network.

### Step 4: Add Noise & Validate
* Introduce random outliers and timezone/geo offsets.
* Validate the distribution (e.g., 5% fraud vs. 95% legitimate).
* Generate summary metrics: Average commission, trades per client, and cluster counts.

---

## 4. Advanced Enhancements & Stress Testing
* **Dynamic Evolution:** Fraud rings that form gradually over days/weeks.
* **Market Integration:** Price movements and volatility events that trigger specific trade patterns.
* **Scale Testing:** Generating 1000+ clients and 50+ sub-affiliates to stress-test the temporal correlation engine.

---

## 5. Deliverables for Hackathon Use
* **Datasets:** Ready-to-use CSV/Parquet files with realistic trading logs.
* **Visual Structures:** Graph data for fraud network mapping.
* **Live Configs:** Parameters to adjust fraud intensity during the demo.
* **Evaluation Labels:** Ground-truth labels to calculate AI precision and recall.

---

## ✅ Outcome
Using this framework:
1.  **PRISM** can ingest, detect, and visualize fraud rings in realistic conditions.
2.  **Judges** can witness lockstep behavior and multi-level attribution in real-time.
3.  **End-to-End Flow:** The solution works without requiring access to sensitive live data.
4.  **Dramatic Impact:** Full control over fraud complexity allows for a compelling, high-stakes demonstration.