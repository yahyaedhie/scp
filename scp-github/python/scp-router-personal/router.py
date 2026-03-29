from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
import uuid

from config import Config
from anchors import AnchorStore
from memory import SessionMemory
from compression import CompressionEngine
from drift import DriftFirewall
from tri import TRICalculator
from llm_gateway import LLMGateway  # Add this

app = FastAPI(title="SCP Router - Personal Edition", version="3.2")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Redirect root to chat
@app.get("/")
async def root():
    return RedirectResponse(url="/static/chat.html")

# Initialize components
anchor_store = AnchorStore(Config.ANCHOR_DB_PATH)
session_memory = SessionMemory()
compression_engine = CompressionEngine()
drift_firewall = DriftFirewall(Config.DRIFT_THRESHOLD)
tri_calculator = TRICalculator()
llm_gateway = LLMGateway(Config)  # Add this

class RouteRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    domain: str = "finance"
    compression: str = "moderate"
    model: str = None  # Add model selection
    show_stats: bool = False

class RouteResponse(BaseModel):
    session_id: str
    response: str
    model: Optional[str] = None  # Return which model was used
    metrics: Optional[dict] = None

# Default anchors (same as before)
DEFAULT_ANCHORS = {
    "[WAR]": {"code": "[WAR]", "expansion": "War/Geopolitical Risk Premium", 
              "definition": "Risk premium from geopolitical conflict, sanctions, military escalation"},
    "[LIQ]": {"code": "[LIQ]", "expansion": "Liquidity Conditions",
              "definition": "Availability of capital for trading, funding, and position unwinding"},
    "[CARRY]": {"code": "[CARRY]", "expansion": "Carry Trade Dynamics",
                "definition": "Borrow low-yield currency, invest in high-yield asset; sensitive to volatility"}
}

# Initialize default anchors
for code, anchor in DEFAULT_ANCHORS.items():
    if not anchor_store.get(code):
        anchor_store.create(code, anchor["expansion"], anchor["definition"], "finance")

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "3.2", "models": ["deepseek", "claude"]}

@app.post("/v3/sessions")
async def create_session():
    session_id = session_memory.create()
    return {"session_id": session_id}

@app.post("/v3/route", response_model=RouteResponse)
async def route_message(request: RouteRequest):
    # Get or create session
    if not request.session_id:
        session_id = session_memory.create()
    else:
        session_id = request.session_id
        if not session_memory.get(session_id):
            session_id = session_memory.create()
    
    # Load anchors
    anchors_dict = {}
    db_anchors = anchor_store.list_by_domain(request.domain)
    for a in db_anchors:
        anchors_dict[a["code"]] = a
    if not anchors_dict:
        anchors_dict = DEFAULT_ANCHORS
    
    # Detect codes
    detected_codes = [code for code in anchors_dict.keys() if code in request.message]
    
    # Compress
    compressed, compression_stats = compression_engine.compress(
        request.message, request.compression, anchors_dict
    )
    
    # Build system prompt
    system_prompt = f"""You are an AI assistant using SCP v3.2 (Semantic Compression Protocol).
Domain: {request.domain}
Active anchors: {', '.join(anchors_dict.keys())}

Guidelines:
- Use anchors like [CODE] when referencing concepts
- Provide concise, precise answers
- Maintain semantic accuracy
- If you detect drift, flag with [DRIFT-DETECTED]
"""
    
    # Call LLM via gateway
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
            response=f"Error: {str(e)}",
            model=None,
            metrics={"error": True}
        )
    
    # Drift check
    drift_results = {}
    for code in detected_codes:
        anchor = anchors_dict.get(code)
        if anchor:
            passed, sim = drift_firewall.check(assistant_response, anchor["definition"])
            drift_results[code] = {"passed": passed, "similarity": sim}
    
    drift_passed = all(r["passed"] for r in drift_results.values()) if drift_results else True
    
    # Calculate TRI
    tri = tri_calculator.calculate(request.message, assistant_response)
    
    # Save turn
    session_memory.add_turn(session_id, {
        "message": request.message[:200],
        "compressed": compressed[:200],
        "response": assistant_response[:200],
        "model": model_used,
        "tri": tri,
        "drift_passed": drift_passed
    })
    
    # Build metrics
    metrics = {
        "compression_savings": compression_stats.get("savings", 0),
        "tri": tri,
        "drift_passed": drift_passed,
        "model_used": model_used
    }
    
    if request.show_stats:
        metrics["drift_results"] = drift_results
        metrics["compression_mode"] = compression_stats.get("mode")
        metrics["detected_codes"] = detected_codes
        metrics["original_length"] = len(request.message.split())
        metrics["compressed_length"] = len(compressed.split())
    
    return RouteResponse(
        session_id=session_id,
        response=assistant_response,
        model=model_used,
        metrics=metrics if request.show_stats else None
    )

@app.get("/v3/anchors")
async def list_anchors(domain: str = None):
    if domain:
        anchors = anchor_store.list_by_domain(domain)
    else:
        anchors = anchor_store.list_by_domain("finance")
    return {"anchors": anchors}

@app.post("/v3/anchors")
async def create_anchor(
    code: str, 
    expansion: str, 
    definition: str, 
    domain: str,
    keywords: str = ""
):
    kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
    anchor = anchor_store.create(code, expansion, definition, domain, keywords=kw_list)
    return anchor

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)