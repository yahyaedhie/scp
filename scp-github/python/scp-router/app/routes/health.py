"""SCP Router v3.2 — /health endpoint"""

from fastapi import APIRouter
from app.config import settings
from app.store.anchor_store import get_all_anchors

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    """Health check + router status."""
    anchors = await get_all_anchors()
    domains = list(set(a.domain for a in anchors))

    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "scp_version": settings.scp_version,
        "model": settings.anthropic_model,
        "drift_firewall": settings.drift_firewall,
        "compression_mode": settings.compression_mode,
        "anchors_loaded": len(anchors),
        "domains_active": domains,
    }