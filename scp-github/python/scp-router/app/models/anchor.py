"""SCP Router v3.2 — Anchor Models"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class Validation(BaseModel):
    status: str = "valid"  # valid|invalid|fallback
    confidence: str = "high"  # low|medium|high
    last_checked: str = Field(default_factory=lambda: date.today().isoformat())


class AnchorMetadata(BaseModel):
    created: str = "v3.0"
    migrated: str = "v3.0"
    stability: str = "high"  # low|medium|high
    validation: Optional[Validation] = None


class Anchor(BaseModel):
    id: str  # e.g. "WAR-ANCHOR"
    shorthand: str  # e.g. "[WAR]"
    expansion: str  # e.g. "War/Geopolitical Risk Premium"
    definition: str
    constraints: list[str] = []
    domain: str = "market"
    domain_profile: str = ""
    aspect: str = "technical"
    hash: str  # e.g. "WAR1.0"
    version: str = "3.0"
    metadata: AnchorMetadata = Field(default_factory=AnchorMetadata)


class AnchorCreate(BaseModel):
    """Input model for creating an anchor."""
    id: str
    shorthand: str
    expansion: str
    definition: str
    constraints: list[str] = []
    domain: str = "market"
    domain_profile: str = ""
    aspect: str = "technical"
    hash: str
    version: str = "3.0"
    stability: str = "high"


class ResolveRequest(BaseModel):
    code: str  # e.g. "[WAR]" or "WAR"
    domain: str = "market"


class ResolveResponse(BaseModel):
    code: str
    expansion: str
    definition: str
    constraints: list[str]
    domain: str
    domain_profile: str
    anchor_id: str
    hash: str
    version: str
    status: str = "resolved"  # resolved|unknown|not-loaded