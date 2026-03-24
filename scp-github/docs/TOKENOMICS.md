# LLM Tokenomics — Why SCP Exists

`/docs/TOKENOMICS.md`

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

| Turn | Input Tokens Sent |
|---|---|
| 1 | ~200 |
| 10 | ~2,000 |
| 50 | ~10,000 |
| 100 | ~20,000 |

Two costs per turn:
- **Input tokens** — everything sent to the model
- **Output tokens** — the model's response

Both are billed. Both accumulate.

---

## The Context Window Ceiling

Every model has a fixed context limit:

| Model | Context Limit |
|---|---|
| Claude Sonnet | 200K tokens |
| GPT-4o | 128K tokens |
| Gemini Pro | 1M tokens |
| Llama 3 70B | 8K tokens |

When the ceiling is hit:
- Oldest turns are dropped silently
- Early anchor definitions scroll out of context
- Model loses protocol understanding
- Accuracy degrades — drift begins

---

## The Energy Dimension

Every token processed = GPU compute = energy consumed.

```
Without compression:
  Full prose history processed every turn
  Redundant tokens recomputed turn after turn
  Same information processed 100x across a session

With SCP:
  Compressed history processed every turn
  60–80% fewer tokens
  60–80% less redundant computation
```

At scale:
- Millions of concurrent users
- Billions of turns per day
- Each turn resending full history
- **= Massive redundant energy consumption globally**

This is the infrastructure problem SCP addresses at the protocol level.

---

## What SCP Changes

| Without SCP | With SCP |
|---|---|
| "War/Geopolitical Risk Premium elevated" (~8 tokens) | `[WAR]↑` (~3 tokens) |
| Full prose response (~150 tokens) | Structured compressed response (~25 tokens) |
| History grows unbounded | History grows slowly |
| Context ceiling hit ~turn 100 | Context ceiling hit ~turn 400+ |
| Accuracy degrades late-session | Accuracy stable |

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

Agentic systems amplify the problem:

```
Agent 1 → calls Agent 2 → calls Agent 3 → calls Agent 4

Each agent:
  Receives full context from previous agent
  Adds its own system prompt
  Adds tool call outputs
  Adds its own processing
  = context explosion at every hop
```

SCP + SPF packets:
```
Agent 1 → SPF packet → Agent 2 → SPF packet → Agent 3

Each hop:
  ~70 tokens instead of thousands
  Full meaning preserved
  Zero drift
```

---

## Summary

| Concept | Reality |
|---|---|
| Tokens | Economic units of LLM computation |
| Input tokens | Everything sent to model — including all history |
| Output tokens | Model response |
| Context window | Fixed ceiling — your working memory budget |
| Session reset | Clears everything — start fresh |
| SCP role | Compress history → slower cost growth → more turns |
| SPF role | Preserve meaning across session resets |
| Energy role | Fewer tokens = less compute = less energy |

---

*SCP treats tokens as what they are: scarce economic and energy resources.*
