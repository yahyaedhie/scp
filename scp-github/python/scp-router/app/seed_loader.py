"""SCP Router v3.2 — Seed Loader

Loads anchor seed data from seed/*.json into SQLite on startup.
"""

import json
from pathlib import Path
from app.models.anchor import Anchor, AnchorMetadata, Validation
from app.store.anchor_store import upsert_anchor, get_all_anchors


SEED_DIR = Path(__file__).parent.parent / "seed"


async def check_seeded(domain: str) -> bool:
    """Return True if domain already has anchors in the database."""
    anchors = await get_all_anchors(domain=domain)
    return len(anchors) > 0


async def seed_all() -> dict[str, int]:
    """Load all *.json files from seed/ into the database.

    Returns {domain: count} for each domain loaded.
    """
    results: dict[str, int] = {}

    for json_file in sorted(SEED_DIR.glob("*.json")):
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"  [SEED] WARNING: could not load {json_file.name}: {exc}")
            continue

        domain = data.get("domain", json_file.stem)
        raw_anchors = data.get("anchors", [])
        count = 0

        for raw in raw_anchors:
            anchor = Anchor(
                id=raw["id"],
                shorthand=raw["shorthand"],
                expansion=raw["expansion"],
                definition=raw["definition"],
                constraints=raw.get("constraints", []),
                domain=raw.get("domain", domain),
                domain_profile=raw.get("domain_profile", ""),
                aspect=raw.get("aspect", "technical"),
                hash=raw["hash"],
                version=raw.get("version", "3.0"),
                metadata=AnchorMetadata(
                    stability=raw.get("stability", "high"),
                    validation=Validation(),
                ),
            )
            await upsert_anchor(anchor)
            count += 1

        results[domain] = count

    return results
