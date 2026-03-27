import asyncio
from app.config import settings
from app.models.session import ProxyRequest
from app.core.drift import DriftEvent
import app.routes.proxy as proxy_route
from unittest.mock import AsyncMock, MagicMock

async def verify():
    print("--- Verifying Domain Thresholds ---")
    
    # Override settings
    settings.domain_config["governance"] = {"tri": 0.95, "cqs": 0.85}
    settings.domain_config["finance"] = {"tri": 0.85, "cqs": 0.80}
    
    # Mock dependencies
    proxy_route.extract_codes = AsyncMock(side_effect=lambda x: ["WAR"])
    proxy_route.build_system_prompt = AsyncMock(return_value="prompt")
    
    async def mock_val_side_effect(text, domain):
        # Return a NEW list on each call
        return "drift-warning", [
            DriftEvent("W", "drift", "d1", "warning"),
            DriftEvent("W", "drift", "d2", "warning")
        ]
    proxy_route.validate_response = AsyncMock(side_effect=mock_val_side_effect)
    
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(type="text", text="Resp")]
    mock_client = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_msg)
    proxy_route._get_client = lambda: mock_client
    
    # Mock session store
    proxy_route.get_or_create_session = AsyncMock(return_value=MagicMock(session_id="s", turn_count=0, active_codes=[], drift_events=[]))
    proxy_route.update_session = AsyncMock()

    # 1. Test Governance (Threshold 0.95, TRI 0.90) -> Warning expected
    req1 = ProxyRequest(message="Test", domain="governance")
    resp1 = await proxy_route.proxy_chat(req1)
    print(f"Governance TRI: {resp1.tri} (Threshold: 0.95)")
    events1 = [e["event_type"] for e in resp1.drift_events]
    print(f"Events: {events1}")
    assert "low_tri" in events1
    
    # 2. Test Finance (Threshold 0.85, TRI 0.90) -> NO warning expected
    req2 = ProxyRequest(message="Test", domain="finance")
    resp2 = await proxy_route.proxy_chat(req2)
    print(f"Finance TRI: {resp2.tri} (Threshold: 0.85)")
    events2 = [e["event_type"] for e in resp2.drift_events]
    print(f"Events: {events2}")
    assert "low_tri" not in events2
    
    print("--- VERIFICATION SUCCESSFUL ---")

if __name__ == "__main__":
    asyncio.run(verify())
