"""SCP Router v3.2 — SPF Packet Models"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class SPFValidation(BaseModel):
    status: str = "valid"
    confidence: str = "high"
    last_checked: str = Field(default_factory=lambda: date.today().isoformat())


class SPFPacket(BaseModel):
    """Semantic Packet Format — portable meaning unit."""
    code: str  # "[WAR]"
    expansion: str
    domain: str
    anchor: str  # anchor ID
    hash: str
    version: str = "3.0"
    constraints: list[str] = []
    domain_profile: str = ""
    validation: Optional[SPFValidation] = None


class SPFRefresh(BaseModel):
    """Mid-session re-anchor packet."""
    protocol: str = "SCP v3.0"
    type: str = "mid-session-refresh"
    domain: str
    active_codes: list[str]
    rules: list[str] = [
        "shorthand+domain → fixed meaning always",
        "flag drift — never silently correct",
        "output: structured only",
    ]
    drift_firewall: str = "active"


class SPFInitRequest(BaseModel):
    """Request to generate SPF::INIT for cross-model handoff."""
    domain: str = "market"
    codes: list[str] = []  # empty = all codes in domain


class SPFBundleResponse(BaseModel):
    """Bundle of SPF packets for export."""
    protocol: str = "SCP v3.0"
    domain: str
    packets: list[SPFPacket]
    token_estimate: int = 0