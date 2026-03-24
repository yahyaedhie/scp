# Contributing to SCP v3.0

Thank you for contributing to the Semantic Compression Protocol.

---

## What You Can Contribute

| Type | Examples |
|---|---|
| **New domain packs** | domain:legal, domain:healthcare, domain:finance |
| **New anchor definitions** | Extend existing domains |
| **Reference implementations** | Python, JS, API wrappers |
| **Test cases** | Cross-model expansion tests |
| **Bootstrap templates** | Model-specific optimizations |
| **Documentation** | Clarifications, translations |

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

### 2. Shorthand format
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
    "stability": "low|medium|high",
    "validation": {
      "status": "valid",
      "confidence": "low|medium|high",
      "last_checked": "YYYY-MM-DD"
    }
  }
}
```

### 3. Anchor format
```json
{
  "id": "CODE-ANCHOR",
  "type": "anchor",
  "label": "Human readable label",
  "definition": "Canonical definition — precise and unambiguous.",
  "constraints": [
    "constraint 1",
    "constraint 2",
    "constraint 3"
  ],
  "domain_profiles": {
    "your-domain": "domain-specific expansion"
  },
  "versions": ["CODE1.0"],
  "metadata": {
    "created": "v3.0",
    "stability": "high"
  }
}
```

---

## Contribution Rules

1. **Bidirectional verification** — test expansion works both ways before submitting
2. **Determinism** — same shorthand + same domain must always = same expansion
3. **No ambiguity** — anchor definition must be precise, not interpretable
4. **Stability rating** — be honest about stability level
5. **Domain isolation** — codes must not bleed across domains

---

## Pull Request Checklist

```
[ ] shorthand.json follows schema
[ ] anchor.json follows schema
[ ] expansion tested on minimum 2 models
[ ] no conflict with existing codes
[ ] stability rating justified
[ ] domain isolation verified
```

---

## Code of Conduct

- Propose codes when concept repeats 2+ times across contributions
- Flag conflicts — never silently override existing definitions
- Respect anchor authorship — propose changes, don't overwrite

---

*Questions? Open an issue.*
