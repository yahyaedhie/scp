"""SCP Router v3.2 — Anchor Resolver"""

import re
from app.store.anchor_store import resolve_code, get_all_anchors
from app.models.anchor import ResolveResponse


# Pattern to find shorthand codes in text: [WAR], [LIQ], etc.
CODE_PATTERN = re.compile(r"\[([A-Z][A-Z0-9\-]*)\]")


async def resolve(code: str, domain: str = "market") -> ResolveResponse:
    """Resolve a single shorthand code to its anchor."""
    anchor = await resolve_code(code, domain)
    if not anchor:
        return ResolveResponse(
            code=code,
            expansion="",
            definition="",
            constraints=[],
            domain=domain,
            domain_profile="",
            anchor_id="",
            hash="",
            version="",
            status="unknown",
        )
    return ResolveResponse(
        code=anchor.shorthand,
        expansion=anchor.expansion,
        definition=anchor.definition,
        constraints=anchor.constraints,
        domain=anchor.domain,
        domain_profile=anchor.domain_profile,
        anchor_id=anchor.id,
        hash=anchor.hash,
        version=anchor.version,
        status="resolved",
    )


async def extract_codes(text: str) -> list[str]:
    """Extract all SCP shorthand codes from text."""
    return CODE_PATTERN.findall(text)


async def resolve_all_in_text(text: str, domain: str = "market") -> dict[str, ResolveResponse]:
    """Resolve all shorthand codes found in text."""
    codes = await extract_codes(text)
    results = {}
    for code in codes:
        results[code] = await resolve(code, domain)
    return results


async def expand_text(text: str, domain: str = "market") -> str:
    """Replace all shorthand codes in text with their expansions."""
    codes = await extract_codes(text)
    expanded = text
    for code in codes:
        anchor = await resolve_code(code, domain)
        if anchor:
            expanded = expanded.replace(f"[{code}]", anchor.expansion)
    return expanded


async def build_system_prompt(domain: str = "market") -> str:
    """Build T1+T2 system prompt from stored anchors."""
    from app.config import settings
    anchors = await get_all_anchors(domain)

    # T1 — Nano system prompt
    codes_block = "\n".join(
        f"{a.shorthand} = {a.expansion}" for a in anchors
    )

    t1 = f"""ROLE: You are an SCP v{settings.scp_version} compliant agent.
Expand shorthand using anchors and domain context.
Protocol Version: SCP v{settings.scp_version}  
Activation Mode: {settings.compression_mode.upper()} (anchors + shorthand codes)  
Session ID: [Auto‑Generate]  
COMPRESSION: {settings.compression_mode.upper()} | DRIFT-FIREWALL: active | VERSION: SCP v{settings.scp_version}
{codes_block}"""

    # T2 — Anchor pack
    anchor_blocks = []
    for a in anchors:
        constraints_str = ", ".join(f'"{c}"' for c in a.constraints)
        anchor_blocks.append(
            f"""{a.id} {{
  shorthand: "{a.shorthand}"
  expansion: "{a.expansion}"
  definition: "{a.definition}"
  constraints: [{constraints_str}]
  domain_profile: "{a.domain_profile}"
  hash: {a.hash} | stability: {a.metadata.stability}
}}"""
        )

    t2 = "\n\n".join(anchor_blocks)

    return f"{t1}\n\n# ANCHOR PACK\n\n{t2}"


def get_charter() -> str:
    """Return the formal SCP v3.0.2 Charter Statement."""
    return (
        "Under SCP v3.0.2, AI interaction shifts from short, token‑limited chats to long, "
        "coherent, auditable collaborations. Responses must embody continuity, efficiency, "
        "transparency, and empowerment."
    )


async def handle_commands(message: str, domain: str = "market") -> dict:
    """Parse and handle SPF commands in user message.
    Returns a dict with modifications to session or special responses.
    """
    cmd_results = {
        "show_stats": None,
        "intercept_response": None,
        "refresh_needed": False
    }

    if "SHOW STATS" in message.upper():
        cmd_results["show_stats"] = True
    elif "HIDE STATS" in message.upper():
        cmd_results["show_stats"] = False
    
    if "SPF::REFRESH" in message.upper():
        cmd_results["refresh_needed"] = True
        
    if "SPF::CHARTER" in message.upper():
        cmd_results["intercept_response"] = f"# 📜 SCP v3.0.2 Charter\n\n> {get_charter()}"

    return cmd_results
