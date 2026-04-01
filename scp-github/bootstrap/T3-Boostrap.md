**T3 SPF Pack – LOCKED for SCP v3.1**

**Locked Decisions:**
- **Format:** TOON (Token-Optimized Object Notation) as primary compression technique.
- **Header & Schema:** As shown in the final draft (keys declared once for maximum efficiency).
- **Direction Integration:** Fully aligned with locked T2 (`+` for increasing, `-` for decreasing) — both in `code` and `dir` field.
- **Verbose Fallback:** Default = TOON (dense), expandable to readable prose on explicit request (`[VERBOSE]`), debugging, or critical drift events. Router performs expansion internally with zero extra LLM cost.
- **Full Sample Pack:** The market domain anchors ([WAR]+, [LIQ]-, [CARRY]+ etc.) locked in TOON format.
- **Token Target Achieved:** ~340–380 tokens for full T3 pack (~50% savings vs JSON).
- **Integration Rules:** Context Builder uses TOON by default; portability via TOON lists; comments stripped on load.

**Full Bootstrap Triad Now Officially Locked:**

- **T1 Activation** (~118 tokens, with "SCP v3.1 ACTIVE" confirmation)
- **T2 Anchor Pack** (standardized blocks with `+`/`-` notation)
- **T3 SPF Pack** (TOON-optimized with verbose fallback)

The entire bootstrap process is now **deterministic, measurable, highly compressible, and production-ready**.

---

**Next Recommended Step: Integrate Bootstrap into Main Workflow Spec**

### SCP v3.1 Workflow Specification – Bootstrap Integration (Draft)

**1. Bootstrap Process (Phased & Locked)**

**Phase 0 – Pre-Bootstrap**  
Router checks for existing Memory Bank / Anchor Store snapshot.

**Phase 1 – T1 Activation** (Locked)  
Load minimal activation prompt.  
Success criterion: Model/Router outputs **"SCP v3.1 ACTIVE"**.

**Phase 2 – T2 Anchor Store Seeding** (Locked)  
Load domain-specific anchors (`domain:market` pack) with `+`/`-` direction support.  
Anchor Store becomes immutable source of truth.

**Phase 3 – T3 SPF/TOON Initialization** (Locked)  
Load TOON-optimized SPF packets with verbose fallback capability.  
Interoperability Layer (L4) fully enabled.

**Phase 4 – Warm-up & Convergence**  
Run internal verification (coverage ≥95%, Context Builder test).  
Bootstrap declared complete when savings projection ≥50% on first real turn.

**Total Target Cost (Router-managed):** ~300 tokens effective.  
Manual paste fallback: `MASTER_bootstrap_market_v3.1.txt` (T1+T2+T3 combined).

**2. Updated Per-Turn Workflow** (with Bootstrap References)

1. RECEIVE  
2. REMEMBER (loads post-bootstrap Memory Bank + Anchor Store)  
3. DETECT (uses T2 anchors + `+`/`-` patterns)  
4. CLASSIFY  
5. RESOLVE (from T2 Anchor Store)  
6. CONTEXT → **Build Semantic Packet** (uses T3 TOON by default; verbose fallback if requested)  
7. ROUTE  
8. VALIDATE (Drift Firewall against T2 definitions)  
9. LEARN  
10. METER  
11. PROPOSE  
12. RESPOND

**Key Invariant:** All meaning after bootstrap must trace to T2 anchors serialized via T3 TOON/SPF.
