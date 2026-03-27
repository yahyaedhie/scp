"""SCP Router v3.2 — Session Store (In-Memory)"""

import json
import aiosqlite
from datetime import datetime
from app.models.session import SessionState
from app.config import settings

DB_PATH = settings.db_path
CREATE_SESSIONS_TABLE = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    turn_count INTEGER DEFAULT 0,
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    tokens_saved INTEGER DEFAULT 0,
    active_codes TEXT DEFAULT '[]',
    drift_events TEXT DEFAULT '[]',
    tri REAL DEFAULT 1.0,
    cqs REAL DEFAULT 0.0,
    last_active TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""

async def init_session_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_SESSIONS_TABLE)
        await db.commit()

async def create_session(domain: str = "market") -> SessionState:
    session = SessionState(domain=domain)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO sessions 
            (session_id, domain, turn_count, tokens_input, tokens_output, 
             tokens_saved, active_codes, drift_events, tri, cqs, last_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session.session_id,
                session.domain,
                session.turn_count,
                session.tokens_input,
                session.tokens_output,
                session.tokens_saved,
                json.dumps(session.active_codes),
                json.dumps(session.drift_events),
                session.tri,
                session.cqs,
                session.last_active,
                session.created_at,
            ),
        )
        await db.commit()
    return session

async def get_session(session_id: str) -> SessionState | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
        row = await cursor.fetchone()
        if not row:
            return None
        return SessionState(
            session_id=row["session_id"],
            domain=row["domain"],
            turn_count=row["turn_count"],
            tokens_input=row["tokens_input"],
            tokens_output=row["tokens_output"],
            tokens_saved=row["tokens_saved"],
            active_codes=json.loads(row["active_codes"]),
            drift_events=json.loads(row["drift_events"]),
            tri=row["tri"],
            cqs=row["cqs"],
            last_active=row["last_active"],
            created_at=row["created_at"],
        )

async def get_or_create_session(session_id: str | None, domain: str = "market") -> SessionState:
    if session_id:
        session = await get_session(session_id)
        if session:
            session.last_active = datetime.utcnow().isoformat()
            await update_session(session)
            return session
    return await create_session(domain)

async def update_session(session: SessionState):
    session.last_active = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """UPDATE sessions SET
            turn_count = ?, tokens_input = ?, tokens_output = ?, 
            tokens_saved = ?, active_codes = ?, drift_events = ?, 
            tri = ?, cqs = ?, last_active = ?
            WHERE session_id = ?""",
            (
                session.turn_count,
                session.tokens_input,
                session.tokens_output,
                session.tokens_saved,
                json.dumps(session.active_codes),
                json.dumps(session.drift_events),
                session.tri,
                session.cqs,
                session.last_active,
                session.session_id,
            ),
        )
        await db.commit()

async def delete_session(session_id: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        await db.commit()
        return cursor.rowcount > 0

async def list_sessions() -> list[SessionState]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM sessions")
        rows = await cursor.fetchall()
        return [
            SessionState(
                session_id=row["session_id"],
                domain=row["domain"],
                turn_count=row["turn_count"],
                tokens_input=row["tokens_input"],
                tokens_output=row["tokens_output"],
                tokens_saved=row["tokens_saved"],
                active_codes=json.loads(row["active_codes"]),
                drift_events=json.loads(row["drift_events"]),
                tri=row["tri"],
                cqs=row["cqs"],
                last_active=row["last_active"],
                created_at=row["created_at"],
            )
            for row in rows
        ]