# SCP v3.0 — Protocol Specification (Quick Reference)

`/spec/SPEC.md` — Version 3.0 · March 2026

> **Full technical specification:** [`/spec/SCP_v3_0_Specification.md`](spec/SCP_v3_0_Specification.md)

---

## 1. Purpose

SCP (Semantic Compression Protocol) defines a standard for:
- Compressing meaning into shorthand codes
- Anchoring codes to canonical definitions
- Preventing semantic drift across sessions and models
- Packaging meaning as portable units (SPF packets)
- Reducing token usage at inference time

---

## 2. Core Principles

| Principle | Rule |
|---|---|
| **Determinism** | shorthand + domain → fixed meaning always |
| **Anchor binding** | every shorthand must link to an anchor |
| **Drift transparency** | flag drift — never silently correct |
| **Validation first** | validate before compressing |
| **Domain isolation** | codes are scoped to domains |
| **Error transparency** | invalid shorthand must be logged, not inferred |
| **Meaning preservation** | compression must not alter intent or constraints |

---

## 3. Architecture — 4 Layers

```
L1 — Compression Layer    shorthand modes (light / moderate / deep / adaptive)
L2 — Semantic Layer       SCG + anchors + drift firewall
L3 — Memory Layer         versioning + lineage + semantic hashes
L4 — Interoperability     SPF packets + multi-model + agent compatibility
```

---

## 4. Shorthand Format

```json
{
  "code": "[CODE]",
  "expansion": "Full human-readable meaning",
  "domain": "active-domain",
  "anchor": "CODE-ANCHOR",
  "version": "3.0",
  "hash": "CODE1.0",
  "metadata": {
    "created": "v3.0",
    "stability": "low|medium|high"
  }
}
```

---

## 5. Anchor Format

```json
{
  "id": "CODE-ANCHOR",
  "type": "anchor",
  "label": "Human readable label",
  "definition": "Canonical definition — precise, unambiguous.",
  "constraints": ["constraint 1", "constraint 2", "constraint 3"],
  "goals": ["goal 1", "goal 2"],
  "domain_profiles": {
    "domain1": "domain-specific expansion"
  },
  "versions": ["CODE1.0"],
  "links": ["RELATED-ANCHOR"],
  "metadata": {
    "created": "v3.0",
    "stability": "high"
  }
}
```

---

## 6. SPF Packet Format

```json
SPF {
  "code": "[CODE]",
  "expansion": "Full expansion text",
  "domain": "domain",
  "anchor": "CODE-ANCHOR",
  "hash": "CODE1.0",
  "version": "3.0",
  "constraints": ["c1", "c2"],
  "metadata": { "stability": "high" }
}
```

---

## 7. Bootstrap Tiers

| Tier | Purpose | Tokens |
|---|---|---|
| **T1** — Nano System Prompt | Always load. Role + rules + locked codes | ~180 |
| **T2** — Anchor Pack | Load at session start. Full anchor definitions | ~420 |
| **T3** — SPF Packets | Cross-model handoff or cold-start context | ~420 |
| **SPF::REFRESH** | Mid-session re-anchor (every ~20+ turns) | ~80 |

---

## 8. Workflow

```
1. Classify     → input type + active domain
2. Graph lookup → shorthand → anchor match
3. Validate     → expansion matches anchor constraints
4. Compress     → adaptive mode selection
5. Anchor-expand → resolve codes to full meaning
6. Drift check  → firewall validation
7. Package      → SPF if cross-model, direct if single
```

---

## 9. Error Codes

| Code | Trigger | Action |
|---|---|---|
| `[UNKNOWN-CODE]` | Shorthand not in dictionary | Request definition |
| `[ANCHOR-NOT-LOADED]` | Anchor missing from context | Do not infer |
| `[DRIFT-DETECTED]` | Expansion varies across runs | Halt + report |
| `[HASH-CONFLICT]` | Version mismatch detected | Reject + log |

---

## 10. Performance Targets

| Metric | Target |
|---|---|
| Token reduction | 60–80% |
| Expansion accuracy | 100% (deterministic) |
| Drift rate | Zero |
| Cross-model portability | 100% via SPF |

---

## 11. Domain Status

| Domain | State | Codes |
|---|---|---|
| `market` | Locked | `[WAR]` `[SH-C]` `[SH-S]` `[LIQ]` `[CARRY]` `[STACK]` |
| `education` | Active | `TA bot`, `ALUMNI` |
| `blockchain` | Pending | — |
| `scp_meta` | Pending | — |

---

## 12. Roadmap

| Version | Focus | Status |
|---|---|---|
| **v3.0** | Core protocol | ✅ Stable |
| **v3.1** | SCV validation extension | 🔄 In progress |
| **v3.2** | SCP Router (FastAPI middleware) | 🔄 In progress |
| **v3.3** | Blockchain integration | ⏳ Planned |
| **v4.0** | Semantic Router infrastructure | ⏳ Planned |
| **v5.0+** | Semantic Network Layer | ⏳ Deferred |

---

## Related Documents

| Document | Path |
|---|---|
| **Full Technical Specification** | [`/spec/SCP_v3_0_Specification.md`](SCP_v3_0_Specification.md) |
| **SPF Packet Format** | [`/spec/SPF-Packet-Format.md`](SPF-Packet-Format.md) |
| **Semantic Graph Schema** | [`/spec/Semantic-Graph-Schema.json`](Semantic-Graph-Schema_json.md) |
| **SCV Validation Extension** | [`/spec/SCV-Extension.md`](SCV-Extension.md) |
| **Token Economics** | [`/docs/TOKENOMICS.md`](../docs/TOKENOMICS.md) |
| **Vision Document** | [`/VISION.md`](../VISION.md) |
| **Contributing Guide** | [`/CONTRIBUTING.md`](../CONTRIBUTING.md) |

---

*SCP v3.0 — github.com/yahyaedhie/scp — Apache 2.0*
