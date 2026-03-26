# SCV v3.0 — Smart Compression & Validation Extension

### _Validation Layer for SCP v3.0_

`/spec/SCV-Extension.md` — Version 3.0 · March 2026

---

## 1. Purpose

SCV v3.0 defines a **validation extension** for SCP, adding trust, compliance, and error-handling intelligence on top of the core compression protocol.

SCV is **optional**. SCP operates fully without it. Enable SCV when enterprise compliance, audit trails, or confidence-weighted compression is required.

---

## 2. What SCV Adds to SCP

| SCP (Core) | SCV (Extension) |
|---|---|
| Compression + anchors + drift firewall | + Validation status per shorthand |
| Deterministic expansion | + Confidence scoring per expansion |
| SPF packets | + Validation metadata in packets (SSPF) |
| Drift detection (flag only) | + Validation reports on drift events |
| Lineage tracking | + Validation history tracking |

---

## 3. Architecture

SCV extends SCP's four layers with validation hooks:

```
L1 — Compression Layer    + validation-gated compression
L2 — Semantic Layer       + semantic constraint checking
L3 — Memory Layer         + validation history + lineage integrity
L4 — Interoperability     + SSPF packets with validation metadata
```

---

## 4. Validation Layer

### 4.1 Validation Rules

- Every shorthand must pass **domain validation** before compression.
- Anchors must be checked against **semantic constraints**.
- Hashes must be verified against **lineage integrity**.
- Drift firewall events must trigger **validation reports**.

### 4.2 Validation Metadata

Each shorthand/anchor must include:

```json
"validation": {
  "status": "valid|invalid|fallback",
  "confidence": "low|medium|high",
  "last_checked": "2026-03-26"
}
```

**Status values:**

| Status | Meaning |
|---|---|
| `valid` | Expansion matches anchor, constraints satisfied |
| `invalid` | Expansion failed validation — reject or escalate |
| `fallback` | Anchor unavailable — using fallback expansion with reduced confidence |

**Confidence values:**

| Confidence | Criteria |
|---|---|
| `high` | Locked domain, tested on 2+ models, zero drift history |
| `medium` | Active domain, tested on 1 model, minor drift corrected |
| `low` | New code, pending verification, or fallback expansion |

### 4.3 Error Handling

| Condition | SCV Response |
|---|---|
| Unknown shorthand | Fallback expansion + `status: fallback` |
| Conflicting domains | Priority resolution + validation report |
| Corrupted hashes | Reject + log + `status: invalid` |
| Missing anchors | Infer from graph + `confidence: low` |

---

## 5. Smart Semantic Packet Format (SSPF)

SSPF extends SPF with validation metadata:

```json
SSPF {
  "type": "shorthand",
  "code": "[WAR]",
  "expansion": "War/Geopolitical Risk Premium",
  "version": "3.0",
  "anchor": "WAR-ANCHOR",
  "domain": ["market"],
  "hash": "WAR1.0",
  "validation": {
    "status": "valid",
    "confidence": "high",
    "last_checked": "2026-03-26"
  }
}
```

SSPF packets are backward-compatible with SPF. Non-SCV agents ignore the `validation` field.

---

## 6. Protocol Rules (SCV-Specific)

| Rule | Description |
|---|---|
| **Validation First** | Compression cannot proceed without validation |
| **Confidence Gating** | Low-confidence codes use lighter compression only |
| **Report on Drift** | Every drift event generates a validation report |
| **Lineage Integrity** | Validation history must be preserved across versions |
| **Error Transparency** | Invalid shorthand must be logged, not silently corrected |

---

## 7. Integration with SCP Layers

### L1 — Compression

SCV adds **validation-gated compression**:
- `high` confidence — all compression modes allowed
- `medium` confidence — light and moderate only
- `low` confidence — light only, with explicit expansion

### L2 — Semantic

SCV integrates with the Drift Firewall:
- DFW events trigger validation status updates
- Constraint violations update confidence scores
- Repeated drift on same code — auto-downgrade to `low` confidence

### L3 — Memory

SCV extends lineage tracking with validation history:

```json
"validation_history": [
  { "timestamp": "2026-03-20", "status": "valid", "confidence": "medium" },
  { "timestamp": "2026-03-24", "status": "valid", "confidence": "high" }
]
```

### L4 — Interoperability

SCV uses SSPF packets (SPF + validation metadata). Receiving agents can:
- Accept validated packets at face value
- Re-validate if their own SCV layer is active
- Ignore validation metadata if SCV is not enabled

---

## 8. Performance Impact

| Metric | SCP (without SCV) | SCV (with validation) |
|---|---|---|
| Token reduction | 60-80% | 55-75% (validation overhead) |
| Drift rate | Zero (flag-based) | Zero (validation-enforced) |
| Packet size | ~70 tokens | ~85 tokens (validation metadata) |
| Compliance | Behavioral | Auditable |

---

## 9. SCV Compliance Checklist

```
[ ] All shorthand includes validation metadata
[ ] Validation status updated on every drift event
[ ] Confidence scores gate compression mode selection
[ ] SSPF packets include validation fields
[ ] Validation history preserved in lineage tracking
[ ] Drift firewall events generate validation reports
[ ] Fallback expansions marked with reduced confidence
```

---

## 10. Future Extensions

Planned for SCV v3.1-v4.0:

- Automated validation agents
- Semantic error registries
- Confidence-weighted compression algorithms
- Enterprise compliance dashboards
- Anchor validation marketplaces
- On-chain validation receipts (blockchain integration)

---

*SCV is an optional extension of SCP v3.0.*
*Core SCP specification: `/spec/SCP_v3_0_Specification.md`*
*Apache 2.0 — github.com/yahyaedhie/scp*
