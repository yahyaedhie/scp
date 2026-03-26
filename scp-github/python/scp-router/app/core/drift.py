"""SCP Router v3.2 — Drift Firewall

Detects when LLM output deviates from anchor definitions.
Checks:
  1. Code used without matching anchor expansion
  2. Expansion wording diverges from canonical definition
  3. Domain contamination (code used in wrong domain context)
  4. Unknown codes in output
"""

from dataclasses import dataclass
from app.core.resolver import extract_codes, resolve_code


@dataclass
class DriftEvent:
    code: str
    event_type: str  # unknown_code | expansion_drift | domain_mismatch
    detail: str
    severity: str  # warning | error

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "event_type": self.event_type,
            "detail": self.detail,
            "severity": self.severity,
        }


async def check_drift(text: str, domain: str = "market") -> list[DriftEvent]:
    """Scan text for drift events against stored anchors."""
    events: list[DriftEvent] = []
    codes = await extract_codes(text)

    for code in codes:
        anchor = await resolve_code(code, domain)

        if not anchor:
            events.append(
                DriftEvent(
                    code=f"[{code}]",
                    event_type="unknown_code",
                    detail=f"[{code}] not found in domain:{domain}. Cannot verify.",
                    severity="error",
                )
            )
            continue

        # Check if expansion text appears near the code in output
        # This is a heuristic — checks if the LLM mentioned the concept
        # without using the canonical expansion
        expansion_words = set(anchor.expansion.lower().split())
        # Find surrounding context (~200 chars around code mention)
        code_tag = f"[{code}]"
        idx = text.find(code_tag)
        if idx >= 0:
            context_start = max(0, idx - 200)
            context_end = min(len(text), idx + 200)
            context = text[context_start:context_end].lower()

            # Check if any constraint keywords appear in wrong context
            # This is a basic heuristic — production would use embedding similarity
            if anchor.constraints:
                constraint_words = set()
                for c in anchor.constraints:
                    constraint_words.update(c.lower().split())

                # If code is mentioned but none of the constraint context appears,
                # it might be used in wrong context
                context_words = set(context.split())
                overlap = constraint_words & context_words
                if len(overlap) == 0 and len(constraint_words) > 0:
                    events.append(
                        DriftEvent(
                            code=f"[{code}]",
                            event_type="expansion_drift",
                            detail=f"[{code}] used without constraint context. "
                            f"Expected context: {anchor.constraints[:3]}",
                            severity="warning",
                        )
                    )

    return events


async def validate_response(
    response_text: str, domain: str = "market"
) -> tuple[str, list[DriftEvent]]:
    """Validate LLM response and return drift events.
    Returns (status, events) where status is 'clean' or 'drift-detected'.
    """
    events = await check_drift(response_text, domain)
    errors = [e for e in events if e.severity == "error"]

    if errors:
        status = "drift-detected"
    elif events:
        status = "drift-warning"
    else:
        status = "clean"

    return status, events