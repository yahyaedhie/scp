"""SCP Router v3.2 — /spf endpoints

Generate, validate, and export SPF packets for cross-model handoff.
"""

from fastapi import APIRouter
from app.models.spf import SPFPacket, SPFRefresh, SPFInitRequest, SPFBundleResponse, SPFValidation
from app.store.anchor_store import get_all_anchors, resolve_code
from app.core.meter import count_tokens
import json

router = APIRouter(prefix="/spf", tags=["spf"])


def _anchor_to_spf(anchor) -> SPFPacket:
    return SPFPacket(
        code=anchor.shorthand,
        expansion=anchor.expansion,
        domain=anchor.domain,
        anchor=anchor.id,
        hash=anchor.hash,
        version=anchor.version,
        constraints=anchor.constraints,
        domain_profile=anchor.domain_profile,
        validation=SPFValidation(
            status=anchor.metadata.validation.status if anchor.metadata.validation else "valid",
            confidence=anchor.metadata.validation.confidence if anchor.metadata.validation else "high",
            last_checked=anchor.metadata.validation.last_checked if anchor.metadata.validation else "",
        ),
    )


@router.post("/bundle", response_model=SPFBundleResponse)
async def generate_bundle(req: SPFInitRequest):
    """Generate SPF packet bundle for cross-model handoff (T3)."""
    anchors = await get_all_anchors(req.domain)

    # Filter to requested codes if specified
    if req.codes:
        normalized = [c.strip().upper() for c in req.codes]
        normalized = [f"[{c}]" if not c.startswith("[") else c for c in normalized]
        anchors = [a for a in anchors if a.shorthand in normalized]

    packets = [_anchor_to_spf(a) for a in anchors]

    # Estimate token cost of bundle
    bundle_text = json.dumps([p.model_dump() for p in packets])
    token_estimate = count_tokens(bundle_text)

    return SPFBundleResponse(
        domain=req.domain,
        packets=packets,
        token_estimate=token_estimate,
    )


@router.get("/packet/{code}")
async def get_packet(code: str, domain: str = "market"):
    """Generate a single SPF packet for a code."""
    anchor = await resolve_code(code, domain)
    if not anchor:
        return {"error": f"[UNKNOWN-CODE] {code} not found in domain:{domain}"}
    return _anchor_to_spf(anchor).model_dump()


@router.get("/refresh", response_model=SPFRefresh)
async def generate_refresh(domain: str = "market"):
    """Generate SPF::REFRESH packet for mid-session re-anchoring."""
    anchors = await get_all_anchors(domain)
    active_codes = [a.shorthand for a in anchors]

    return SPFRefresh(
        domain=domain,
        active_codes=active_codes,
    )


@router.post("/export")
async def export_for_handoff(req: SPFInitRequest):
    """Export complete T3 payload as pasteable text for cross-model handoff."""
    anchors = await get_all_anchors(req.domain)

    if req.codes:
        normalized = [c.strip().upper() for c in req.codes]
        normalized = [f"[{c}]" if not c.startswith("[") else c for c in normalized]
        anchors = [a for a in anchors if a.shorthand in normalized]

    lines = [
        f"## SCP v3.0 — SPF PACKET SET (TIER 3)",
        f"## domain:{req.domain} | Cross-model handoff payload",
        f"## Self-contained — no prior SCP knowledge needed.",
        "",
    ]

    for a in anchors:
        constraints_str = json.dumps(a.constraints)
        lines.append(
            f'SPF {{ "code":"{a.shorthand}", "expansion":"{a.expansion}", '
            f'"domain":"{a.domain}", "anchor":"{a.id}", "hash":"{a.hash}", '
            f'"version":"{a.version}", "constraints":{constraints_str}, '
            f'"domain_profile":"{a.domain_profile}" }}'
        )
        lines.append("")

    payload = "\n".join(lines)
    tokens = count_tokens(payload)

    return {
        "payload": payload,
        "token_count": tokens,
        "anchor_count": len(anchors),
        "domain": req.domain,
    }