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
from similarity import SimilarityEngine

app = FastAPI(title="SCP Router - Professional Edition", version="3.2")

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
llm_gateway = LLMGateway(Config)

class RouteRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    domain: str = "finance"
    compression: str = "moderate"
    model: Optional[str] = None
    show_stats: bool = True
    dry_run: bool = False  # New: Bypass LLM for testing

class RouteResponse(BaseModel):
    session_id: str
    response: str
    model: Optional[str] = None
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
    return {"status": "healthy", "version": "3.2", "models": ["deepseek", "claude"]}

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
        if not session_memory.get(session_id):
            session_id = session_memory.create()
    
    # Load domain-specific anchors
    anchors_dict = {}
    db_anchors = anchor_store.list_by_domain(request.domain)
    for a in db_anchors:
        anchors_dict[a["code"]] = a
    if not anchors_dict:
        anchors_dict = DEFAULT_ANCHORS
    
    # Compression phase
    compressed, compression_stats = compression_engine.compress(
        request.message, request.compression, anchors_dict
    )
    
    # Determine thresholds for this domain
    domain_config = _get_domain_config(request.domain)
    
    # LLM Execution or Dry Run
    if request.dry_run:
        assistant_response = f"[DRY-RUN] Compressed Input: {compressed}"
        model_used = "dry-run-mock"
    else:
        system_prompt = _build_system_prompt(request.domain, anchors_dict)
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
    detected_codes = [code for code in anchors_dict.keys() if code in request.message]
    
    # Drift check against domain threshold
    active_anchors = [anchors_dict[code] for code in detected_codes if code in anchors_dict]
    drift_results = drift_firewall.batch_check(
        assistant_response, 
        active_anchors, 
        domain_thresholds={request.domain: domain_config}
    )
    
    # TRI calculation
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
    
    return RouteResponse(
        session_id=session_id,
        response=assistant_response,
        model=model_used,
        metrics=metrics
    )

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