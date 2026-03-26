# SCP v3.0 — Semantic Compression Protocol

### Design Document

`version: 3.0 | status: concept verified | date: 2026-03-26`

---

## 1. Core Principle

**SCP is the AI's internal operating protocol. The entity just communicates.**

The entity — whether a person, an agent, or an organization — communicates naturally in any format. The SCP router handles all compression, anchor resolution, drift prevention, token optimization, and memory management internally. The protocol is invisible to the entity unless they choose to engage with it directly.

SCP is to the AI what TCP/IP is to the internet: the entity doesn't write packet headers — the protocol handles it.

---

## 2. What SCP Solves

Every turn, every model resends the full conversation history. There is no persistent memory. Token cost compounds. Context windows fill. Oldest content drops silently. Meaning drifts without detection.

SCP addresses this at the protocol level:

- Compresses meaning into anchored definitions
- Prevents drift through algorithmic detection
- Persists knowledge outside the model via router memory
- Reduces token cost by 60–80%
- Enables cross-model and cross-session continuity
- Scales from single person to multi-agent corporate environments

---

## 3. Architecture Overview

```
ENTITY (person / agent / corporate)
  communicates naturally
       ↓
ROUTER (SCP engine — has memory, makes decisions)
  ├─ Concept Detector       understands what the entity means
  ├─ Anchor Resolver        fetches precise definitions
  ├─ Memory Bank            knows this entity across sessions
  ├─ Session Memory         knows this conversation
  ├─ Context Builder        builds optimal prompt for LLM
  ├─ Drift Firewall         validates response integrity
  ├─ Token Meter            measures everything
  └─ Proposal Engine        discovers new concepts
       ↓
LLM (SCP-aware, stateless, any vendor)
       ↓
ENTITY gets precise answer in their style
```

---

## 4. Four Protocol Layers

```
L1 — Compression Layer      Input normalization + adaptive compression
L2 — Semantic Layer         Concept detection + anchor resolution + drift firewall
L3 — Memory Layer           Session memory + memory bank + versioning + lineage
L4 — Interoperability       SPF packets + multi-model + multi-agent compatibility
```

Every layer operates on SPF packets — the universal unit of meaning in the system.

---

## 5. Entity Model

A "user" in SCP is an entity. An entity is any participant that communicates through the router.

### 5.1 Entity Types

|Type|Description|Example|
|---|---|---|
|**Person**|Individual human user|Analyst running market analysis|
|**Agent**|Autonomous AI agent or bot|Trading bot querying risk via SCP|
|**Corporate**|Organization or team|Entire company sharing definitions|

### 5.2 Entity Data Ownership

Each entity owns its own data. Nothing is shared across entities unless explicitly inherited.

```
Entity
  ├─ type: person | agent | corporate
  ├─ parent: optional (for inheritance)
  ├─ Anchor Store (own definitions + inherited from parent)
  ├─ Memory Bank (own patterns, never shared upward)
  └─ Sessions (own conversation history)
```

### 5.3 Inheritance

Entities can inherit from a parent entity. Resolution order follows a chain:

1. Check entity's own anchor store
2. If not found, check parent entity (e.g., corporate)
3. If not found, concept is unmatched

This enables corporate entities to define shared organizational vocabulary while persons and agents add their own customizations on top.

```
Corporate entity: "Acme Trading"
  ├─ Anchor Store (organizational definitions)
  │   ├─ domain:market
  │   ├─ domain:compliance
  │   └─ domain:internal
  │
  └─ Sub-entities (inherit corporate anchors)
      ├─ Person: analyst-1 (own sessions + own additions)
      ├─ Person: analyst-2 (own sessions + own additions)
      └─ Agent: risk-bot (own sessions + task-specific anchors)
```

---

## 6. Three-Layer Memory Architecture

The router has memory. The LLM does not. This is what makes SCP fundamentally different from prompt engineering.

### 6.1 Layer 1 — Session Memory (temporary, per conversation)

What is happening right now.

|Contains|Purpose|
|---|---|
|Active concepts this conversation|Track what has been discussed|
|Relationships established this session|Track connections between concepts|
|Turn narrative (compressed)|Provide context without full prose history|
|Drift events|Audit trail for this session|
|Domain context|Which domains are active right now|
|Uncertain anchor tracking|Evidence accumulation for promotion/demotion|
|Unmatched concept tracking|Input for auto-proposal engine|

Session memory resets when the session ends. Confirmed patterns are promoted to the memory bank.

### 6.2 Layer 2 — Memory Bank (permanent, per entity)

What the router has learned about this entity across all sessions.

|Contains|Purpose|
|---|---|
|Entity profile (style, expertise, preferences)|Personalize every interaction|
|Anchor usage history (frequency, recency, pairings)|Predict which anchors to pre-load|
|Learned relationships (confirmed across sessions)|Enrich context without re-discovery|
|Custom anchors (entity-created definitions)|Extend the protocol per entity|
|Domain usage patterns|Predict active domains|

Memory bank is never pruned. All history has value to the entity. The memory bank is exportable — the entity owns their semantic identity and can carry it to any SCP-compatible router.

### 6.3 Layer 3 — Anchor Store (permanent, per entity)

The canonical definitions that give meaning to shorthand codes.

|Contains|Purpose|
|---|---|
|SPF anchor definitions|Source of truth for all meaning|
|Domain assignments|Organize anchors by context|
|Version history|Track how definitions evolve|
|Constraints and keywords|Enable concept detection and drift validation|

Each entity has their own anchor store. Corporate entities provide shared anchors that sub-entities inherit.

### 6.4 How the Three Layers Interact

```
Session starts:
  Router loads memory bank → knows the entity
  Router loads anchor store → has the definitions
  Session memory initialized → empty, ready to accumulate

Each turn:
  Session memory tracks what happens
  Anchor store provides definitions
  Memory bank informs routing decisions (pre-loading, style, confidence)

Session ends:
  Session memory → confirmed patterns promoted to memory bank
  Session memory → new anchors stored in anchor store
  Session memory → archived (compressed)
  Memory bank → updated with usage stats
  Anchor store → updated with new/modified anchors

Next session:
  Memory bank already loaded → warm start
  No manual setup needed
  Router already knows who this entity is
```

---

## 7. SPF — Semantic Packet Format

SPF is the universal unit of meaning in SCP. It is the anchor definition packet — static, canonical, portable.

### 7.1 SPF Role

SPF is not a runtime state container. It is the meaning itself.

|Object|What It Is|Lifecycle|
|---|---|---|
|SPF Packet|Meaning container — definition, constraints, hash|Permanent in anchor store|
|Session Memory|Runtime state — what happened this turn|Temporary per session|
|Memory Bank|Learned state — patterns across sessions|Permanent per entity|

SPF packets flow through every layer of the router but do not carry runtime metadata. The router's memory handles runtime intelligence separately.

### 7.2 SPF Packet Structure

```
SPF {
  code:        "[WAR]"
  expansion:   "War/Geopolitical Risk Premium"
  definition:  "Risk premium embedded in asset prices due to
                geopolitical conflict, sanctions, or military escalation."
  constraints: ["armed conflict", "sanctions", "supply disruption"]
  keywords:    ["war", "geopolitical", "conflict", "military", "sanctions"]
  domain:      "market"
  anchor:      "WAR-ANCHOR"
  hash:        "WAR1.0"
  version:     "3.0"
  stability:   "high"
}
```

### 7.3 SPF Use Cases

|Use Case|How SPF Is Used|
|---|---|
|Anchor resolution|Router fetches SPF packet from store, injects into LLM context|
|Cross-model handoff|Export SPF packets, import into new model's router|
|Cross-session continuity|SPF packets persist in anchor store, available every session|
|Agent-to-agent communication|Agents exchange SPF packets — shared meaning, zero drift|
|Corporate shared vocabulary|Corporate anchor store contains SPF packets all sub-entities inherit|

---

## 8. Concept Detection

The router understands what the entity means without requiring structured input.

### 8.1 Dual-Path Detection

Two detection paths run in parallel on every message:

|Path|Input|Method|Output|
|---|---|---|---|
|**Path A — Shorthand**|`[WAR]↑ → [LIQ]↓`|Regex pattern matching|Direct anchor resolution|
|**Path B — Semantic**|"war risk affecting liquidity"|Keyword/phrase matching against anchor keywords, constraints, definitions|Concept-to-anchor mapping|
|**Path C — Hybrid**|`[WAR] is tightening liquidity`|Both paths on same message|Combined resolution|

### 8.2 Confidence Classification

Every detection is classified:

|Confidence|Meaning|Router Action|
|---|---|---|
|**High**|Direct shorthand match or strong keyword overlap|Inject anchor as active|
|**Uncertain**|Weak keyword match, ambiguous context|Inject anchor tagged as uncertain — LLM decides relevance|
|**No match**|Concept not in anchor store|Track in session memory for auto-proposal|

### 8.3 Concept Matching Rules

- Expansion match: entity text matches anchor's expansion field
- Keyword match: entity text matches anchor's keywords field
- Constraint match: entity text matches anchor's constraints
- Domain scoping: only match anchors within active domain(s)
- Confidence threshold: minimum keyword overlap required before mapping
- Ambiguity handling: if multiple anchors match equally, context from memory bank helps disambiguate

---

## 9. Context Building

The router builds the optimal prompt for the LLM each turn.

### 9.1 What the LLM Receives

|Component|Source|Purpose|
|---|---|---|
|T1 system rules|Protocol definition|LLM is SCP-aware, follows rules|
|Active anchors|Detected this turn (high confidence)|Precise definitions for current concepts|
|Uncertain anchors|Detected this turn (low confidence), tagged|LLM evaluates relevance from context|
|Session narrative|Session memory (compressed)|Conversation continuity without full prose|
|Style instruction|Memory bank (entity profile)|Match entity's communication style|
|Entity message|Original, unmodified|What the entity actually said|

### 9.2 What the LLM Does NOT Receive

- Full prose history of all past turns
- The memory bank itself
- All anchors in the store (only relevant ones)
- Internal router decisions or scoring
- Protocol infrastructure details

### 9.3 LLM Is SCP-Aware

The LLM receives T1 protocol rules and actively participates in drift prevention:

- Follows deterministic expansion rules
- Flags drift if detected from its side
- Respects anchor definitions as source of truth
- Reports unknown codes
- Adapts response format to match entity's style

The router catches drift algorithmically. The LLM catches drift behaviorally. Double layer.

---

## 10. Drift Firewall

Drift is when meaning shifts away from its anchor definition. SCP prevents this through two layers.

### 10.1 Router-Side Detection (Algorithmic)

After every LLM response, the router validates:

- Does the response align with the anchor definitions that were injected?
- Are constraints respected?
- Has the LLM paraphrased in a way that changes meaning?

### 10.2 LLM-Side Detection (Behavioral)

The LLM is instructed to:

- Flag `[DRIFT-DETECTED]` if its own expansion varies from the anchor
- Report `[UNKNOWN-CODE]` for unrecognized shorthand
- Report `[ANCHOR-NOT-LOADED]` if a referenced anchor is missing
- Never silently correct — always flag

### 10.3 Drift Events

When drift is detected:

1. Event is logged in session memory
2. Response is flagged (not silently corrected)
3. Entity is informed if the drift affects answer quality
4. Anchor definition is re-injected on next turn

---

## 11. Auto-Proposal Engine

When the entity introduces concepts the router doesn't recognize, the router learns.

### 11.1 Detection

Unmatched concepts are tracked in session memory:

```
Turn 3:  entity mentions "volatility smile" → no anchor match → logged
Turn 8:  entity mentions "vol smile" again  → 2nd occurrence → threshold met
```

### 11.2 Proposal

When an unmatched concept reaches the occurrence threshold (2+), the router generates a proposal:

```
Proposed anchor:
  suggested code: [VOL-SMILE]
  suggested expansion: "Volatility Smile Pattern"
  detected from: ["volatility smile", "vol smile"]
  domain: market
  status: pending approval
```

### 11.3 Approval

The router presents the proposal to the entity at a natural break in conversation. The entity approves, modifies, or rejects. Approved anchors are added to the entity's anchor store.

### 11.4 For Agent Entities

Agents can be configured to auto-approve proposals above a confidence threshold, or to queue all proposals for human review.

---

## 12. Multi-Domain Support

A session can span multiple domains. The router infers active domains from context.

### 12.1 Domain Detection

The router tracks domain signals in session memory:

- Keywords that match specific domain anchors
- Explicit domain references by the entity
- Memory bank patterns (entity usually works in these domains)

### 12.2 Domain Activation

Domains activate automatically when enough signals accumulate. The entity never needs to declare "switching to blockchain" — the router detects it.

### 12.3 Cross-Domain Resolution

When a concept exists in multiple domains, the router:

1. Checks active domain context
2. Checks memory bank for entity's historical usage
3. If still ambiguous, injects both with domain tags — LLM decides from context

---

## 13. Response Format

The router adapts the LLM's response style to match the entity's communication style.

|Entity Style|Router Instructs LLM|
|---|---|
|Prose / conversational|Respond naturally, no formatting|
|Technical / structured|Respond with tables, lists, structured analysis|
|Shorthand user|Respond with shorthand codes, compressed format|
|Brief / time-constrained|Respond concisely, lead with direct answer|

Style is learned from the memory bank and confirmed per session. The entity never needs to specify — the router adapts.

---

## 14. Token Metering

Every turn is measured automatically.

### 14.1 What Is Measured

|Metric|Description|
|---|---|
|Input tokens|What the router sent to the LLM (system prompt + context + message)|
|Output tokens|What the LLM returned|
|Baseline estimate|What would have been sent without SCP (full prose equivalent)|
|Savings|Baseline minus actual — tokens saved this turn|
|Cumulative savings|Total savings across the session|

### 14.2 Why This Matters

Token metering generates benchmark data automatically. Every conversation produces evidence of SCP's efficiency. No manual benchmarking needed — the router measures itself.

### 14.3 Energy Proxy

Tokens saved correlate to reduced GPU computation. The router tracks an energy proxy:

```
Compute reduction ratio = tokens saved / baseline tokens
```

At scale — millions of entities, billions of turns — this represents measurable inference energy savings.

---

## 15. Session Lifecycle

### 15.1 New Session

1. Router loads memory bank for this entity
2. Router knows: entity style, expertise, frequent anchors, domain preferences
3. Router pre-loads most likely anchors from usage history
4. No manual setup needed — memory bank replaces SPF::INIT

### 15.2 During Session

5. Each turn follows the per-turn flow (Section 16)
6. Session memory accumulates
7. Uncertain anchors promoted or demoted based on accumulated evidence
8. Unmatched concepts tracked for auto-proposal
9. Token savings measured every turn

### 15.3 Session End

10. Confirmed patterns promoted to memory bank
11. New anchors stored in anchor store
12. Usage statistics updated in memory bank
13. Session memory archived (compressed)

### 15.4 Next Session

14. Entity communicates naturally
15. Router already knows the entity — warm start
16. Zero re-explanation, zero cold start

---

## 16. Per-Turn Flow

```
 1. RECEIVE      Entity message (any format, any style)
 2. REMEMBER     Load memory bank — who is this entity, what do they care about
 3. DETECT       Shorthand (regex) + concepts (semantic) in message
 4. CLASSIFY     High confidence → active | low confidence → uncertain | no match → track
 5. RESOLVE      Fetch SPF anchors for active + uncertain detections
 6. CONTEXT      Build prompt: T1 rules + relevant anchors + session narrative + style
 7. ROUTE        Forward to LLM (any vendor)
 8. VALIDATE     Drift firewall — response vs anchor definitions
 9. LEARN        Update session memory + promote/demote uncertain anchors
10. METER        Count tokens — input, output, baseline, savings
11. PROPOSE      If unmatched concept hits threshold → queue proposal
12. RESPOND      Clean answer to entity in their style
```

---

## 17. Performance Targets

|Metric|Target|
|---|---|
|Token reduction (30-turn session)|60–80%|
|Bootstrap overhead|~300 tokens (router-managed)|
|Break-even point|Turn 3–5|
|Drift events per session|0|
|Cross-model meaning accuracy|100%|
|Entity protocol knowledge required|0|
|Session warm-start time|Instant (memory bank pre-loaded)|

---

## 18. Versioning Roadmap

|Version|Focus|Status|
|---|---|---|
|v3.0|Core protocol — design verified|✅ This document|
|v3.1|SCV validation extension|Planned|
|v3.2|Infrastructure middleware (router implementation)|Planned|
|v4.0|Semantic router — full external anchor resolution at scale|Vision|
|v5.0|Semantic network layer — multi-router, multi-agent mesh|Vision|

---

## 19. Design Decisions Log

All decisions verified and locked during design review on 2026-03-26.

|#|Decision|Choice|Rationale|
|---|---|---|---|
|1|Entity experience|Protocol is invisible|Entity should not need to know SCP exists|
|2|Detection method|Dual-path: regex + semantic|Support both shorthand users and natural language|
|3|Source of truth|Anchor definitions|LLM must not infer meaning — anchors are canonical|
|4|Anchor injection|Minimal — only detected per turn|Save tokens, inject only what's needed|
|5|LLM awareness|SCP-aware (T1 rules)|LLM co-participates in drift prevention|
|6|False positive handling|Inject tagged uncertain, LLM decides|Avoids false negatives while letting LLM apply context|
|7|New concept handling|Router auto-proposes anchor|Protocol grows organically from usage|
|8|Multi-domain|Allowed, router infers from context|No friction — entity doesn't declare domains|
|9|Response format|Match entity's communication style|Prose in, prose out — or structured if entity prefers|
|10|Memory persistence|No pruning — all history has value|Entity's semantic history is an asset|
|11|Anchor store scope|One entity = one store|Personal semantic identity, fully owned|
|12|Entity model|Person, agent, or corporate with inheritance|Scales from individual to organization|
|13|SPF role|Meaning container — static, canonical|Runtime state handled by router memory, not SPF|
|14|Memory bank|Permanent per entity, cross-session|Router learns and improves over time|

---

## 20. Summary

SCP v3.0 is a semantic compression protocol that works behind the scenes. The entity — person, agent, or organization — communicates naturally. The router — powered by SCP — detects concepts, resolves anchors, compresses context, prevents drift, meters tokens, learns patterns, and maintains meaning across turns, sessions, and models.

The protocol is invisible. The precision is not.

---

_SCP v3.0 — github.com/yahyaedhie/scp_ _Apache 2.0 — open protocol_