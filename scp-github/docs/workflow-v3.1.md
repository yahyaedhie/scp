# SCP v3.1 Workflow Specification

**Status:** Locked  
**Version:** 3.1  
**Date:** April 2026  
**Author:** Yahya Edhie & Grok (Research Collaborator)

## 1. Purpose

This document defines the deterministic per-turn processing pipeline of the Semantic Compression Protocol (SCP) v3.1.

The workflow guarantees **semantic stability**, **high compression**, **drift protection**, and **portability** while remaining completely invisible to the Entity.

## 2. Bootstrap Requirement

The full pipeline activates only after successful completion of the locked bootstrap triad:
- T1 Activation (with "SCP v3.1 ACTIVE" confirmation)
- T2 Anchor Store (`domain:market` with `+`/`-` direction notation)
- T3 SPF Pack (TOON format with verbose fallback)

Router-managed bootstrap target: ~300 tokens effective.

## 3. High-Level View (Entity Perspective)

**Receive → Resolve Meaning → Build Semantic Packet → Process with Guardrails → Validate & Learn → Expand & Present**

## 4. Detailed 12-Step Per-Turn Pipeline

After bootstrap, the SCP Router executes these steps on every message:

1. **RECEIVE** — Accept raw Entity input.  
2. **REMEMBER** — Load Entity Memory Bank and Session Memory.  
3. **DETECT** — Identify concepts via shorthand regex and semantic matching.  
4. **CLASSIFY** — Score concepts by confidence level.  
5. **RESOLVE** — Retrieve versioned Anchors from the Anchor Store (source of truth).  
6. **CONTEXT** — Build prompt using TOON Anchors, compressed narrative, rules, and style.  
7. **ROUTE** — Forward compact context to any LLM.  
8. **VALIDATE** — Execute Drift Firewall and flag deviations by severity.  
9. **LEARN** — Update memory and queue new Anchor proposals.  
10. **METER** — Track tokens, baseline, and compression savings (target 60–80%).  
11. **PROPOSE** — Queue suggestions for new Anchors.  
12. **RESPOND** — Deliver natural response, showing flags only when needed.

## 5. Key Invariants (MUST)

- All meaning after bootstrap traces back to versioned Anchors from T2.
- Context Builder defaults to TOON format (verbose fallback via `[VERBOSE]`).
- Drift is always flagged with severity — never silently corrected.
- Concept coverage must reach ≥95% and savings ≥60% after early turns.
- Entity experience remains natural and invisible unless a flag or proposal is needed.

## 6. Layer Mapping

- **L1 Compression**: Steps 1, 6, 10, 12  
- **L2 Semantic**: Steps 3, 4, 5, 6, 8, 11  
- **L3 Memory**: Steps 2, 9  
- **L4 Interoperability**: Steps 6, 7 (TOON/SPF)

## 7. Success Metrics

- **Bootstrap Convergence**: ≥95% coverage + meaningful savings within first 5–10 turns  
- **Compression**: 60–80% token reduction in sustained sessions  
- **Stability**: Zero silent drift  
- **Portability**: Full session handoff via TOON packets (<5% meaning loss)

## 8. Next Development Priorities

- Formalize Drift Firewall (severity levels, recovery, audit logging)  
- Define precise Context Builder TOON injection and anchor selection rules  
- Build reference router implementation (Python)  
- Develop benchmark suite using the locked MASTER bootstrap