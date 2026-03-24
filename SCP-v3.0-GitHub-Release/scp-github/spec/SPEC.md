# SCP v3.0 — Full Protocol Specification

`/spec/SPEC.md` | version: 3.0 | status: stable

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

---

## 3. Architecture — 4 Layers

### L1 — Compression Layer

Four compression modes:

| Mode | Description | Use Case |
|---|---|---|
| **Light** | Minimal shorthand, maximum clarity | Onboarding, first use |
| **Moderate** | Shorthand + anchors, balanced | Default |
| **Deep** | Semantic hashes, ultra-compact | Stable long sessions |
| **Adaptive** | Dynamic — adjusts to ambiguity + drift risk | Recommended |

### L2 — Semantic Layer

- **Semantic Compression Graph (SCG)** — maps all shorthand, anchors, hashes, relationships
- **Anchors** — canonical definition containers
- **Drift Firewall** — detects conflict, corruption, contamination

### L3 — Memory Layer

- **Versioning** — all shorthand versioned
- **Lineage tracking** — evolution of meaning over versions
- **Hashes** — version-pinned identifiers (e.g. WAR1.0)

### L4 — Interoperability Layer

- **SPF packets** — portable JSON-like semantic units
- **Multi-model sync** — meaning stable across vendors
- **Agent compatibility** — agents interpret, validate, relay packets

---

## 4. Shorthand Format

```
{
  "id": "<unique-id>",
  "type": "shorthand",
  "label": "[CODE]",
  "expansion": "Full human-readable meaning",
  "domain": ["domain1", "domain2"],
  "anchor": "CODE-ANCHOR",
  "version": "3.0",
  "hash": "CODE1.0",
  "metadata": {
    "created": "v3.0",
    "stability": "low|medium|high",
    "validation": {
      "status": "valid|invalid|fallback",
      "confidence": "low|medium|high",
      "last_checked": "YYYY-MM-DD"
    }
  }
}
```

---

## 5. Anchor Format

```
{
  "id": "CODE-ANCHOR",
  "type": "anchor",
  "label": "Human readable label",
  "definition": "Canonical definition — precise, unambiguous.",
  "constraints": ["constraint 1", "constraint 2", "constraint 3"],
  "goals": ["goal 1", "goal 2"],
  "domain_profiles": {
    "domain1": "domain-specific expansion",
    "domain2": "domain-specific expansion"
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
{
  "type": "shorthand",
  "code": "[CODE]",
  "expansion": "Full expansion text",
  "version": "3.0",
  "anchor": "CODE-ANCHOR",
  "domain": ["domain1"],
  "hash": "CODE1.0",
  "metadata": {
    "created": "v3.0",
    "stability": "high",
    "validation": {
      "status": "valid",
      "confidence": "high",
      "last_checked": "YYYY-MM-DD"
    }
  }
}
```

---

## 7. Bootstrap Structure

### Tier 1 — Nano System Prompt (~180 tokens)
Always load. Contains: role + rules + locked codes.

### Tier 2 — Anchor Pack (~100 tokens per anchor)
Load at session start or on-demand per shorthand.

### Tier 3 — SPF Packets (~70 tokens per packet)
Use for cross-model handoff or cold-start context.

### SPF::REFRESH (~80 tokens)
Inject mid-session every ~50 turns to re-anchor.

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

## 11. SCV Extension (Optional)

SCV adds validation intelligence on top of SCP:

- Validation status per shorthand (valid/invalid/fallback)
- Confidence scoring (low/medium/high)
- Validation lineage tracking
- Enterprise compliance metadata

See `/spec/SCV-Extension.md` for full SCV specification.

---

## 12. Domain Profiles

Domains scope shorthand meaning:

| Domain | Description |
|---|---|
| `market` | Financial markets, trading, macro |
| `technical` | Software, architecture, engineering |
| `education` | Learning, teaching, institutional |
| `msme` | Small/medium business contexts |
| `community` | Social, collaborative, network |
| `scp_meta` | SCP protocol itself |

---

*Full schema: `/spec/Semantic-Graph-Schema.json`*
*SPF format: `/spec/SPF-Packet-Format.md`*
