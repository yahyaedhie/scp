**SCP v3.1 – T2 Anchor Pack Sub-Specification (Revised Draft with +/- Notation)**

**Component Name:** T2 Anchor Pack (Phase 2 of Bootstrap)  
**Version:** v3.1 (revised)  
**Key Change:** Direction notation updated from `↑ ↓` to easy-to-type **`+`** (increasing) and **`-`** (decreasing).  
**Token Target:** ≤ 450 tokens for full `domain:market` pack.

### 1. Purpose of T2 (Unchanged)

T2 populates the **Anchor Store** — the immutable source-of-truth for semantic resolution, Context Builder, Drift Firewall, and learning.

### 2. Direction Notation (New Section – Added at Top of T2)

```
Direction Notation (v3.1 – Easy Keyboard):
+   = increasing / rising / strengthening / expanding
-   = decreasing / falling / easing / contracting

Examples:
[WAR]+   → War/Geopolitical Risk Premium is increasing
[LIQ]-   → Liquidity constraint is easing
[CARRY]+ → Carry trade is strengthening
```

This replaces the previous `↑ ↓` arrows entirely for better usability. Old arrow notation will be supported during transition (v3.1) but deprecated in v3.2.

### 3. Standardized Anchor Block Format (Updated)

Each anchor follows this clean, parseable block:

```
[CODE] vVERSION – Expansion (Stability: HIGH/MEDIUM/LOW)

Domain: market
Definition: Full precise meaning (1-2 sentences max)
Keywords: comma, separated, list, for detection
Constraints: must-include concepts or forbidden interpretations
Directions: + (increasing), - (decreasing)
SPF Hash: [short unique hash]
Notes: Optional usage guidance or relations to other anchors
```

### 4. Example Anchors (Revised with +/-)

Here are tightened examples based on typical `domain:market` anchors:

```
[WAR] v3.1 – War / Geopolitical Risk Premium (Stability: HIGH)

Domain: market
Definition: Any armed conflict, major geopolitical tension, or credible threat of war that impacts global risk appetite, safe-haven flows, or commodity prices.
Keywords: war, conflict, invasion, geopolitical crisis, escalation, Middle East tension
Constraints: Do not confuse with minor diplomatic disputes or economic sanctions alone.
Directions: + (increasing risk premium), - (decreasing risk premium)
SPF Hash: WAR-3.1-a1f9
Notes: Frequently appears with [LIQ] and [CARRY]. Use [WAR]+ for rising tension.

[LIQ] v3.1 – Liquidity Constraint (Stability: HIGH)

Domain: market
Definition: Tightening or easing of market liquidity conditions, funding availability, or balance sheet stress for participants.
Keywords: liquidity, funding, credit crunch, balance sheet, dollar shortage
Constraints: Must relate to actual funding or market depth stress, not just price volatility.
Directions: + (tightening liquidity), - (easing liquidity)
SPF Hash: LIQ-3.1-b2e8
Notes: Often directional: [LIQ]- frequently supports risk assets.

[CARRY] v3.1 – Carry Trade Positioning (Stability: MEDIUM)

Domain: market
Definition: Positioning in high-yield versus low-yield currencies or assets, sensitive to volatility and funding conditions.
Keywords: carry trade, yield chase, funding currency, unwind
Constraints: Refers specifically to leveraged cross-asset or cross-currency positioning.
Directions: + (building carry positions), - (unwinding carry)
SPF Hash: CARRY-3.1-c7d4
Notes: Strongly linked to [LIQ] and [WAR]. [CARRY]- often accelerates during [WAR]+ events.
```

(Additional anchors like [RISK], [VOL], [SAFE] would follow the same format.)

### 5. T2 Loading Rules (MUST)

- Load only after T1 confirmation ("SCP v3.1 ACTIVE").
- Parse every anchor into the Anchor Store with its exact fields.
- Validate: unique codes, consistent versioning, valid SPF hashes.
- After loading, resolution must support both natural language and shorthand with `+` / `-` directions.
- Router may store anchors in optimized internal format (further token reduction possible).

### 6. Integration Points

- **Context Builder (Step 6):** Pulls anchors and serializes with direction (e.g., `"code": "[WAR]+", "direction": "+"` in SPF).
- **Drift Firewall (Step 8):** Validates output against Definition + Constraints + directional meaning.
- **Detection (Step 3):** Regex updated to catch `[A-Z]+[+-]?` pattern.
- **Proposal Engine:** New anchors can include direction support from birth.
