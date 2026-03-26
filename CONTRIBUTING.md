# Contributing to SCP v3.0

Thank you for contributing to the Semantic Compression Protocol.

SCP is an open protocol. The semantic layer of AI communication should belong to everyone who builds on it.

---

## Design Principle

Before contributing, understand the core principle:

**SCP is the AI's internal operating protocol. The entity just communicates.**

Everything in SCP — anchors, packets, detection, memory — works behind the scenes. Contributions should preserve this invisibility. If a feature requires the entity to learn protocol internals, the design is wrong.

---

## What You Can Contribute

| Type | Examples | Impact |
|---|---|---|
| **New domain packs** | domain:legal, domain:healthcare, domain:finance, domain:logistics | Extends SCP to new fields |
| **Anchor definitions** | New anchors for existing or new domains | Grows the protocol's vocabulary |
| **Keyword sets** | Natural language keywords for concept detection | Improves detection accuracy |
| **Router components** | Detection, compression, drift firewall improvements | Strengthens the engine |
| **Benchmark data** | Token savings measurements from real sessions | Proves the protocol works |
| **Reference implementations** | Python, JS, API wrappers, CLI tools | Makes SCP accessible |
| **Test cases** | Cross-model expansion tests, drift detection tests | Ensures reliability |
| **Documentation** | Clarifications, translations, tutorials | Lowers entry barrier |
| **Entity templates** | Pre-configured anchor stores for specific use cases | Speeds up adoption |

---

## How to Add a New Domain

### 1. Create domain folder

```
domains/
└── your-domain/
    ├── shorthand.json
    └── anchors/
        └── YOUR-ANCHOR.json
```

### 2. Anchor format (v3.0)

Every anchor must include the `keywords` field. This is what enables natural language concept detection — entities don't need to use shorthand codes.

```json
{
  "id": "CODE-ANCHOR",
  "shorthand": "[CODE]",
  "expansion": "Full Human-Readable Expansion",
  "definition": "Canonical definition — precise and unambiguous. This is the source of truth.",
  "constraints": [
    "boundary condition 1",
    "boundary condition 2",
    "boundary condition 3"
  ],
  "keywords": [
    "natural language term 1",
    "natural language term 2",
    "phrase that a user would actually say",
    "synonym or related term"
  ],
  "domain": "your-domain",
  "domain_profile": "How this concept is used within this specific domain",
  "hash": "CODE1.0",
  "version": "3.0",
  "stability": "low|medium|high",
  "metadata": {
    "created": "v3.0",
    "modified": "v3.0",
    "validation": {
      "status": "valid",
      "confidence": "low|medium|high",
      "last_checked": "YYYY-MM-DD"
    }
  }
}
```

### 3. Shorthand registry format

```json
{
  "id": "CODE-id",
  "type": "shorthand",
  "label": "[CODE]",
  "expansion": "Full Expansion Text",
  "domain": ["your-domain"],
  "anchor": "CODE-ANCHOR",
  "version": "3.0",
  "hash": "CODE1.0",
  "metadata": {
    "created": "v3.0",
    "stability": "low|medium|high"
  }
}
```

### 4. SPF packet format

For cross-model portability, every anchor should have a corresponding SPF packet:

```json
SPF {
  "code": "[CODE]",
  "expansion": "Full Expansion Text",
  "domain": "your-domain",
  "anchor": "CODE-ANCHOR",
  "hash": "CODE1.0",
  "version": "3.0",
  "constraints": ["constraint 1", "constraint 2"],
  "validation": {
    "status": "valid",
    "confidence": "high",
    "last_checked": "YYYY-MM-DD"
  }
}
```

---

## Keywords — Critical for Concept Detection

The `keywords` field is what makes SCP invisible to the entity. Without good keywords, the concept detector can't match natural language to anchors.

### Writing Good Keywords

| Guideline | Example |
|---|---|
| Include the obvious terms | `"liquidity"` for LIQ-ANCHOR |
| Include synonyms | `"funding"`, `"credit"` for LIQ-ANCHOR |
| Include phrases entities actually say | `"dry up"`, `"tightening"` for LIQ-ANCHOR |
| Include domain-specific jargon | `"bid-ask"`, `"repo"`, `"market depth"` for LIQ-ANCHOR |
| Include related concepts that signal this anchor | `"safe-haven"` for WAR-ANCHOR |
| Avoid generic words that match everything | Don't add `"market"`, `"risk"`, `"price"` unless highly specific |

### Testing Keywords

Before submitting, test your keywords against realistic natural language:

```
Anchor:   LIQ-ANCHOR (Liquidity Conditions)
Keywords: ["liquidity", "funding", "credit", "bid-ask", "market depth",
           "repo", "dry up", "tightening", "liquid"]

Test sentences:
  "funding markets are tightening"         → should match ✓
  "credit conditions are worsening"        → should match ✓
  "the weather is nice today"              → should NOT match ✓
  "I need to buy some liquid soap"         → should NOT match (but might — acceptable false positive, LLM will filter)
```

The concept detector uses confidence thresholds. A single weak keyword match alone won't trigger injection — multiple matching terms increase confidence. Design your keyword list so that genuine references produce 2+ keyword hits.

---

## Contribution Rules

1. **Invisibility first** — the entity should never need to know your anchor exists for it to work. Keywords must cover natural language.

2. **Deterministic expansion** — same concept + same domain must always resolve to the same anchor definition. No ambiguity.

3. **Precise definitions** — anchor definitions must be canonical and unambiguous. If two people could reasonably interpret a definition differently, it's not precise enough.

4. **Domain isolation** — anchor codes must not collide across domains. If "carry" means different things in `domain:market` and `domain:logistics`, they must be separate anchors with separate codes.

5. **Keywords are required** — every anchor must include a `keywords` field with natural language terms. Anchors without keywords break concept detection.

6. **Stability honesty** — rate stability accurately. New anchors start at `low` or `medium`. Only anchors tested across multiple sessions and models earn `high`.

7. **Constraint completeness** — constraints define the boundaries of what the anchor covers. They are used by the drift firewall to validate responses. Incomplete constraints weaken drift detection.

8. **Version discipline** — modifications to existing anchors must increment the hash version. Definition changes are breaking changes and require a major version bump (e.g., `CODE1.0` → `CODE2.0`). Constraint additions are minor (e.g., `CODE1.0` → `CODE1.1`).

---

## How to Add Benchmark Data

Benchmark data is critical evidence that SCP works. Every real measurement strengthens the protocol's credibility.

### What to Measure

| Metric | How |
|---|---|
| Token count (control) | Run a task without SCP — record input + output tokens per turn |
| Token count (SCP) | Run the same task with SCP — record input + output tokens per turn |
| Drift events | At checkpoints, request expansion and compare to anchor definition |
| Cross-model accuracy | Export SPF packets from model A, import to model B, verify expansion |

### Submitting Results

Use the templates in `benchmarks/templates/` and submit to `benchmarks/results/`:

```
benchmarks/
└── results/
    └── YOUR-TEST-ID.yaml
```

Format:

```yaml
test_id: "CAT1-XXX"
date: "YYYY-MM-DD"
contributor: "your-name"
category: "single_session_efficiency|drift_resistance|cross_model|break_even"
model: "model-name-and-version"
domain: "domain-tested"
turns: 30
results:
  control_total_tokens: ___
  scp_total_tokens: ___
  savings_percent: ___
  drift_events: ___
notes: ""
```

### Rules for Benchmark Data

- Report raw numbers — don't round until summary
- Include bootstrap overhead in SCP totals
- Note token counting method (API count vs estimate)
- Report ALL results including unfavorable ones
- Test on minimum 2 models for conclusive claims

---

## How to Contribute Router Components

The SCP router is the middleware engine. Contributions to router components follow the architecture documented in `spec/SCP_v3_0_Design.md`.

### Router Components

| Component | Purpose | Key Constraint |
|---|---|---|
| Concept Detector | Detect shorthand + natural language concepts | Must support dual-path (regex + semantic) |
| Anchor Resolver | Fetch definitions from anchor store | Must support entity inheritance (own store → parent store) |
| Context Builder | Build compressed prompt for LLM | Must inject only relevant anchors per turn (minimal injection) |
| Drift Firewall | Validate response against anchor definitions | Must flag, never silently correct |
| Token Meter | Count tokens and calculate savings | Must track per-turn and cumulative |
| Session Memory | Track conversation state | Must compress — not store full prose |
| Memory Bank | Learn entity patterns across sessions | Must never prune |
| Proposal Engine | Detect repeated unmatched concepts | Must queue for approval, not auto-create |

### Design Constraints for All Components

- Entity-agnostic — must work for persons, agents, and corporate entities
- Model-agnostic — must work with any LLM vendor
- SCP-invisible — must not require the entity to know the protocol exists
- SPF-native — must operate on SPF packets as the universal meaning unit

---

## Entity Templates

Entity templates are pre-configured anchor stores for specific use cases. They help new entities get started quickly.

### Example: Market Analysis Entity

```
entity-templates/
└── market-analyst/
    ├── anchors.json        ← pre-defined market anchors
    ├── description.md      ← what this template is for
    └── bootstrap.txt       ← behavioral bootstrap for context-window-only usage
```

### Submitting a Template

- Include at least 4 anchors with complete definitions, constraints, and keywords
- Test on minimum 2 models
- Include a description of the intended entity type and use case
- Include a behavioral bootstrap for users who don't have the router yet

---

## Pull Request Checklist

### For New Anchors / Domains

```
[ ] anchor.json follows v3.0 schema
[ ] keywords field included with natural language terms
[ ] definition is precise and unambiguous
[ ] constraints are complete
[ ] hash version assigned
[ ] stability rating justified
[ ] domain isolation verified — no code collisions
[ ] tested: concept detection matches on natural language
[ ] tested: expansion verified on minimum 2 models
[ ] no conflict with existing anchors
```

### For Router Components

```
[ ] follows architecture in SCP_v3_0_Design.md
[ ] entity-agnostic (works for person/agent/corporate)
[ ] model-agnostic (no vendor lock-in)
[ ] includes tests
[ ] documented
```

### For Benchmark Data

```
[ ] uses template from benchmarks/templates/
[ ] raw numbers reported
[ ] bootstrap overhead included
[ ] token counting method noted
[ ] minimum 2 models tested (for conclusive claims)
```

---

## Code of Conduct

- **Propose, don't overwrite** — flag conflicts, suggest changes, respect existing definitions
- **Precision over convenience** — a vague anchor that's easy to write is worse than a precise anchor that takes thought
- **Test before submitting** — untested anchors with bad keywords degrade detection for everyone
- **Document your reasoning** — explain why a definition uses these constraints, why these keywords were chosen
- **Respect entity ownership** — anchor stores belong to entities, not to the protocol

---

## Questions?

Open an issue. Include:

- What you're trying to contribute
- Which domain or component it affects
- Any conflicts you've identified with existing definitions

---

*SCP v3.0 — open protocol, open contributions*
*github.com/yahyaedhie/scp*