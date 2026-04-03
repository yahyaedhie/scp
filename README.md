 Status: Draft v0.1 — Seeking feedback and validation.
# SCP v3.0 — Semantic Compression Protocol

> **You just talk. The AI remembers, compresses, and never drifts.**

---

## The Problem

Every time you message an AI, the entire conversation history is resent to the model. Every turn. Every token. From scratch.

The model has no memory. It re-reads everything, every time. Token costs compound. Context windows fill. The oldest content drops silently. Meaning drifts. Nobody notices.

```
Turn 1:    500 tokens
Turn 10:   5,000 tokens
Turn 50:   25,000 tokens — context ceiling approaching
Turn 100:  definitions lost — drift begins silently
```

At scale — millions of users, billions of turns — this is planetary-scale redundant computation.

---

## What SCP Does

SCP is an open protocol that sits between the user and the AI model. It compresses meaning, prevents drift, and remembers context — so the model doesn't have to.

|Without SCP|With SCP|
|---|---|
|Full prose resent every turn|Compressed context, anchored definitions|
|Meaning drifts silently|Drift firewall detects and flags|
|New session = start from scratch|Memory bank = instant warm start|
|Switch models = lose everything|SPF packets = meaning survives handoff|
|Long sessions degrade|Long sessions stay precise|
|Every token reprocessed redundantly|60–80% fewer tokens processed|

**The user doesn't need to know SCP exists.** They just talk. The protocol works behind the scenes.

---

## How It Works

```
You say:  "how does war risk affect liquidity right now?"
          OR "[WAR] impact on [LIQ]?"
          OR "carry trades look fragile with all this geopolitical stuff"
          OR anything — any format, any style

Router:   Detects concepts → resolves precise definitions → compresses context
          → sends optimized prompt to AI → validates response → logs savings

You get:  A precise answer. In your style. No drift. No waste.
```

---

## Architecture

```
ENTITY (person / agent / organization)
  communicates naturally
       ↓
SCP ROUTER (has memory, makes decisions)
  ├─ Concept Detector       understands what you mean
  ├─ Anchor Resolver        fetches precise definitions
  ├─ Memory Bank            knows you across sessions
  ├─ Session Memory         knows this conversation
  ├─ Context Builder        builds optimal prompt for AI
  ├─ Drift Firewall         validates response integrity
  ├─ Token Meter            measures everything
  └─ Proposal Engine        discovers new concepts
       ↓
LLM (any vendor — Claude, GPT, Gemini, Llama, any model)
       ↓
ENTITY gets precise answer
```

### Four Protocol Layers

```
L1 — Compression Layer      Input normalization + adaptive compression
L2 — Semantic Layer         Concept detection + anchor resolution + drift firewall
L3 — Memory Layer           Session memory + memory bank + versioning + lineage
L4 — Interoperability       SPF packets + multi-model + multi-agent compatibility
```

---

## Core Concepts

### Anchor

The source of truth. A canonical definition container that prevents drift.

```json
{
  "id": "WAR-ANCHOR",
  "shorthand": "[WAR]",
  "expansion": "War/Geopolitical Risk Premium",
  "definition": "Risk premium embedded in asset prices due to geopolitical
                 conflict, sanctions, or military escalation.",
  "constraints": ["armed conflict", "sanctions", "supply disruption"],
  "keywords": ["war", "geopolitical", "conflict", "military", "sanctions"],
  "domain": "market",
  "hash": "WAR1.0",
  "version": "3.0",
  "stability": "high"
}
```

### SPF Packet

The universal unit of meaning. Portable, self-describing, drift-resistant.

```json
SPF {
  "code": "[WAR]",
  "expansion": "War/Geopolitical Risk Premium",
  "domain": "market",
  "anchor": "WAR-ANCHOR",
  "hash": "WAR1.0",
  "version": "3.0"
}
```

Any model. Any session. Zero prior context required.

### Concept Detection

Dual-path — understands both structured shorthand and natural language.

```
Path A (shorthand):  "[WAR]↑ → [LIQ]↓"         → direct anchor resolution
Path B (natural):    "war risk affecting liquidity" → keyword matching → same result
Path C (hybrid):     "[WAR] is tightening liquidity" → both paths combined
```

The user never needs to learn shorthand. The router figures out what they mean.

### Drift Firewall

Two-layer detection — algorithmic (router-side) + behavioral (LLM-side).

```
Router:  validates every response against anchor definitions
LLM:     flags [DRIFT-DETECTED] if its own expansion varies from anchor
Rule:    flag immediately — never silently correct
```

### Memory Bank

The router remembers. Across sessions. Across models.

```
Session Memory    → what's happening this conversation (temporary)
Memory Bank       → what the router learned about you (permanent)
Anchor Store      → canonical definitions (permanent)
```

No pruning. All history has value. Your semantic identity is yours — exportable, portable.

---

## Entity Model

SCP serves any entity that communicates — not just humans.

|Entity Type|Description|
|---|---|
|**Person**|Individual user|
|**Agent**|Autonomous AI agent or bot|
|**Corporate**|Organization or team sharing definitions|

Corporate entities provide shared anchors that sub-entities inherit:

```
Corporate: Acme Trading
  ├─ Shared anchors (market, compliance, internal)
  ├─ Analyst-1 (inherits corporate + own additions)
  ├─ Analyst-2 (inherits corporate + own additions)
  └─ Risk-bot (inherits corporate + task-specific anchors)
```

Each entity owns: one anchor store + one memory bank + their sessions. Nothing shared across entities unless explicitly inherited.

---

## Token Efficiency

|Metric|Value|
|---|---|
|Token reduction per session|60–80%|
|Bootstrap overhead (router-managed)|~300 tokens|
|Break-even point|Turn 3–5|
|Long session savings (Turn 50+)|Compounds significantly|
|Cross-model handoff|~70 tokens per SPF packet|

### Energy Efficiency

Fewer tokens = less GPU compute = less energy. At scale, SCP represents measurable reduction in inference energy consumption. Not as a side effect — as a primary design goal.

```
Without SCP:  full prose history reprocessed every turn
With SCP:     compressed context, anchored definitions, memory-assisted routing
Difference:   60–80% less redundant computation per session
At scale:     millions of entities × billions of turns = significant energy reduction
```

---

## Per-Turn Flow

```
 1. RECEIVE      Entity message (any format)
 2. REMEMBER     Load memory bank — who is this entity
 3. DETECT       Shorthand (regex) + concepts (semantic)
 4. CLASSIFY     High confidence → active | low → uncertain | none → track
 5. RESOLVE      Fetch relevant anchors from store
 6. CONTEXT      Build prompt: rules + anchors + session narrative + style
 7. ROUTE        Forward to LLM (any vendor)
 8. VALIDATE     Drift firewall checks response
 9. LEARN        Update session memory + promote/demote uncertain anchors
10. METER        Count tokens — input, output, baseline, savings
11. PROPOSE      If unmatched concept hits threshold → queue proposal
12. RESPOND      Clean answer to entity in their style
```

---

## The Deeper Vision

SCP started as a personal productivity tool — a way to have more efficient conversations with AI. It became something larger.

### The Missing Layer

```
Internet stack:
  Physical layer    → cables, signals
  Network layer     → IP routing
  Transport layer   → TCP/UDP
  Application layer → HTTP, DNS

Missing:
  Semantic layer    → MEANING
```

The internet moves data. It does not move meaning. SCP is a proposal for what the semantic layer of AI networks looks like:

|Network Concept|SCP Equivalent|
|---|---|
|Router|SCP router + drift firewall|
|Routing table|Anchor store|
|Packet|SPF unit|
|Cache|Memory bank|
|DNS|Anchor resolution|
|Checksum|Hash integrity|
|Firewall|Drift firewall|

**DNS made the internet human-readable. SCP makes AI communication meaning-stable.**

### Smaller Models. Smarter Systems.

Current AI models carry reasoning capability and domain knowledge in the same weights. SCP separates these:

```
Model          = reasoning engine (compact, stateless)
SCP router     = knowledge + meaning store (external, persistent)
Together       = more capable than either alone
```

This mirrors human cognition: the brain reasons, the library stores knowledge, together they're a capable system.

---

## Status

|Component|Status|
|---|---|
|Core design|✅ Verified|
|Protocol specification|✅ v3.0|
|SPF packet format|✅ Stable|
|Semantic graph schema|✅ Stable|
|Entity model|✅ Designed|
|Memory bank architecture|✅ Designed|
|Concept detection (dual-path)|✅ Designed|
|domain:market (6 locked codes)|✅ Implemented|
|domain:education|⏳ Planned|
|domain:blockchain|⏳ Planned|
|Router implementation|🔄 In progress|
|Benchmark suite|🔄 Methodology designed|
|SCV validation extension|⏳ Planned|

---

## Roadmap

|Version|Focus|Status|
|---|---|---|
|**v3.0**|Core protocol — design verified, behavioral implementation|✅ Current|
|**v3.1**|SCV validation extension|Planned|
|**v3.2**|Infrastructure middleware — router with memory|In progress|
|**v4.0**|Semantic router — full external anchor resolution at scale|Vision|
|**v5.0**|Semantic network layer — multi-router, multi-agent mesh|Vision|

---

## Repository Structure

```
scp/
├── README.md                           ← you are here
├── LICENSE                             ← Apache 2.0
├── CONTRIBUTING.md                     ← how to extend SCP
├── VISION.md                           ← the deeper case for semantic infrastructure
│
├── spec/
│   ├── SCP_v3_0_Design.md              ← full design document (verified)
│   ├── SPF-Packet-Format.md            ← semantic packet format
│   ├── Semantic-Graph-Schema.json       ← SCG schema
│   └── SCV-Extension.md                ← validation layer (optional)
│
├── dictionary/
│   ├── shorthand.json                  ← shorthand registry
│   └── anchors/                        ← anchor definitions
│
├── domains/
│   └── market/
│       ├── shorthand.json              ← market domain codes
│       └── anchors/                    ← market anchor definitions
│
├── bootstrap/
│   ├── T1-bootstrap.md                 ← nano bootstrap (~180 tokens)
│   ├── T2-bootstrap.md                 ← anchor definitions (~420 tokens)
│   ├── T3=bootstrap.md                 ← cross-model packets (~420 tokens)
│   └── T123-Boostrap.md                ← all tiers combined
│
├── benchmarks/
│   ├── BENCHMARK.md                    ← benchmark methodology
│   ├── prompts/                        ← standardized test prompts
│   └── templates/                      ← recording templates
│
├── docs/
│   ├── SCP_Evolution_refined.md        ← protocol evolution history
│   └── TOKENOMICS.md                   ← token economics explained
│
└── examples/
    └── compressed-vs-expanded.md       ← expansion examples
```

---

## Quick Start (Behavioral — No Router)

SCP works today as a behavioral protocol inside any LLM's context window.

### 1. Copy the bootstrap

Paste the contents of `bootstrap/T1-bootstrap.md` as your system prompt.

### 2. Talk normally

```
You:   "how does war risk affect carry trades when liquidity is tight?"
AI:    [resolves concepts against loaded anchors, responds with precision]
```

Or use shorthand if you prefer:

```
You:   [WAR]↑ + [LIQ]↓ → [CARRY] impact?
AI:    [WAR] elevation compresses [LIQ] → [CARRY] unwind risk ↑
```

### 3. Cross-model handoff

Export `T3-bootstrap.md` → paste into new model's system prompt → meaning preserved.

---

## Origin

SCP was born from a constraint: limited token usage per day.

When you can't afford to waste tokens, you discover the structural inefficiency that unlimited-access researchers never feel. Every repeated explanation is waste. Every drifted concept is a lost turn. Every session restart is a cold start.

SCP is what emerged from following that constraint to its logical conclusion — a protocol for meaning that doesn't get lost, doesn't drift, and doesn't waste computation.

The path from personal productivity to planetary infrastructure was not planned. It was discovered.

---

## License

Apache 2.0 — see [LICENSE]
---

## Author

**Edhie** — Founder, IT Consulting Sorong, Papua, Indonesia

---

## Contributing

SCP is an open protocol. Contributions welcome — see [CONTRIBUTING.md]
You can contribute: new domain packs, anchor definitions, reference implementations, test cases, documentation, and translations.

---

_SCP v3.0 — open protocol, open future_ _github.com/yahyaedhie/scp_