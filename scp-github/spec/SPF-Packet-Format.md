
---

# 📘 **Semantic Packet Format (SPF)**

### _Specification for portable semantic meaning units in SCP v3.0_

`/spec/SPF-Packet-Format.md`

---

## **1. Purpose**

The Semantic Packet Format (SPF) is a **portable container** for transmitting meaning across AI models, agents, and workflows.  
It ensures that shorthand, anchors, and semantic metadata remain consistent and drift‑resistant, even outside the originating environment.

---

## **2. Structure**

SPF packets are JSON‑like objects with mandatory and optional fields.

### **2.1 Example Packet**

```json
SPF {
  "type": "shorthand",
  "code": "PT app",
  "expansion": "Price-Tracking Application",
  "version": "3.0",
  "anchor": "PT-ANCHOR",
  "domain": ["technical", "msme"],
  "hash": "PT1.2",
  "metadata": {
    "created": "v2.0",
    "migrated": "v3.0",
    "stability": "high"
  }
}
```

---

## **3. Field Definitions**

| Field         | Type          | Required | Description                                                    |
| ------------- | ------------- | -------- | -------------------------------------------------------------- |
| **type**      | string        | ✔        | Defines packet type (`shorthand`, `anchor`, `hash`, `domain`). |
| **code**      | string        | ✔        | Shorthand identifier (e.g., `PT app`).                         |
| **expansion** | string        | ✔        | Full human‑readable meaning.                                   |
| **version**   | string        | ✔        | Semantic version (e.g., `3.0`).                                |
| **anchor**    | string        | ✔        | Anchor ID linked to this shorthand.                            |
| **domain**    | array[string] | ✔        | Applicable domain profiles (e.g., `technical`, `msme`).        |
| **hash**      | string        | ✔        | Semantic hash identifier (e.g., `PT1.2`).                      |
| **metadata**  | object        | optional | Tracks creation, migration, stability, and validation.         |

---

## **4. Metadata Subfields**

| Subfield       | Type   | Description                                    |
| -------------- | ------ | ---------------------------------------------- |
| **created**    | string | Version when shorthand was first created.      |
| **migrated**   | string | Version when migrated to v3.0.                 |
| **stability**  | string | Stability rating (`low`, `medium`, `high`).    |
| **validation** | object | Validation metadata (optional, SCV extension). |

---

## **5. Validation Metadata (Optional, SCV Extension)**

```json
"validation": {
  "status": "valid",
  "confidence": "high",
  "last_checked": "2026-03-24"
}
```

- **status** — `valid`, `invalid`, or `fallback`
- **confidence** — `low`, `medium`, `high`
- **last_checked** — timestamp of last validation

---

## **6. Rules**

1. **Deterministic Expansion** — same shorthand + same domain = same expansion.
2. **Anchor Binding** — every shorthand must link to an anchor.
3. **Version Integrity** — packets must include semantic version + hash.
4. **Metadata Transparency** — creation, migration, and stability must be recorded.
5. **Validation Optionality** — validation metadata is optional unless SCV is active.

---

## **7. Use Cases**

- **Cross‑model portability** — transmit meaning between LLMs.
- **Multi‑agent ecosystems** — agents share semantic packets.
- **Enterprise workflows** — anchors + shorthand remain stable across teams.
- **Compliance workflows (SCV)** — validation metadata ensures trustworthiness.

---

## **8. Compliance Checklist**

✔ Packet includes type, code, expansion, version, anchor, domain, hash  
✔ Metadata tracks creation, migration, stability  
✔ Validation metadata included if SCV is active  
✔ Packet is JSON‑like and machine‑readable  
✔ Packet maps to Semantic Compression Graph (SCG)

---

