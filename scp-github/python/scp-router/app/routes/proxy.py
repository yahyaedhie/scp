"""SCP Router v3.2 — /proxy endpoint

Sits between user and Claude API.
Injects SCP system prompt (T1+T2), compresses context,
validates response, meters tokens.
"""

from fastapi import APIRouter, HTTPException
from anthropic import AsyncAnthropic
from app.config import settings
from app.models.session import ProxyRequest, ProxyResponse
from app.store.session_store import get_or_create_session, update_session
from app.core.resolver import build_system_prompt, extract_codes
from app.core.drift import validate_response
from app.core.meter import count_tokens

router = APIRouter(prefix="/proxy", tags=["proxy"])


def _get_client() -> AsyncAnthropic:
    if not settings.anthropic_api_key:
        raise HTTPException(
            status_code=500,
            detail="ANTHROPIC_API_KEY not set. Set SCP_ANTHROPIC_API_KEY env var.",
        )
    return AsyncAnthropic(api_key=settings.anthropic_api_key)


@router.post("/chat", response_model=ProxyResponse)
async def proxy_chat(req: ProxyRequest):
    """Route user message through SCP compression layer to Claude."""

    # 1. Get or create session
    session = get_or_create_session(req.session_id, req.domain)
    session.turn_count += 1

    # 2. Build SCP system prompt (T1 + T2)
    system_prompt = ""
    if req.inject_anchors:
        system_prompt = await build_system_prompt(req.domain)

    # 3. Detect codes in user message
    codes_in_message = await extract_codes(req.message)
    for code in codes_in_message:
        tag = f"[{code}]"
        if tag not in session.active_codes:
            session.active_codes.append(tag)

    # 4. Count input tokens
    input_text = system_prompt + "\n" + req.message
    input_tokens = count_tokens(input_text)

    # 5. Estimate what full prose would cost (baseline)
    # Rough estimate: each code mention in compressed form saves ~10 tokens
    baseline_extra = len(codes_in_message) * 10
    baseline_tokens = input_tokens + baseline_extra

    # 6. Call Claude API
    client = _get_client()
    try:
        message = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=settings.anthropic_max_tokens,
            system=system_prompt if system_prompt else None,
            messages=[{"role": "user", "content": req.message}],
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Claude API error: {str(e)}")

    # 7. Extract response
    response_text = ""
    for block in message.content:
        if block.type == "text":
            response_text += block.text

    # 8. Count output tokens
    output_tokens = count_tokens(response_text)

    # 9. Drift firewall check
    drift_status, drift_events = await validate_response(response_text, req.domain)

    # 10. Update session metrics
    session.tokens_input += input_tokens
    session.tokens_output += output_tokens
    session.tokens_saved += baseline_extra
    if drift_events:
        session.drift_events.extend([e.to_dict() for e in drift_events])
    update_session(session)

    # 11. Build response
    return ProxyResponse(
        session_id=session.session_id,
        response=response_text,
        turn=session.turn_count,
        tokens_input=input_tokens,
        tokens_output=output_tokens,
        tokens_saved_estimate=baseline_extra,
        drift_events=[e.to_dict() for e in drift_events],
        active_codes=session.active_codes,
    )


@router.post("/chat/dry-run")
async def proxy_dry_run(req: ProxyRequest):
    """Show what the router would send to Claude — without calling the API.
    Useful for debugging system prompt and compression.
    """
    system_prompt = ""
    if req.inject_anchors:
        system_prompt = await build_system_prompt(req.domain)

    codes_in_message = await extract_codes(req.message)

    system_tokens = count_tokens(system_prompt)
    message_tokens = count_tokens(req.message)

    return {
        "system_prompt": system_prompt,
        "user_message": req.message,
        "detected_codes": codes_in_message,
        "system_prompt_tokens": system_tokens,
        "user_message_tokens": message_tokens,
        "total_input_tokens": system_tokens + message_tokens,
        "note": "Dry run — no API call made.",
    }