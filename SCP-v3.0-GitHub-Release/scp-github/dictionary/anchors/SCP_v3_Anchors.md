
---

### 📂 `/dictionary/anchors/PT-ANCHOR.json`

```json
{
  "id": "PT-ANCHOR",
  "type": "anchor",
  "label": "Price-Tracking Application Anchor",
  "definition": "Canonical definition of the price-tracking application concept.",
  "constraints": [
    "Must track product prices across multiple sources",
    "Must support alerts for price changes",
    "Must maintain portability across models"
  ],
  "goals": [
    "Enable MSMEs to monitor market prices",
    "Provide technical scalability for enterprise use",
    "Ensure semantic stability across AI workflows"
  ],
  "domain_profiles": {
    "technical": "Cloud-first architecture for price monitoring",
    "msme": "Mobile-first tracker for small businesses"
  },
  "versions": ["PT1.0", "PT1.1", "PT1.2"],
  "links": ["SCP-ANCHOR"],
  "metadata": {
    "created": "v2.0",
    "migrated": "v3.0",
    "stability": "high"
  }
}
```

---

### 📂 `/dictionary/anchors/TA-ANCHOR.json`

```json
{
  "id": "TA-ANCHOR",
  "type": "anchor",
  "label": "Teacher Assistant Bot Anchor",
  "definition": "Canonical definition of the teacher assistant bot concept.",
  "constraints": [
    "Must support student Q&A",
    "Must integrate with Telegram or similar platforms",
    "Must maintain semantic clarity across educational contexts"
  ],
  "goals": [
    "Provide scalable AI support for teachers",
    "Enable adaptive learning for students",
    "Ensure drift-free educational workflows"
  ],
  "domain_profiles": {
    "education": "AI-powered assistant for classroom and remote learning"
  },
  "versions": ["TA1.0", "TA1.1"],
  "links": ["SCP-ANCHOR"],
  "metadata": {
    "created": "v2.0",
    "migrated": "v3.0",
    "stability": "medium"
  }
}
```

---

### 📂 `/dictionary/anchors/ALUMNI-ANCHOR.json`

```json
{
  "id": "ALUMNI-ANCHOR",
  "type": "anchor",
  "label": "Alumni Engagement System Anchor",
  "definition": "Canonical definition of alumni engagement and community management.",
  "constraints": [
    "Must support alumni communication",
    "Must track alumni participation",
    "Must integrate with educational institutions"
  ],
  "goals": [
    "Strengthen alumni networks",
    "Enable community-driven projects",
    "Preserve semantic continuity across education and community domains"
  ],
  "domain_profiles": {
    "education": "Alumni engagement for schools and universities",
    "community": "Community-driven alumni collaboration"
  },
  "versions": ["AL1.0"],
  "links": ["SCP-ANCHOR"],
  "metadata": {
    "created": "v3.0",
    "migrated": "v3.0",
    "stability": "high"
  }
}
```

---

# 🔍 **How to Use These Anchors**

- Each anchor is the **authoritative semantic container** for its shorthand.
- Anchors prevent drift by storing definitions, constraints, goals, and domain profiles.
- Anchors are linked to shorthand codes via the `anchor` field in `/dictionary/shorthand.json`.
- Anchors can reference each other (`links`) to form semantic ecosystems.

---

