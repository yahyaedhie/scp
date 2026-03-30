scp-router-personal/
├── router.py              # Main FastAPI application (Refactored v3.2)
├── similarity.py          # Unified Similarity Engine (TF-IDF)
├── llm_gateway.py         # Async LLM Gateway (DeepSeek & Claude)
├── tri.py                 # Token Retention Index (Weighted scoring)
├── drift.py               # Drift Firewall (Semantic integrity)
├── compression.py         # Semantic Compression Engine
├── anchors.py             # SQLite Anchor Store & Registry
├── memory.py              # Session Memory (Redis/Local dict)
├── config.py              # Configuration & Domain Thresholds
├── static/                # Modern Frontend Dashboard
│   ├── chat.html          # High-fidelity UI (Glassmorphism)
│   ├── index.css          # Design System (Inter/Outfit fonts)
│   └── app.js             # Modular Frontend Application Logic
├── test_logic.py          # Backend Logic Verification Suite
├── requirements.txt       # Dependencies (Python 3.12.2)
├── .env                   # API Keys & Environment Config
└── README.md              # Project Documentation & Usage