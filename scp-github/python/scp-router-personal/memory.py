import json
import uuid
from typing import Dict, Optional
from datetime import datetime

class SessionMemory:
    def __init__(self, redis_url: str = None):
        self.redis_url = redis_url
        self.use_redis = False  # Simplified: use dict for personal use
        
        if redis_url:
            try:
                import redis
                self.redis = redis.from_url(redis_url)
                self.use_redis = True
            except:
                pass
        
        if not self.use_redis:
            self._dict_memory = {}
    
    def _get_key(self, session_id: str) -> str:
        return f"session:{session_id}"
    
    def create(self, entity_id: str = "user") -> str:
        session_id = str(uuid.uuid4())[:8]
        data = {
            "session_id": session_id,
            "entity_id": entity_id,
            "created_at": datetime.utcnow().isoformat(),
            "turns": [],
            "active_anchors": []
        }
        
        if self.use_redis:
            self.redis.setex(self._get_key(session_id), 3600, json.dumps(data))
        else:
            self._dict_memory[session_id] = data
        
        return session_id
    
    def get(self, session_id: str) -> Optional[Dict]:
        if self.use_redis:
            data = self.redis.get(self._get_key(session_id))
            return json.loads(data) if data else None
        else:
            return self._dict_memory.get(session_id)
    
    def update(self, session_id: str, data: Dict):
        if self.use_redis:
            self.redis.setex(self._get_key(session_id), 3600, json.dumps(data))
        else:
            self._dict_memory[session_id] = data
    
    def add_turn(self, session_id: str, turn_data: Dict):
        session = self.get(session_id)
        if session:
            turns = session.get("turns", [])
            turns.append(turn_data)
            # Keep only last 50 turns
            if len(turns) > 50:
                turns = turns[-50:]
            session["turns"] = turns
            self.update(session_id, session)