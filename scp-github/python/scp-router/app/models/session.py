"""SCP Router v3.2 — Session Models"""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class SessionState(BaseModel):
    session_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    domain: str = "market"
    active_codes: list[str] = []
    turn_count: int = 0
    tokens_input: int = 0
    tokens_output: int = 0
    tokens_saved: int = 0
    drift_events: list[dict] = []
    tri: float = 1.0
    cqs: float = 0.0
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    last_active: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ProxyRequest(BaseModel):
    """User message to route through SCP compression."""
    message: str
    session_id: Optional[str] = None
    domain: str = "market"
    compression: str = "adaptive"  # light|moderate|deep|adaptive
    inject_anchors: bool = True  # inject T2 anchor pack into system prompt


class ProxyResponse(BaseModel):
    session_id: str
    response: str
    turn: int
    tokens_input: int
    tokens_output: int
    tokens_saved_estimate: int
    drift_events: list[dict] = []
    active_codes: list[str] = []
    tri: float = 1.0
    cqs: float = 0.0


class TokenReport(BaseModel):
    session_id: str
    turn_count: int
    tokens_input_total: int
    tokens_output_total: int
    tokens_saved_total: int
    savings_percent: float
    active_codes: list[str]
    drift_events_count: int
    tri: float = 1.0
    cqs: float = 0.0