
## 🧩 SCP‑Router Domain Rules 

### 1. **Domain Activation**
- Each session begins with a **domain flag** (e.g., `finance`, `education`, `governance`).  
- Rule: Only anchors, compression rules, and TRI/CQS thresholds relevant to the active domain are loaded.  
- Example:  
  - Domain = `finance` → `[INFLATION]`, `[LIQ]`, `[CARRY]`.  
  - Domain = `education` → `[QUIZ]`, `[FLASHCARD]`, `[CURRICULUM]`.  
  - Domain = `governance` → `[AUDIT]`, `[CHECKLIST]`, `[COMPLIANCE]`.

---

### 2. **Anchor Registry per Domain**
- Rule: Each domain maintains its own **anchor registry**.  
- Anchors must be unique within a domain, but can overlap across domains with different expansions.  
- Example:  
  - `[INFLATION]` in **finance** → “price level increase.”  
  - `[INFLATION]` in **cosmology** → “expansion of the universe.”  

---

### 3. **TRI/CQS Thresholds per Domain**
- Rule: TRI/CQS scoring adapts to domain complexity.  
- Example thresholds:  
  - **Finance** → TRI ≥ 0.85, CQS ≥ 0.80.  
  - **Education** → TRI ≥ 0.90 (higher fidelity needed for teaching).  
  - **Governance** → TRI ≥ 0.95, CQS ≥ 0.85 (strict compliance).  

---

### 4. **Routing Logic per Domain**
- Rule: Routing decisions adapt to domain context.  
- Example:  
  - **Finance** → factual queries → Pre‑Search (market data).  
  - **Education** → conceptual queries → AI Model (explanations, quizzes).  
  - **Governance** → mixed queries → AI Model + Audit Trail (compliance check).  

---

### 5. **Audit Trail per Domain**
- Rule: Session reports must include domain flag.  
- Anchors, TRI/CQS scores, routing decisions, and token savings logged separately per domain.  
- Governance dashboard shows domain‑specific performance.  

---

### ⚖️ Repo vs Future Rule Snapshot

| Feature                | Repo (Current)                          | Future Rule (Phase 3+)                          |
|-------------------------|-----------------------------------------|------------------------------------------------|
| Domain Activation       | Single domain (finance anchors only)    | Multi‑domain flags (finance, education, governance) |
| Anchor Registry         | SQLite store with seed anchors          | Separate registries per domain, overlapping allowed |
| TRI/CQS Thresholds      | Not implemented                         | Domain‑specific thresholds (strict for governance) |
| Routing Logic           | Proxy to Claude only                    | Domain‑aware routing (finance → search, education → AI, governance → audit) |
| Audit Trail             | Token savings report only               | Domain‑tagged logs with TRI/CQS + routing decisions |

