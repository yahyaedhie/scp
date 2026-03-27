 **TRI (Task Reliability Index)** and **CQS (Compression Quality Score)**

---

## 🔍 Task Reliability Index (TRI)
- **Definition**: Measures how well compressed output preserves the *intended meaning* of the original input.  
- **Scale**: 0.0 → 1.0 (higher = more reliable).  
- **Focus**: Semantic fidelity.  
- **Examples**:  
  - Text: Does “OBJ1.0 = person” still convey the same meaning as “a person”?  
  - Image: Are the compressed patches still recognizable as “forest” and “person”?  
  - Video: Is the motion anchor “running” preserved across frames?  

**Interpretation**:  
- TRI ≥ 0.90 → High reliability (safe for governance).  
- TRI 0.70–0.89 → Acceptable, but some detail loss.  
- TRI < 0.70 → Risk of semantic drift; needs review.

---

## 🔍 Compression Quality Score (CQS)
- **Definition**: Balances *efficiency vs accuracy* — how much compression was achieved without unacceptable loss.  
- **Scale**: 0.0 → 1.0 (higher = better balance).  
- **Focus**: Trade‑off between token savings and fidelity.  
- **Examples**:  
  - Text: Did shorthand codes save tokens without confusing expansion?  
  - Image: Did patch compression reduce background noise without losing key objects?  
  - Video: Did frame reduction preserve motion clarity?  

**Interpretation**:  
- CQS ≥ 0.85 → Strong balance (efficient + accurate).  
- CQS 0.70–0.84 → Moderate balance (some loss tolerated).  
- CQS < 0.70 → Efficiency too aggressive; meaning compromised.

---

## ⚖️ Relationship Between TRI & CQS
- **TRI** = “Did we keep the meaning intact?”  
- **CQS** = “Did we compress efficiently without breaking meaning?”  
- Together, they form the **audit trail**:  
  - High TRI + High CQS → Ideal (accurate + efficient).  
  - High TRI + Low CQS → Accurate but inefficient (not enough compression).  
  - Low TRI + High CQS → Efficient but risky (meaning drift).  
  - Low TRI + Low CQS → Failure case (neither efficient nor accurate).  

---

## 📊 Example from Our Session
- Text: TRI 0.95, CQS 0.92 → Excellent fidelity + efficiency.  
- Image: TRI 0.90, CQS 0.88 → Strong, but background detail compressed.  
- Video: TRI 0.85, CQS 0.79 → Motion preserved, but frame detail reduced.  
- Combined: TRI 0.90, CQS 0.88 → Balanced across modalities.  

---

👉 In short: **TRI tells you if meaning survived compression; CQS tells you if the compression was worth it.** Together, they make SCP auditable and governance‑ready.  

Would you like me to **design a scoring rubric table** (like a checklist) that shows thresholds and what actions to take depending on TRI and CQS levels? That would give you a practical tool for evaluating SCP runs.

---

Here’s a **draft of the TRI & CQS Evaluation Protocol** — a step‑by‑step guide that any model or human reviewer can follow to calculate and interpret scores during SCP runs. It’s designed to be transferable across systems:

---

# 📑 TRI & CQS Evaluation Protocol (Draft)

## 1. Purpose
To provide a standardized method for evaluating **Task Reliability Index (TRI)** and **Compression Quality Score (CQS)** in SCP compression runs, ensuring fidelity, efficiency, and governance transparency.

---

## 2. Definitions
- **TRI (Task Reliability Index)**: Measures semantic fidelity — how well the compressed output preserves the intended meaning.  
- **CQS (Compression Quality Score)**: Measures efficiency vs accuracy — how well compression reduces tokens without unacceptable loss.

---

## 3. Scoring Procedure

### Step 1: Identify Anchors
- Extract anchors (e.g., `OBJ1.0 = person`, `ACT1.0 = running`).  
- Confirm anchors represent the core meaning of the input.

### Step 2: Compare Original vs Compressed
- Text: Check if compressed shorthand expands correctly.  
- Image: Check if compressed patches still represent key objects.  
- Video: Check if reduced frames preserve motion anchors.

### Step 3: Assign TRI
- 1.0 = Perfect fidelity (no meaning lost).  
- 0.90–0.99 = High fidelity (minor detail loss).  
- 0.70–0.89 = Acceptable fidelity (review needed).  
- <0.70 = Drift risk (reject or revise).

### Step 4: Calculate CQS
- Formula:  
  \[
  CQS = \frac{\text{Token Savings %} + \text{TRI}}{2}
  \]  
- Adjust for modality (text, image, video).  
- Interpret balance:  
  - ≥0.85 = Strong balance.  
  - 0.70–0.84 = Moderate balance.  
  - <0.70 = Poor balance.

### Step 5: Log Results
- Record TRI and CQS per modality.  
- Record combined TRI and CQS across modalities.  
- Add narrative audit notes (router decisions, anchor expansions, observed losses).

---

## 4. Rubric for Action
| **TRI Range** | **CQS Range** | **Action** |
|---------------|---------------|------------|
| ≥0.90         | ≥0.85         | Approve, governance‑ready |
| 0.70–0.89     | 0.70–0.84     | Accept with caution, review detail loss |
| 0.50–0.69     | Any           | Flag for revision |
| <0.50         | Any           | Reject compression run |

---

## 5. Governance Notes
- **Transparency**: Always log TRI & CQS with anchors.  
- **Auditability**: Store results in session audit logs.  
- **Cross‑Model Transferability**: Protocol applies equally to text‑only, vision, or multi‑modal systems.  

---

## 6. Example (From Current Session)
- Text: TRI 0.95, CQS 0.92 → Approved.  
- Image: TRI 0.90, CQS 0.88 → Approved.  
- Video: TRI 0.85, CQS 0.79 → Accept with caution.  
- Combined: TRI 0.90, CQS 0.88 → Governance‑ready.

---

👉 This protocol makes TRI & CQS **portable across models** — any system can calculate, interpret, and log them consistently.  

Would you like me to **extend this into a formal “Evaluator’s Checklist”** (bullet‑point format) so reviewers can quickly apply TRI & CQS scoring without reading the full protocol?
