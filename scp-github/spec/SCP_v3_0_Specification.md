# SCP v3.0 — Semantic Compression Protocol

### _Full Protocol Specification_

`/spec/SCP-v3.0-Spec.md` — Version 3.0 · March 2026

---

## 1. Purpose

SCP v3.0 is an open protocol for **efficient, drift-resistant meaning transfer** between AI models, agents, and workflows.

It solves a structural inefficiency in LLM communication: every turn resends the full conversation history. Token cost compounds, context ceilings approach, and meaning drifts when anchor definitions scroll out of context — silently.

SCP compresses meaning into **shorthand codes anchored to canonical definitions**, reducing token usage by 60–80% while preserving 100% semantic accuracy across models, sessions, and agents.

---

## 2. Design Principles

| Principle | Rule |
|---|---|
| Deterministic Expansion | Same shorthand + same domain = same meaning, always |
| Anchor Binding | Every shorthand must link to a canonical anchor |
| Drift Prevention | Flag immediately — never silently correct |
| Validation First | Validate before compressing or expanding |
| Domain Isolation | Codes must not bleed across domains |
| Error Transparency | Invalid shorthand must be logged, not inferred |
| Meaning Preservation | Compression must not alter intent or constraints |

---

## 3. Architecture

SCP v3.0 is composed of four layers:

```
L1 — Compression Layer    shorthand modes (light / moderate / deep / adaptive)
L2 — Semantic Layer       SCG + anchors + drift firewall
L3 — Memory Layer         versioning + lineage + semantic hashes
L4 — Interoperability     SPF packets + multi-model + agent compatibility
```

Each layer builds on the one below. L1 can operate standalone for basic compression. Full SCP compliance requires all four layers.

---

## 4. Layer 1 — Compression Layer

### 4.1 Compression Modes

| Mode | Description | Use Case |
|---|---|---|
| **Light** | Minimal shorthand, maximum clarity | Onboarding, new collaborators |
| **Moderate** (default) | Shorthand + anchors, balanced efficiency | Standard sessions |
| **Deep** | Semantic hashes, ultra-compact | Stable context, expert users |
| **Adaptive** | Dynamic selection based on context signals | Long sessions, multi-agent |

### 4.2 Adaptive Compression Logic

Adaptive mode selects compression depth based on:

- **Ambiguity level** — higher ambiguity → lighter compression
- **Domain maturity** — locked domains → deeper compression allowed
- **Session length** — longer sessions → prefer deep + periodic refresh
- **Model capability** — weaker model → lighter compression with more explicit anchors

### 4.3 Shorthand Format

Every shorthand is self-describing:

```json
{
  "code": "[WAR]",
  "expansion": "War/Geopolitical Risk Premium",
  "domain": "market",
  "anchor": "WAR-ANCHOR",
  "version": "3.0",
  "hash": "WAR1.0",
  "metadata": {
    "created": "v3.0",
    "stability": "high"
  }
}
```

No prior context required. The code carries its own meaning.

### 4.4 Compression Rules

1. Propose a new code when a concept repeats 2+ times in a session or across contributions.
2. Verify bidirectionally before locking — expansion must reconstruct from code, and code must map to a single expansion per domain.
3. Use bracket notation for domain-locked codes: `[WAR]`, `[LIQ]`, `[CARRY]`.
4. Shorthand without brackets is informal and domain-flexible.

---

## 5. Layer 2 — Semantic Layer

### 5.1 Semantic Compression Graph (SCG)

The SCG is a graph-based architecture that maps relationships between shorthand, anchors, hashes, domains, and concepts.

**Node types:** `shorthand`, `anchor`, `hash`, `domain`, `concept`

**Edge types:**

| Relationship | Description |
|---|---|
| `expands_to` | Shorthand → full expansion |
| `linked_to` | Anchor → related anchor |
| `version_of` | Hash → previous hash |
| `domain_of` | Code → domain scope |
| `inherits` | Code → parent concept |
| `conflicts_with` | Code → conflicting code |

SCG enables automatic shorthand generation, drift detection via relationship mapping, lineage tracking across versions, and cross-project linking.

Schema: see `/spec/Semantic-Graph-Schema.json`

### 5.2 Anchor Definitions

An anchor is the **authoritative semantic container** for a shorthand code. It prevents drift by storing the canonical definition, constraints, goals, and domain profiles.

**Anchor structure:**

```json
{
  "id": "WAR-ANCHOR",
  "type": "anchor",
  "label": "War/Geopolitical Risk Premium Anchor",
  "definition": "Risk premium embedded in asset prices due to geopolitical
                 conflict, sanctions, or military escalation.",
  "constraints": [
    "Triggered by: armed conflict, sanctions, territorial disputes",
    "Affects: commodities (energy/metals), FX (safe-haven flows), equities",
    "Measured by: VIX spike, gold premium, USD/JPY/CHF movement"
  ],
  "goals": [
    "Quantify geopolitical risk impact on asset pricing",
    "Enable cross-asset risk analysis"
  ],
  "domain_profiles": {
    "market": "Risk premium visible in commodity spreads and safe-haven demand"
  },
  "versions": ["WAR1.0"],
  "links": ["SCP-ANCHOR"],
  "metadata": {
    "created": "v3.0",
    "stability": "high"
  }
}
```

**Anchor rules:**

- Every shorthand must link to exactly one anchor per domain.
- Anchor definitions must be precise and unambiguous — not interpretable.
- Anchors can reference each other via `links` to form semantic ecosystems.
- Anchors are versioned. Changing a definition creates a new hash, not an overwrite.

### 5.3 Drift Firewall (DFW)

The Drift Firewall is the detection and enforcement layer. It flags when meaning deviates from its anchor.

**DFW detects:**

| Condition | Response |
|---|---|
| Conflicting domains | `[DRIFT-DETECTED]` — halt + report |
| Corrupted shorthand | `[HASH-CONFLICT]` — reject + log |
| Ambiguous expansion | Ask: domain? aspect? |
| Cross-project contamination | Flag and isolate |
| Anchor not loaded | `[ANCHOR-NOT-LOADED]` — do not infer |
| Unknown code | `[UNKNOWN-CODE]` — request definition |

**DFW rule:** Flag immediately — **never silently correct.** Silent correction is the primary source of semantic drift in LLM workflows.

### 5.4 Domain System

Domains scope shorthand meaning. The same code can have different expansions in different domains without conflict.

**Domain structure:**

```
domain:<name>
  ├── shorthand.json       codes scoped to this domain
  └── anchors/             anchor definitions for this domain
      ├── CODE1-ANCHOR.json
      └── CODE2-ANCHOR.json
```

**Domain states:**

| State | Definition |
|---|---|
| **Locked** | Codes finalized, anchors stable, ready for production |
| **Active** | Codes in use, anchors defined, may evolve |
| **Pending** | Domain planned, anchors not yet defined |

**Current domain status:**

| Domain | State | Codes |
|---|---|---|
| `market` | Locked | `[WAR]` `[SH-C]` `[SH-S]` `[LIQ]` `[CARRY]` `[STACK]` |
| `education` | Active | `TA bot`, `ALUMNI` |
| `blockchain` | Pending | — |
| `scp_meta` | Pending | — |

### 5.5 Aspect System

Aspects provide a **lens** on a domain — the perspective from which a code is expanded.

| Aspect | Description |
|---|---|
| `technical` | Engineering, architecture, implementation |
| `msme` | Small business, practical application |
| `education` | Learning, pedagogy, curriculum |
| `creative` | Design, narrative, user experience |

Domain = active topic. Aspect = lens on that topic.

---

## 6. Layer 3 — Memory Layer

### 6.1 Semantic Versioning

All shorthand, anchors, and hashes must be versioned using the format `CODE<major>.<minor>`:

```
WAR1.0 → WAR1.1 → WAR2.0
```

- **Minor version** — refinement, constraint update, no meaning change.
- **Major version** — definition change, requires new anchor review.

### 6.2 Semantic Hashing

Hashes are compact version identifiers that map to specific anchor states:

```
Hash: WAR1.0
  → Anchor: WAR-ANCHOR (v3.0 state)
  → Expansion: "War/Geopolitical Risk Premium"
  → Constraints: [armed conflict, sanctions, supply disruption]
```

Hash integrity is verified by the Drift Firewall. Mismatched hashes trigger `[HASH-CONFLICT]`.

### 6.3 Lineage Tracking

Every shorthand records its creation version, migration history, and stability rating:

```json
"metadata": {
  "created": "v2.0",
  "migrated": "v3.0",
  "stability": "high"
}
```

**Stability ratings:**

| Rating | Criteria |
|---|---|
| `high` | Tested on 2+ models, locked domain, no drift in 20+ turns |
| `medium` | Tested on 1 model, active domain, minor drift corrected |
| `low` | New code, pending verification, domain not locked |

---

## 7. Layer 4 — Interoperability Layer

### 7.1 Semantic Packet Format (SPF)

SPF is the portable container for transmitting meaning across AI models, agents, and workflows. Each packet is self-contained — no prior SCP knowledge required by the receiving model.

**SPF packet structure:**

```json
SPF {
  "code": "[WAR]",
  "expansion": "War/Geopolitical Risk Premium",
  "domain": "market",
  "anchor": "WAR-ANCHOR",
  "hash": "WAR1.0",
  "version": "3.0",
  "constraints": ["armed conflict", "sanctions", "supply disruption"],
  "domain_profile": "risk premium in commodities/FX/equities",
  "metadata": {
    "stability": "high"
  }
}
```

**Required fields:** `code`, `expansion`, `domain`, `anchor`, `hash`, `version`
**Optional fields:** `constraints`, `domain_profile`, `metadata`, `validation`

Full SPF specification: see `/spec/SPF-Packet-Format.md`

### 7.2 SPF Operational Packets

Beyond individual code packets, SPF defines operational packet types:

| Packet Type | Purpose | Typical Size |
|---|---|---|
| `SPF::INIT` | Warm-start a new session with full SCP context | ~600 tokens |
| `SPF::REFRESH` | Mid-session re-anchoring to prevent drift | ~80 tokens |
| `SPF::HANDOFF` | Cross-model transfer — complete semantic state | ~420 tokens |

**SPF::INIT example:**

```json
SPF::INIT {
  "protocol": "SCP v3.0",
  "type": "warm-start",
  "active_domains": { "market": "locked" },
  "active_codes": ["[WAR]","[SH-C]","[SH-S]","[LIQ]","[CARRY]","[STACK]"],
  "rules": ["deterministic","anchor-binding","drift-firewall"],
  "drift_firewall": "active"
}
```

**SPF::REFRESH example:**

```json
SPF::REFRESH {
  "protocol": "SCP v3.0",
  "type": "mid-session-refresh",
  "domain": "market",
  "active_codes": ["[WAR]","[SH-C]","[SH-S]","[LIQ]","[CARRY]","[STACK]"],
  "drift_firewall": "active",
  "instruction": "Re-confirm all active codes against anchors. Continue session."
}
```

### 7.3 Tiered Bootstrap System

SCP uses a three-tier loading strategy to minimize overhead while maximizing context stability:

```
[T1] — Nano System Prompt     ~180 tokens   always load
[T2] — Anchor Pack            ~420 tokens   load at session start
[T3] — SPF Packets            ~420 tokens   cross-model handoff
SPF::REFRESH                   ~80 tokens   mid-session re-anchor
```

**Loading scenarios:**

| Scenario | Load | Tokens |
|---|---|---|
| New session, single model | T1 + T2 | ~600 |
| Continuing session | T1 only | ~180 |
| Cross-model handoff | T3 only | ~420 |
| Cold model, no context | T1 + T3 | ~600 |
| Long session (>20 turns) | Inject SPF::REFRESH | ~80 |
| Full compliance mode | T1 + T2 + T3 | ~1020 |

### 7.4 Agent Compatibility

SCP-compliant agents must:

1. Interpret shorthand codes deterministically
2. Validate anchors before expansion
3. Reject corrupted or unresolvable packets
4. Log drift events with `[DRIFT-DETECTED]`
5. Never silently correct — always flag

**Agent error codes:**

| Code | Meaning |
|---|---|
| `[UNKNOWN-CODE]` | Shorthand not in dictionary — request definition |
| `[ANCHOR-NOT-LOADED]` | Anchor missing — do not infer |
| `[DRIFT-DETECTED]` | Expansion varied — halt + report |
| `[HASH-CONFLICT]` | Version mismatch — reject + log |

### 7.5 Multi-Agent Relay

In agentic systems, SCP + SPF packets compress context at every hop:

```
Without SCP:
  Agent 1 → [full context] → Agent 2 → [full context] → Agent 3
  Context explosion at every hop

With SCP:
  Agent 1 → SPF packet (~70 tokens) → Agent 2 → SPF packet → Agent 3
  Full meaning preserved, zero drift
```

---

## 8. Workflow Specification

Standard SCP processing pipeline:

```
1. Input Classification    → identify domain, detect shorthand
2. Semantic Graph Lookup   → resolve code against SCG
3. Validation Check        → verify anchor binding, hash integrity
4. Adaptive Compression    → select compression mode
5. Anchor-Based Expansion  → deterministic expansion from anchor
6. Drift Firewall Check    → verify expansion matches anchor
7. Interop Packaging       → package as SPF if cross-model
```

---

## 9. Token Economics

### 9.1 The Compounding Problem

```
Turn 1 input:  [system prompt] + [message 1]
Turn 2 input:  [system prompt] + [message 1] + [response 1] + [message 2]
Turn N input:  [system prompt] + [all previous turns] + [message N]
```

Without compression, a 100-turn session sends ~20,000 input tokens per turn — most of which is redundant history.

### 9.2 SCP Impact

| Metric | Value |
|---|---|
| Token reduction per mention | ~60–80% |
| Bootstrap overhead (one-time) | ~600 tokens |
| Break-even point | ~Turn 5 |
| Long session savings (Turn 50+) | Compounds significantly |
| Cross-model handoff overhead | ~70 tokens per SPF packet |
| Full expansion per mention (baseline) | ~480 tokens |
| Compressed per mention | ~30 tokens |
| Savings per mention | ~93% |
| Net session savings (after bootstrap) | ~60–75% |

### 9.3 Session Architecture

```
WRONG:
  One session → run until context ceiling → accuracy degrades → restart

RIGHT:
  Session 1 (turns 1–50) → export SPF packets
  Session 2 (turns 1–50) → load [INIT] + inject SPF packets
  Session N → continue with full meaning, zero token debt
```

SPF packets are the memory bridge between sessions. The bootstrap is the protocol bridge.

### 9.4 Energy Implication

Every token processed is GPU compute. Every redundant token is wasted energy.

```
Without SCP: full prose history × every turn × millions of users = planetary-scale inference waste
With SCP:    compressed history × every turn × same scale = 60–80% less redundant computation
```

SCP addresses inference energy at the protocol level — before the hardware, before the model.

---

## 10. Infrastructure Perspective

### 10.1 SCP as Semantic Router

At infrastructure scale, SCP maps directly to networking concepts:

| Network Concept | SCP Equivalent |
|---|---|
| Router | SCG lookup + DFW |
| Routing table | Shorthand → Anchor map |
| Packet | SPF unit |
| Packet header | code + domain + hash |
| Payload | expansion + constraints |
| Cache | T2 anchor pack |
| DNS | Anchor resolution |
| Checksum | Hash integrity |
| Firewall | DFW |

DNS made the internet human-readable. SCP makes AI communication meaning-stable.

### 10.2 SCP Router (v3.2)

SCP Router is a FastAPI middleware implementation that sits between the client and the LLM:

- Anchor resolution — resolves shorthand to canonical definitions
- Token metering — tracks compression savings per session
- Drift firewall — algorithmic drift detection
- Session persistence — maintains semantic state across turns

The router is transparent to the model — it works on any vendor.

Repository: `github.com/yahyaedhie/scp`

### 10.3 Compact Models + SCP Architecture

Current AI models carry reasoning capability and domain knowledge in the same weights. SCP separates these concerns:

```
Model         = reasoning engine (compact)
SCP Router    = knowledge + meaning store (external)
Together      = more capable than either alone
Model alone   = smaller, faster, cheaper, more efficient
```

This mirrors the direction of RAG, Small Language Models, and Mixture of Experts — SCP provides the semantic layer that connects them.

---

## 11. SCV Extension (Optional)

SCV (Smart Compression & Validation) adds a validation layer on top of SCP for enterprise and compliance workflows.

**SCV adds per shorthand/anchor:**

```json
"validation": {
  "status": "valid|invalid|fallback",
  "confidence": "low|medium|high",
  "last_checked": "2026-03-26"
}
```

**SCV rules:**

- Compression cannot proceed without validation
- Drift firewall events trigger validation reports
- Confidence scores determine compression aggressiveness
- Validation lineage is maintained for audit

SCV is optional. SCP operates fully without it. Enable SCV when compliance, audit trails, or enterprise trust is required.

Full SCV specification: see `/spec/SCV-Extension.md`

---

## 12. Model Compatibility

| Model | Bootstrap Quality | Notes |
|---|---|---|
| Claude Sonnet/Opus | ★★★★★ | Best anchor compliance, structured output |
| GPT-4o | ★★★★ | Good compliance, occasional drift on deep compression |
| Gemini Pro | ★★★ | Requires explicit refresh, moderate drift risk |
| Llama 3 70B | ★★★ | Good for light/moderate, deep requires monitoring |
| Mistral Large | ★★★ | Adequate, benefits from frequent SPF::REFRESH |

---

## 13. Compliance Checklist

```
[ ] Shorthand is self-describing (code + expansion + domain + anchor + hash)
[ ] Anchors defined with canonical definitions, constraints, and domain profiles
[ ] Hashes mapped to Semantic Compression Graph
[ ] Drift Firewall active — flag-only mode, never silently correct
[ ] Adaptive compression enabled
[ ] SPF packets supported for cross-model handoff
[ ] Bootstrap tiers implemented (T1 + T2 + T3 + REFRESH)
[ ] Agent error codes implemented ([UNKNOWN-CODE], [ANCHOR-NOT-LOADED], [DRIFT-DETECTED], [HASH-CONFLICT])
[ ] Domain isolation verified — codes do not bleed across domains
[ ] Versioning and lineage tracking active
[ ] Stability ratings assigned to all anchors
```

---

## 14. Roadmap

| Version | Focus | Status |
|---|---|---|
| **v3.0** | Core protocol — compression, SCG, DFW, SPF, bootstrap | ✅ Stable |
| **v3.1** | SCV validation extension — confidence scoring, compliance metadata | 🔄 In progress |
| **v3.2** | SCP Router — FastAPI middleware, anchor resolution, token metering, drift firewall | 🔄 In progress |
| **v3.3** | Blockchain integration — on-chain anchor registry, SPF notarization | ⏳ Planned |
| **v4.0** | Semantic Router — centralized anchor store, session-independent meaning, algorithmic DFW | ⏳ Planned |
| **v4.0+** | Domain marketplace, utility token, cross-platform anchor resolution | ⏳ Planned |
| **v5.0+** | Semantic Network Layer — SAF addressing, ADP discovery, multicast (requires multi-node network) | ⏳ Deferred |

---

## 15. Repository Structure

```
scp/
├── README.md                         project overview + quick start
├── SPEC.md                           this document — full protocol specification
├── LICENSE                           Apache 2.0
├── CONTRIBUTING.md                   how to extend SCP
├── VISION.md                         architectural vision document
├── TOKENOMICS.md                     LLM token economics explanation
│
├── spec/
│   ├── SPF-Packet-Format.md          semantic packet format
│   ├── Semantic-Graph-Schema.json    SCG schema
│   └── SCV-Extension.md             validation layer (optional)
│
├── dictionary/
│   ├── shorthand.json                shorthand registry
│   └── anchors/
│       ├── PT-ANCHOR.json
│       ├── TA-ANCHOR.json
│       └── ALUMNI-ANCHOR.json
│
├── domains/
│   ├── market/
│   │   ├── shorthand.json            market domain codes (6 locked)
│   │   └── anchors/                  market anchor definitions
│   ├── education/
│   │   ├── shorthand.json
│   │   └── anchors/
│   └── blockchain/                   planned
│
├── bootstrap/
│   ├── T1_system_prompt.txt          nano bootstrap (~180 tokens)
│   ├── T2_anchor_pack_market.txt     market anchors (~420 tokens)
│   ├── T3_spf_packets_market.txt     cross-model packets (~420 tokens)
│   ├── MASTER_bootstrap_market.txt   all tiers combined
│   └── REFRESH_and_guide.txt         mid-session refresh + usage guide
│
├── examples/
│   ├── compressed-vs-expanded.md     expansion examples
│   └── cross-model-relay.md          multi-model usage
│
└── router/                           SCP Router v3.2 (in progress)
    └── ...                           FastAPI middleware implementation
```

---

## 16. License

Apache 2.0 — open protocol, open future.

---

## 17. Author

**Edhie** — Founder, IT Consulting
Sorong, Papua, Indonesia
`github.com/yahyaedhie/scp`

---

*SCP v3.0 — Compress meaning. Prevent drift. Preserve intent across AI models.*