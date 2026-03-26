"""SCP Router v3.2 — Anchor Store (SQLite)"""

import json
import aiosqlite
from pathlib import Path
from app.models.anchor import Anchor, AnchorMetadata, Validation
from app.config import settings


DB_PATH = settings.db_path

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS anchors (
    id TEXT PRIMARY KEY,
    shorthand TEXT NOT NULL UNIQUE,
    expansion TEXT NOT NULL,
    definition TEXT NOT NULL,
    constraints TEXT DEFAULT '[]',
    domain TEXT NOT NULL DEFAULT 'market',
    domain_profile TEXT DEFAULT '',
    aspect TEXT DEFAULT 'technical',
    hash TEXT NOT NULL,
    version TEXT DEFAULT '3.0',
    stability TEXT DEFAULT 'high',
    validation_status TEXT DEFAULT 'valid',
    validation_confidence TEXT DEFAULT 'high',
    validation_last_checked TEXT DEFAULT ''
);
"""

CREATE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_anchors_domain ON anchors(domain);
CREATE INDEX IF NOT EXISTS idx_anchors_shorthand ON anchors(shorthand);
"""


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_TABLE)
        await db.executescript(CREATE_INDEX)
        await db.commit()


async def upsert_anchor(anchor: Anchor):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT OR REPLACE INTO anchors
            (id, shorthand, expansion, definition, constraints, domain,
             domain_profile, aspect, hash, version, stability,
             validation_status, validation_confidence, validation_last_checked)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                anchor.id,
                anchor.shorthand,
                anchor.expansion,
                anchor.definition,
                json.dumps(anchor.constraints),
                anchor.domain,
                anchor.domain_profile,
                anchor.aspect,
                anchor.hash,
                anchor.version,
                anchor.metadata.stability,
                anchor.metadata.validation.status if anchor.metadata.validation else "valid",
                anchor.metadata.validation.confidence if anchor.metadata.validation else "high",
                anchor.metadata.validation.last_checked if anchor.metadata.validation else "",
            ),
        )
        await db.commit()


def _row_to_anchor(row: aiosqlite.Row) -> Anchor:
    return Anchor(
        id=row[0],
        shorthand=row[1],
        expansion=row[2],
        definition=row[3],
        constraints=json.loads(row[4]),
        domain=row[5],
        domain_profile=row[6],
        aspect=row[7],
        hash=row[8],
        version=row[9],
        metadata=AnchorMetadata(
            stability=row[10],
            validation=Validation(
                status=row[11],
                confidence=row[12],
                last_checked=row[13],
            ),
        ),
    )


async def get_anchor_by_id(anchor_id: str) -> Anchor | None:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM anchors WHERE id = ?", (anchor_id,))
        row = await cursor.fetchone()
        return _row_to_anchor(row) if row else None


async def resolve_code(code: str, domain: str = "market") -> Anchor | None:
    """Resolve shorthand code to anchor. Accepts [WAR], WAR, or war."""
    normalized = code.strip().upper()
    if not normalized.startswith("["):
        normalized = f"[{normalized}]"

    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT * FROM anchors WHERE shorthand = ? AND domain = ?",
            (normalized, domain),
        )
        row = await cursor.fetchone()
        return _row_to_anchor(row) if row else None


async def get_all_anchors(domain: str | None = None) -> list[Anchor]:
    async with aiosqlite.connect(DB_PATH) as db:
        if domain:
            cursor = await db.execute(
                "SELECT * FROM anchors WHERE domain = ?", (domain,)
            )
        else:
            cursor = await db.execute("SELECT * FROM anchors")
        rows = await cursor.fetchall()
        return [_row_to_anchor(r) for r in rows]


async def delete_anchor(anchor_id: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("DELETE FROM anchors WHERE id = ?", (anchor_id,))
        await db.commit()
        return cursor.rowcount > 0