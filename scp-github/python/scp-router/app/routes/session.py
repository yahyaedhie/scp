"""SCP Router v3.2 — /session endpoints"""

from fastapi import APIRouter, HTTPException
from app.models.session import SessionState, TokenReport
from app.store.session_store import (
    get_session,
    list_sessions,
    delete_session,
    create_session,
)

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/create")
async def new_session(domain: str = "market"):
    """Create a new SCP session."""
    session = await create_session(domain)
    return session.model_dump()


@router.get("/{session_id}")
async def get_session_info(session_id: str):
    """Get session state."""
    session = await get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.model_dump()


@router.get("/{session_id}/report", response_model=TokenReport)
async def token_report(session_id: str):
    """Get token savings report for a session."""
    session = await get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    total_tokens = session.tokens_input + session.tokens_output
    savings_pct = (
        (session.tokens_saved / (total_tokens + session.tokens_saved) * 100)
        if (total_tokens + session.tokens_saved) > 0
        else 0
    )

    return TokenReport(
        session_id=session.session_id,
        turn_count=session.turn_count,
        tokens_input_total=session.tokens_input,
        tokens_output_total=session.tokens_output,
        tokens_saved_total=session.tokens_saved,
        savings_percent=round(savings_pct, 1),
        active_codes=session.active_codes,
        drift_events_count=len(session.drift_events),
        tri=session.tri,
        cqs=session.cqs,
    )


@router.get("/")
async def list_all_sessions():
    """List all active sessions."""
    sessions = await list_sessions()
    return {
        "count": len(sessions),
        "sessions": [
            {
                "session_id": s.session_id,
                "domain": s.domain,
                "turn_count": s.turn_count,
                "active_codes": s.active_codes,
                "last_active": s.last_active,
            }
            for s in sessions
        ],
    }


@router.delete("/{session_id}")
async def end_session(session_id: str):
    """Delete a session."""
    if await delete_session(session_id):
        return {"status": "deleted", "session_id": session_id}
    raise HTTPException(status_code=404, detail="Session not found")