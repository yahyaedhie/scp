
---

```json
{
  "shorthand": [
    {
      "id": "PT-app",
      "type": "shorthand",
      "label": "PT app",
      "expansion": "Price-Tracking Application",
      "domain": ["technical", "msme"],
      "anchor": "PT-ANCHOR",
      "version": "3.0",
      "hash": "PT1.2",
      "metadata": {
        "created": "v2.0",
        "migrated": "v3.0",
        "stability": "high",
        "validation": {
          "status": "valid",
          "confidence": "high",
          "last_checked": "2026-03-24"
        }
      }
    },
    {
      "id": "TA-bot",
      "type": "shorthand",
      "label": "TA bot",
      "expansion": "Teacher Assistant Bot",
      "domain": ["education"],
      "anchor": "TA-ANCHOR",
      "version": "3.0",
      "hash": "TA1.1",
      "metadata": {
        "created": "v2.0",
        "migrated": "v3.0",
        "stability": "medium",
        "validation": {
          "status": "valid",
          "confidence": "medium",
          "last_checked": "2026-03-24"
        }
      }
    },
    {
      "id": "ALUMNI",
      "type": "shorthand",
      "label": "ALUMNI",
      "expansion": "Alumni Engagement System",
      "domain": ["education", "community"],
      "anchor": "ALUMNI-ANCHOR",
      "version": "3.0",
      "hash": "AL1.0",
      "metadata": {
        "created": "v3.0",
        "migrated": "v3.0",
        "stability": "high",
        "validation": {
          "status": "valid",
          "confidence": "high",
          "last_checked": "2026-03-24"
        }
      }
    }
  ]
}
```

---

# 🔍 **How to Use This Dictionary**

- Each shorthand entry is **self‑describing** (expansion, domain, anchor, version, hash, metadata).
- Anchors (e.g., `PT-ANCHOR`, `TA-ANCHOR`) should be defined separately in `/dictionary/anchors/*.json`.
- Metadata tracks **creation, migration, stability, and validation**.
- This file can be extended with new shorthand codes as your projects evolve.

---
