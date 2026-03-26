# SCP Router v3.2

> FastAPI middleware between user/agent and LLM.
> Handles anchor resolution, token metering, drift firewall, session persistence.

## Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env → set SCP_ANTHROPIC_API_KEY

# 3. Run
uvicorn app.main:app --reload --port 8000

# 4. Open docs
# http://localhost:8000/docs
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Status + loaded anchors |
| `/resolve/` | POST | Code → anchor resolution |
| `/resolve/text` | POST | Find + resolve all codes in text |
| `/resolve/expand` | POST | Replace codes with expansions |
| `/resolve/anchors` | GET | List all anchors in domain |
| `/proxy/chat` | POST | **Main** — route message through SCP to Claude |
| `/proxy/chat/dry-run` | POST | Preview what router sends (no API call) |
| `/spf/bundle` | POST | Generate SPF packet bundle (T3) |
| `/spf/packet/{code}` | GET | Single SPF packet |
| `/spf/refresh` | GET | SPF::REFRESH for mid-session |
| `/spf/export` | POST | Pasteable T3 for cross-model handoff |
| `/session/create` | POST | New session |
| `/session/{id}` | GET | Session state |
| `/session/{id}/report` | GET | Token savings report |

## Usage Examples

### Resolve a code
```bash
curl -X POST http://localhost:8000/resolve/ \
  -H "Content-Type: application/json" \
  -d '{"code": "[WAR]", "domain": "market"}'
```

```CMD

curl -X POST http://localhost:8000/proxy/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"[WAR] elevated → [LIQ] impact on [CARRY]?\",\"domain\":\"market\"}"

```

### Chat through SCP proxy
```bash
curl -X POST http://localhost:8000/proxy/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "[WAR] elevated → [LIQ] impact on [CARRY]?",
    "domain": "market"
  }'
```

### Dry-run (no API call)
```bash
curl -X POST http://localhost:8000/proxy/chat/dry-run \
  -H "Content-Type: application/json" \
  -d '{
    "message": "[WAR] elevated → [LIQ] impact on [CARRY]?",
    "domain": "market"
  }'
```

```CMD
curl -X POST http://localhost:8000/proxy/chat/dry-run ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"[WAR] elevated → [LIQ] impact on [CARRY]?\",\"domain\":\"market\"}"

```

### Export SPF for cross-model handoff
```bash
curl -X POST http://localhost:8000/spf/export \
  -H "Content-Type: application/json" \
  -d '{"domain": "market"}'
```

## Architecture

```
User/Agent → [SCP Router] → Claude API
                 │
                 ├── Anchor Store (SQLite)
                 ├── Session Store (in-memory)
                 ├── Drift Firewall
                 ├── Token Meter
                 └── SPF Packager
```

## Seed Data

`domain:market` — 6 locked codes auto-loaded on startup:

| Code | Expansion | Hash |
|------|-----------|------|
| `[WAR]` | War/Geopolitical Risk Premium | WAR1.0 |
| `[SH-C]` | Short-side Catalyst | SH-C1.0 |
| `[SH-S]` | Short-side Sentiment | SH-S1.0 |
| `[LIQ]` | Liquidity Conditions | LIQ1.0 |
| `[CARRY]` | Carry Trade Dynamics | CARRY1.0 |
| `[STACK]` | Position Stacking Risk | STACK1.0 |

## Token Metering

The router uses a char-based estimator (~4 chars/token) by default.
For production accuracy, install `tiktoken` and update `app/core/meter.py`.

## Docker

```bash
docker build -t scp-router .
docker run -p 8000:8000 --env-file .env scp-router
```

## Protocol

SCP v3.0 — github.com/yahyaedhie/scp
Apache 2.0