"""SCP Router v3.2 — /resolve endpoints"""

from fastapi import APIRouter, HTTPException
from app.models.anchor import ResolveRequest, ResolveResponse, Anchor
from app.core.resolver import resolve, resolve_all_in_text, expand_text
from app.store.anchor_store import get_all_anchors, get_anchor_by_id

router = APIRouter(prefix="/resolve", tags=["resolve"])


@router.post("/", response_model=ResolveResponse)
async def resolve_code(req: ResolveRequest):
    """Resolve a single shorthand code to its anchor definition."""
    result = await resolve(req.code, req.domain)
    if result.status == "unknown":
        raise HTTPException(
            status_code=404,
            detail=f"[UNKNOWN-CODE] {req.code} not found in domain:{req.domain}",
        )
    return result


@router.post("/text")
async def resolve_text(body: dict):
    """Resolve all shorthand codes found in text."""
    text = body.get("text", "")
    domain = body.get("domain", "market")
    results = await resolve_all_in_text(text, domain)
    return {
        "resolved": {k: v.model_dump() for k, v in results.items()},
        "count": len(results),
    }


@router.post("/expand")
async def expand(body: dict):
    """Expand all shorthand codes in text to full form."""
    text = body.get("text", "")
    domain = body.get("domain", "market")
    expanded = await expand_text(text, domain)
    return {"original": text, "expanded": expanded}


@router.get("/anchors")
async def list_anchors(domain: str = "market"):
    """List all anchors in a domain."""
    anchors = await get_all_anchors(domain)
    return {
        "domain": domain,
        "count": len(anchors),
        "anchors": [a.model_dump() for a in anchors],
    }


@router.get("/anchor/{anchor_id}")
async def get_anchor(anchor_id: str):
    """Get a specific anchor by ID."""
    anchor = await get_anchor_by_id(anchor_id)
    if not anchor:
        raise HTTPException(
            status_code=404,
            detail=f"[ANCHOR-NOT-LOADED] {anchor_id} not found",
        )
    return anchor.model_dump()
