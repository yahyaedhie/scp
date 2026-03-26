"""SCP Router v3.2 — Session Store (In-Memory)"""

from datetime import datetime
from app.models.session import SessionState


# In-memory store — upgrade to Redis for production
_sessions: dict[str, SessionState] = {}


def create_session(domain: str = "market") -> SessionState:
    session = SessionState(domain=domain)
    _sessions[session.session_id] = session
    return session


def get_session(session_id: str) -> SessionState | None:
    return _sessions.get(session_id)


def get_or_create_session(session_id: str | None, domain: str = "market") -> SessionState:
    if session_id and session_id in _sessions:
        session = _sessions[session_id]
        session.last_active = datetime.utcnow().isoformat()
        return session
    return create_session(domain)


def update_session(session: SessionState):
    session.last_active = datetime.utcnow().isoformat()
    _sessions[session.session_id] = session


def delete_session(session_id: str) -> bool:
    return _sessions.pop(session_id, None) is not None


def list_sessions() -> list[SessionState]:
    return list(_sessions.values())