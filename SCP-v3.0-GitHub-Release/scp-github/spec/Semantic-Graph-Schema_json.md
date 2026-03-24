
---

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Semantic Compression Graph Schema",
  "description": "Schema for representing shorthand, anchors, hashes, domains, and relationships in SCP v3.0.",
  "type": "object",
  "properties": {
    "nodes": {
      "type": "array",
      "description": "List of semantic graph nodes.",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "description": "Unique identifier for the node." },
          "type": { 
            "type": "string", 
            "enum": ["shorthand", "anchor", "hash", "domain", "concept"],
            "description": "Type of semantic node."
          },
          "label": { "type": "string", "description": "Human-readable label for the node." },
          "expansion": { "type": "string", "description": "Full expansion of shorthand or anchor meaning." },
          "domain": { 
            "type": "array", 
            "items": { "type": "string" }, 
            "description": "Applicable domain profiles (e.g., technical, MSME, education, creative)." 
          },
          "anchor": { "type": "string", "description": "Anchor ID linked to this node." },
          "version": { "type": "string", "description": "Semantic version number (e.g., 3.0, 2.1)." },
          "hash": { "type": "string", "description": "Semantic hash identifier (e.g., PT1.2)." },
          "metadata": {
            "type": "object",
            "properties": {
              "created": { "type": "string", "description": "Version when created." },
              "migrated": { "type": "string", "description": "Version when migrated." },
              "stability": { "type": "string", "enum": ["low", "medium", "high"], "description": "Stability rating." },
              "validation": {
                "type": "object",
                "properties": {
                  "status": { "type": "string", "enum": ["valid", "invalid", "fallback"], "description": "Validation status." },
                  "confidence": { "type": "string", "enum": ["low", "medium", "high"], "description": "Validation confidence." },
                  "last_checked": { "type": "string", "description": "Timestamp of last validation check." }
                }
              }
            }
          }
        },
        "required": ["id", "type", "label"]
      }
    },
    "edges": {
      "type": "array",
      "description": "List of semantic relationships between nodes.",
      "items": {
        "type": "object",
        "properties": {
          "source": { "type": "string", "description": "ID of the source node." },
          "target": { "type": "string", "description": "ID of the target node." },
          "relationship": { 
            "type": "string", 
            "enum": ["expands_to", "linked_to", "version_of", "domain_of", "inherits", "conflicts_with"],
            "description": "Type of semantic relationship."
          },
          "weight": { "type": "number", "description": "Strength of the relationship (0–1)." }
        },
        "required": ["source", "target", "relationship"]
      }
    }
  },
  "required": ["nodes", "edges"]
}
```

---

# 🔍 **How to Use This Schema**

- **Nodes** represent shorthand, anchors, hashes, domains, or concepts.
- **Edges** define relationships (expansion, version lineage, domain mapping, conflicts).
- **Metadata** tracks creation, migration, stability, and validation.
- **Validation** ensures SCV compatibility if you extend SCP into SCV.

---
