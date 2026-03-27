"""SCP Router v3.2 — Main Application

Semantic Compression Protocol Router
FastAPI middleware between user/agent and LLM.

Handles: anchor resolution, token metering, drift firewall, session persistence.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.store.anchor_store import init_db
from app.store.session_store import init_session_db
from app.seed_loader import seed_all, check_seeded
from app.routes import resolve, proxy, spf, session, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: init DB + seed data. Shutdown: cleanup."""
    # Init databases
    await init_db()
    await init_session_db()

    # Warn if API key is missing
    if not settings.anthropic_api_key:
        print("  [WARN] SCP_ANTHROPIC_API_KEY is not set — /proxy/chat will fail")

    # Seed default domains if empty
    if not await check_seeded("market"):
        loaded = await seed_all()
        for domain, count in loaded.items():
            print(f"  [SEED] domain:{domain} → {count} anchors loaded")
    else:
        print("  [SEED] domain:market already seeded — skipping")

    print(f"  [SCP] Router v{settings.app_version} ready")
    print(f"  [SCP] Protocol: SCP v{settings.scp_version}")
    print(f"  [SCP] Model: {settings.anthropic_model}")
    print(f"  [SCP] Drift Firewall: {'active' if settings.drift_firewall else 'inactive'}")

    yield

    # Shutdown cleanup (if needed)
    print("  [SCP] Router shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "SCP Router v3.2 — Semantic Compression Protocol middleware.\n\n"
        "Sits between user/agent and LLM. Handles anchor resolution, "
        "token metering, drift firewall, and session persistence.\n\n"
        "Protocol: SCP v3.0.2 — github.com/yahyaedhie/scp"
    ),
    lifespan=lifespan,
)

# CORS — allow all origins for dev, restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(health.router)
app.include_router(resolve.router)
app.include_router(proxy.router)
app.include_router(spf.router)
app.include_router(session.router)


@app.get("/")
async def root():
    return {
        "protocol": "SCP v3.0.2",
        "router": f"v{settings.app_version}",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "resolve": "/resolve/ — code → anchor resolution",
            "proxy": "/proxy/chat — LLM proxy with SCP injection",
            "spf": "/spf/bundle — SPF packet generation",
            "session": "/session/ — session management",
        },
    }