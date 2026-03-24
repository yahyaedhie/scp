
---

# 📘 **Compressed vs Expanded Examples**

### _Demonstrations of SCP v3.0 shorthand expansion_

`/examples/compressed-vs-expanded.md`

---

## **Overview**

SCP v3.0 uses shorthand + anchors to compress meaning.  
This file shows how compressed shorthand expands into full meaning across different domains.

---

# **1. Example: PT app**

### **Compressed Form**

```
PT app
```

### **Expanded Form (via PT-ANCHOR)**

```
Price-Tracking Application
- Technical Domain: Cloud-first architecture for monitoring product prices
- MSME Domain: Mobile-first tracker for small businesses
- Anchor: PT-ANCHOR
- Hash: PT1.2
- Version: 3.0
```

---

# **2. Example: TA bot**

### **Compressed Form**

```
TA bot
```

### **Expanded Form (via TA-ANCHOR)**

```
Teacher Assistant Bot
- Education Domain: AI-powered assistant for classroom and remote learning
- Anchor: TA-ANCHOR
- Hash: TA1.1
- Version: 3.0
```

---

# **3. Example: ALUMNI**

### **Compressed Form**

```
ALUMNI
```

### **Expanded Form (via ALUMNI-ANCHOR)**

```
Alumni Engagement System
- Education Domain: Alumni engagement for schools and universities
- Community Domain: Community-driven alumni collaboration
- Anchor: ALUMNI-ANCHOR
- Hash: AL1.0
- Version: 3.0
```

---

# **4. Example: Deep Compression with Hash**

### **Compressed Form**

```
PT1.2
```

### **Expanded Form (via Semantic Graph)**

```
Price-Tracking Application (PT app)
- Anchor: PT-ANCHOR
- Expansion: Price-Tracking Application
- Domain Profiles: Technical, MSME
- Version: 3.0
- Stability: High
```

---

# **5. Example: Semantic Packet Format (SPF)**

### **Compressed Form**

```
SPF { code: "PT app", version: "3.0", anchor: "PT-ANCHOR", hash: "PT1.2" }
```

### **Expanded Form**

```
Price-Tracking Application
- Technical Domain: Cloud-first architecture
- MSME Domain: Mobile-first tracker
- Anchor: PT-ANCHOR
- Hash: PT1.2
- Metadata: { created: v2.0, migrated: v3.0, stability: high }
```

---

# **Summary**

- **Compressed shorthand** saves tokens.
- **Anchors + hashes** ensure drift-free expansion.
- **SPF packets** make meaning portable across models and agents.

---

