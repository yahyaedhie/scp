# LLM Tokenomics — Why SCP Exists

`/docs/TOKENOMICS.md`

*Updated: March 2026*

---

## The Physics of LLMs

Before understanding SCP, you need to understand how LLMs consume tokens.

---

## Every Turn Resends Everything

```
Turn 1 input:
  [system prompt] + [your message 1]

Turn 2 input:
  [system prompt] + [message 1] + [response 1] + [your message 2]

Turn N input:
  [system prompt] + [all previous messages] + [all previous responses] + [your message N]
```

**Full conversation history is resent to the model every single turn.**

This is not a bug — it is how the Transformer architecture works.
The attention mechanism requires seeing all tokens simultaneously.
There is no persistent memory. The model re-reads everything, every turn.

---

## Token Cost Is Cumulative

| Turn | Input Tokens Sent | Approx. Cost (Claude Sonnet) |
|---|---|---|
| 1 | ~200 | $0.0006 |
| 10 | ~2,000 | $0.006 |
| 50 | ~10,000 | $0.03 |
| 100 | ~20,000 | $0.06 |

Two costs per turn:
- **Input tokens** — everything sent to the model
- **Output tokens** — the model's response

Both are billed. Both accumulate.

A 100-turn session with a mid-tier model costs ~$0.06 in input alone — per user, per session.
At 1M concurrent sessions/day, that is $60,000/day in input tokens — before a single output is generated.

---

## API Pricing Landscape (March 2026)

Token prices have dropped ~80% year-over-year, but volume is growing faster than prices are falling.

### Flagship Models

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Context Window |
|---|---|---|---|
| Claude Opus 4.6 | $5.00 | $25.00 | 200K |
| Claude Sonnet 4.6 | $3.00 | $15.00 | 200K |
| Claude Haiku 4.5 | $0.25 | $1.25 | 200K |
| GPT-5.2 | $1.75 | $14.00 | 128K |
| GPT-5.2 Pro | $21.00 | $168.00 | 128K |
| Gemini 2.5 Pro | $1.25 | $10.00 | 1M |
| Gemini 2.5 Flash | $0.30 | $2.50 | 1M |
| DeepSeek V3.2 | $0.28 | $0.42 | 128K |

### Budget Models

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Context Window |
|---|---|---|---|
| GPT-5 nano | $0.05 | $0.40 | 128K |
| GPT-5 mini | $0.25 | $2.00 | 128K |
| Gemini 2.0 Flash-Lite | $0.075 | $0.30 | 1M |
| Mistral Small | $0.20 | $0.60 | 32K |

*Sources: Official provider pricing pages, March 2026.*

### Cost Reduction Mechanisms

| Mechanism | Savings | Notes |
|---|---|---|
| Prompt caching | Up to 90% on cached input | Anthropic, OpenAI, Google all support |
| Batch API | 50% off | Async processing within 24hrs |
| Model routing | 60–80% | Route simple tasks to cheap models |
| **SCP compression** | **60–80%** | **Fewer tokens sent — compounds every turn** |

**Key insight:** Prompt caching and SCP are complementary, not competing.
Caching reduces the cost of tokens already sent. SCP reduces the number of tokens that need to be sent in the first place.

```
Without SCP:    20,000 tokens × $3.00/1M = $0.06 per turn
With caching:   20,000 tokens × $0.30/1M = $0.006 per turn (90% saved)
With SCP:        6,000 tokens × $3.00/1M = $0.018 per turn (70% saved)
With SCP+cache:  6,000 tokens × $0.30/1M = $0.0018 per turn (97% saved)
```

SCP + caching = compounding savings at every layer.

---

## The Context Window Ceiling

Every model has a fixed context limit:

| Model Family | Context Limit | Notes |
|---|---|---|
| Claude Sonnet/Opus 4.6 | 200K tokens | Effective ~150K before degradation |
| GPT-5.2 | 128K tokens | Extended context available |
| Gemini 2.5 Pro | 1M tokens | Largest available context |
| DeepSeek V3.2 | 128K tokens | |
| Llama 4 Maverick | 1M tokens | Open-source, self-hosted |

When the ceiling is hit:
- Oldest turns are dropped silently
- Early anchor definitions scroll out of context
- Model loses protocol understanding
- Accuracy degrades — drift begins

**Even with 1M token windows, the economics remain the same:**
more tokens = more compute = more cost = more energy.
Larger windows do not solve the redundancy problem — they defer it.

---

## The Energy Dimension

Every token processed = GPU compute = energy consumed.

### The Scale of the Problem

Global data center electricity consumption reached an estimated 415 TWh in 2024 — roughly 1.5% of global electricity. By 2030, this is projected to nearly double to ~945 TWh (IEA base case), approaching 3% of global consumption — equivalent to the entire energy demand of Japan.

AI-specific servers consumed an estimated 53–76 TWh in 2024 in the US alone. Inference — running trained models for end users — now dominates, accounting for 80–90% of total AI energy consumption at fleet scale. A single AI chatbot query can consume 10× more energy than a standard web search.

### Where SCP Fits

```
Without compression:
  Full prose history processed every turn
  Redundant tokens recomputed turn after turn
  Same information processed 100× across a session

With SCP:
  Compressed history processed every turn
  60–80% fewer tokens
  60–80% less redundant computation per session
```

At scale:
- Billions of AI queries per day globally
- Each query resending full history
- Each redundant token = wasted GPU cycles = wasted electricity
- **SCP addresses this at the protocol level — before the hardware, before the model**

The industry has focused on training energy costs and hardware efficiency.
Inference redundancy — the daily, continuous, compounding cost — remains largely unaddressed at the protocol level.

---

## What SCP Changes

| Without SCP | With SCP |
|---|---|
| "War/Geopolitical Risk Premium elevated" (~8 tokens) | `[WAR]↑` (~3 tokens) |
| Full prose response (~150 tokens) | Structured compressed response (~25 tokens) |
| History grows unbounded | History grows slowly |
| Context ceiling hit ~turn 100 | Context ceiling hit ~turn 400+ |
| Accuracy degrades late-session | Accuracy stable |
| Full cost per token per turn | 60–80% fewer tokens billed |

---

## Real Cost Modeling

### Scenario: Daily Market Analysis (domain:market)

**Assumptions:**
- 50 turns/session, 2 sessions/day
- Mid-tier model (Claude Sonnet 4.6: $3/$15 per 1M)
- 6 active shorthand codes, ~10 mentions per session

**Without SCP:**

| Metric | Value |
|---|---|
| Avg input tokens/turn at T50 | ~10,000 |
| Total input tokens/session | ~250,000 |
| Total output tokens/session | ~75,000 |
| Input cost/session | $0.75 |
| Output cost/session | $1.13 |
| **Daily cost (2 sessions)** | **$3.76** |
| **Monthly cost (30 days)** | **$112.80** |

**With SCP v3.0:**

| Metric | Value |
|---|---|
| Avg input tokens/turn at T50 | ~3,000 |
| Total input tokens/session | ~75,000 |
| Total output tokens/session | ~20,000 |
| Input cost/session | $0.23 |
| Output cost/session | $0.30 |
| **Daily cost (2 sessions)** | **$1.06** |
| **Monthly cost (30 days)** | **$31.80** |

**Savings: ~72% → $81/month for a single user on a single domain.**

### Scenario: Enterprise Multi-Agent Pipeline

**Assumptions:**
- 4-agent chain, each agent adds system prompt + tool calls
- 100 pipeline runs/day
- Without SCP: ~15,000 tokens per hop
- With SCP + SPF: ~2,000 tokens per hop

| Metric | Without SCP | With SCP |
|---|---|---|
| Tokens per pipeline run | ~60,000 | ~8,000 |
| Daily token volume | 6M | 800K |
| Daily cost (Sonnet) | $18 input + $X output | $2.40 input + $X output |
| **Monthly cost (input only)** | **~$540** | **~$72** |

At 1,000 pipeline runs/day, multiply by 10×.
At enterprise scale with thousands of users: the savings become material infrastructure cost.

---

## Session Architecture

```
WRONG approach:
  One session → run until context ceiling
  → accuracy degrades → restart from scratch

RIGHT approach:
  Session 1 (turns 1–50) → export SPF packets
  Session 2 (turns 1–50) → load [INIT] + inject SPF packets
  Session N → continue with full meaning, zero token debt
```

**SPF packets are the memory bridge between sessions.**
**[INIT] bootstrap is the protocol bridge between sessions.**

---

## Why This Matters for Agentic AI

Agentic systems amplify the token problem at every hop:

```
Agent 1 → calls Agent 2 → calls Agent 3 → calls Agent 4

Each agent:
  Receives full context from previous agent
  Adds its own system prompt
  Adds tool call outputs
  Adds its own processing
  = context explosion at every hop
```

SCP + SPF packets compress the handoff:

```
Agent 1 → SPF packet → Agent 2 → SPF packet → Agent 3

Each hop:
  ~70 tokens instead of thousands
  Full meaning preserved
  Zero drift
  Deterministic expansion at destination
```

### The Agent Cost Multiplier

Without SCP, agentic cost scales multiplicatively:

```
N agents × M hops × full context per hop = N×M× cost

With SCP:
N agents × M hops × compressed context per hop = N×M× (0.2 × cost)
```

As agentic AI scales from pilot to production in 2026–2027, this multiplier becomes the dominant cost factor.
SCP addresses it at the protocol layer.

---

## SCP Router v3.2 — Middleware Architecture

SCP Router sits between client and model as infrastructure middleware:

```
┌──────────┐     ┌──────────────┐     ┌─────────┐
│  Client   │────▶│  SCP Router  │────▶│  Model  │
│ (user/    │◀────│  v3.2        │◀────│  (any   │
│  agent)   │     │              │     │  vendor) │
└──────────┘     │  - compress  │     └─────────┘
                  │  - validate  │
                  │  - anchor    │
                  │  - meter     │
                  │  - firewall  │
                  └──────────────┘
```

**Token metering happens at the router level:**
- Input compressed before model sees it
- Output validated against anchors
- Drift detected algorithmically
- Token savings measured per session
- Works with any model, any vendor

This makes SCP savings transparent and measurable — not behavioral, but infrastructural.

---

## Interaction With Provider Optimizations

| Provider Feature | What It Does | SCP Interaction |
|---|---|---|
| Prompt caching | Reduces cost of repeated system prompts | SCP reduces what needs caching |
| Batch API | 50% off for async | SCP reduces batch payload size |
| Model routing | Cheap models for simple tasks | SCP compressed context fits smaller models |
| Extended context | Larger windows | SCP extends effective window 3–5× further |
| Fine-tuning | Baked-in knowledge | SCP provides runtime knowledge without retraining |

**SCP is not competing with these features. It compounds their benefit.**

---

## Summary

| Concept | Reality |
|---|---|
| Tokens | Economic and energy units of LLM computation |
| Input tokens | Everything sent to model — including all history |
| Output tokens | Model response — always more expensive per token |
| Context window | Fixed ceiling — your working memory budget |
| Session reset | Clears everything — start fresh |
| Prompt caching | Reduces cost of repeated tokens — does not reduce token count |
| SCP role | Compress history → fewer tokens → slower cost growth → more turns |
| SPF role | Preserve meaning across session resets and model handoffs |
| SCP Router | Middleware — compress/validate/meter at infrastructure level |
| Energy role | Fewer tokens = less compute = less energy at planetary scale |

---

## The Bottom Line

```
2024 data center electricity:  ~415 TWh globally
2030 projection:               ~945 TWh (IEA base case)
AI inference share:            80–90% of AI compute
Redundant token reprocessing:  the invisible cost nobody names

SCP target:
  60–80% token reduction per session
  × millions of concurrent sessions
  × billions of turns per day
  = measurable reduction in inference energy consumption

Not as a side effect.
As the primary design goal.
```

---

*SCP treats tokens as what they are: scarce economic and energy resources.*
*The cheapest token is the one you never send.*

---

*SCP v3.0 — github.com/yahyaedhie/scp*
*Apache 2.0 — open protocol, open future*