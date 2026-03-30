from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import time

from config import Config
from anchors import AnchorStore
from memory import SessionMemory
from compression import CompressionEngine
from drift import DriftFirewall
from tri import TRICalculator
from llm_gateway import LLMGateway
from similarity import SimilarityEngine, DomainClassifier

app = FastAPI(title="SCP Router - Professional Edition", version="3.3")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/static/chat.html")

# Initialize components with shared similarity engine
similarity_engine = SimilarityEngine()
anchor_store = AnchorStore(Config.ANCHOR_DB_PATH)
session_memory = SessionMemory()
compression_engine = CompressionEngine()
drift_firewall = DriftFirewall(similarity_engine=similarity_engine)
tri_calculator = TRICalculator(similarity_engine=similarity_engine)
domain_classifier = DomainClassifier(engine=similarity_engine)
llm_gateway = LLMGateway(Config)

class RouteRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    domain: str = "auto"
    compression: str = "moderate"
    model: Optional[str] = None
    show_stats: bool = True
    dry_run: bool = False  # New: Bypass LLM for testing

class RouteResponse(BaseModel):
    session_id: str
    response: str
    model: Optional[str] = None
    detected_domain: Optional[str] = None
    optimization_ready: bool = False
    metrics: Optional[dict] = None

# Default anchors
DEFAULT_ANCHORS = {
    "[WAR]": {"code": "[WAR]", "expansion": "War/Geopolitical Risk Premium", 
              "definition": "Risk premium from geopolitical conflict, sanctions, military escalation"},
    "[LIQ]": {"code": "[LIQ]", "expansion": "Liquidity Conditions",
              "definition": "Availability of capital for trading, funding, and position unwinding"},
    "[CARRY]": {"code": "[CARRY]", "expansion": "Carry Trade Dynamics",
                "definition": "Borrow low-yield currency, invest in high-yield asset; sensitive to volatility"}
}

# Helpers
def _get_domain_config(domain: str) -> Dict[str, float]:
    return Config.DOMAIN_CONFIG.get(domain, Config.DOMAIN_CONFIG["default"])

def _build_system_prompt(domain: str, anchors: Dict) -> str:
    return f"""You are an AI assistant using SCP v3.2 (Semantic Compression Protocol).
Domain: {domain}
Active anchors: {', '.join(anchors.keys())}

Guidelines:
- Use anchors like [CODE] when referencing concepts
- Provide concise, precise answers
- Maintain semantic accuracy
- If you detect drift, flag with [DRIFT-DETECTED]
"""

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "3.3", "models": ["deepseek", "claude"]}

@app.post("/v3/sessions")
async def create_session():
    session_id = session_memory.create()
    return {"session_id": session_id}

@app.post("/v3/route", response_model=RouteResponse)
async def route_message(request: RouteRequest):
    start_time = time.time()
    
    # Session Management
    if not request.session_id:
        session_id = session_memory.create()
    else:
        session_id = request.session_id
        session_data = session_memory.get(session_id)
        if not session_data:
            session_id = session_memory.create()
        elif session_data.get("blacklisted"):
            raise HTTPException(status_code=403, detail="Entity Blacklisted: Protocol Violation Level 3")
    
    # Domain Detection Logic
    effective_domain = request.domain
    if request.domain == "auto":
        effective_domain = domain_classifier.predict(request.message)
    
    # Load domain-specific anchors
    anchors_dict = {}
    db_anchors = anchor_store.list_by_domain(effective_domain)
    for a in db_anchors:
        anchors_dict[a["code"]] = a
    if not anchors_dict:
        anchors_dict = DEFAULT_ANCHORS
    
    # Compression phase
    compressed, compression_stats = compression_engine.compress(
        request.message, request.compression, anchors_dict
    )
    
    # Determine thresholds for this domain
    domain_config = _get_domain_config(effective_domain)
    
    # 1. Salted Hash Verification (v3.3 Hardening - Firewall Phase)
    import re
    detected_codes = []
    # Identify anchor tags like [WAR:b6a77322]
    matches = re.finditer(r'(\[[A-Z]+\]):([a-z0-9]+)', request.message)
    for match in matches:
        code, sent_hash = match.groups()
        anchor = anchor_store.get(code)
        if anchor:
            # Re-verify hash using local Secret Salt
            if anchor["hash"] != sent_hash:
                print(f"🚨 INTEGRITY ALERT: Hash mismatch for {code}. Sent: {sent_hash}, Expected: {anchor['hash']}")
                session_memory.log_violation(session_id)
            else:
                detected_codes.append(code)
    
    # Check if this strike makes the session blacklisted *after* checking all tags
    session_data = session_memory.get(session_id)
    if session_data and session_data.get("blacklisted"):
        raise HTTPException(status_code=403, detail="Entity Blacklisted: Protocol Violation Level 3")

    # 2. LLM Execution or Dry Run
    if request.dry_run:
        assistant_response = f"[DRY-RUN] Context: {effective_domain.upper()} | Compressed Input: {compressed}"
        model_used = "dry-run-mock"
    else:
        system_prompt = _build_system_prompt(effective_domain, anchors_dict)
        try:
            result = await llm_gateway.call(
                system_prompt=system_prompt,
                user_message=compressed,
                model=request.model
            )
            assistant_response = result["response"]
            model_used = result["model"]
        except Exception as e:
            return RouteResponse(
                session_id=session_id,
                response=f"Logic Error: {str(e)}",
                model=None,
                metrics={"error": True}
            )
    
    # Post-processing: Drift & TRI
    # Drift check against domain threshold
    active_anchors = [anchors_dict[code] for code in detected_codes if code in anchors_dict]
    drift_results = drift_firewall.batch_check(
        assistant_response, 
        active_anchors, 
        domain_thresholds={effective_domain: domain_config}
    )
    
    # TRI calculation (Bypass for Dry Run verification)
    if request.dry_run:
        tri = 0.95
    else:
        tri = tri_calculator.calculate(request.message, assistant_response)
    
    # Update Session Memory
    session_memory.add_turn(session_id, {
        "message": request.message[:200],
        "response": assistant_response[:200],
        "model": model_used,
        "tri": tri,
        "latency_ms": int((time.time() - start_time) * 1000)
    })
    
    # Build final metrics
    metrics = {
        "compression_savings": compression_stats.get("savings", 0),
        "tri": tri,
        "tri_threshold": domain_config["tri"],
        "drift_passed": all(r["passed"] for r in drift_results.values()) if drift_results else True,
        "model_used": model_used,
        "processing_time_ms": int((time.time() - start_time) * 1000)
    }
    
    if request.show_stats:
        metrics["drift_results"] = drift_results
        metrics["detected_codes"] = detected_codes
    
    # Check for Optimization Readiness
    readiness = session_memory.get_readiness_report(session_id)
    optimization_ready = readiness.get("ready", False)
    if optimization_ready:
        print(f"✨ OMNIMODEL READY: Session {session_id} is a candidate for '{readiness['domain']}' optimization.")
    else:
        print(f"DEBUG: Session {session_id} not ready yet. Reason: {readiness.get('reason')}")

    return RouteResponse(
        session_id=session_id,
        response=assistant_response,
        model=model_used,
        detected_domain=effective_domain,
        optimization_ready=optimization_ready,
        metrics=metrics
    )

@app.get("/v3/sessions/{session_id}/readiness")
async def get_session_readiness(session_id: str):
    return session_memory.get_readiness_report(session_id)

@app.post("/v3/sessions/{session_id}/optimize")
async def optimize_session_experience(session_id: str, approved_keywords: list[str]):
    readiness = session_memory.get_readiness_report(session_id)
    if not readiness["ready"]:
        return {"status": "error", "message": "Session not ready for optimization"}
    
    domain = readiness["domain"]
    
    # Global Retention Implementation (Phase 7)
    committed = []
    for keyword in approved_keywords:
        # Create a permanent anchor with "global" domain as requested
        code = f"[{keyword.upper()}]"
        expansion = f"Learned Context: {keyword}"
        definition = f"Semantic anchor autonomously extracted from high-fidelity session {session_id} in {domain} domain."
        
        # Salted hash will be generated automatically in anchor_store.create
        anchor_store.create(
            code=code,
            expansion=expansion,
            definition=definition,
            domain="global",  # Force global retention
            keywords=[keyword, domain]
        )
        committed.append(code)

    print(f"OMNIMODEL HARDENING: Global experience updated with {committed}")
    return {"status": "success", "domain": "global", "anchors": committed}

@app.get("/v3/anchors")
async def list_anchors(domain: Optional[str] = None):
    domain = domain or "finance"
    anchors = anchor_store.list_by_domain(domain)
    return {"anchors": anchors}

@app.post("/v3/anchors")
async def create_anchor(
    code: str, expansion: str, definition: str, domain: str, keywords: str = ""
):
    kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
    anchor = anchor_store.create(code, expansion, definition, domain, keywords=kw_list)
    return anchor

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)