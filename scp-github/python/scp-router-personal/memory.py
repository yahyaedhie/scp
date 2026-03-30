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
            "active_anchors": [],
            "strike_count": 0,
            "blacklisted": False
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

    def get_readiness_report(self, session_id: str) -> Dict:
        """Analyze session history to see if it's a candidate for optimization"""
        session = self.get(session_id)
        if not session or len(session.get("turns", [])) < 3:
            return {"ready": False, "reason": "Insufficient turns"}
            
        turns = session["turns"]
        
        # 1. Stability Check: Must have EXACTLY 3 consecutive turns in the same domain
        history_slice = turns[-3:]
        domains = [t.get("detected_domain") for t in history_slice if t.get("detected_domain")]
        
        if len(domains) < 3 or len(set(domains)) != 1:
            return {"ready": False, "reason": "Context instability (need 3 consistent turns)"}
        
        target_domain = domains[0]
        
        # 2. Quality Check: Is the average TRI high enough?
        avg_tri = sum(t.get("tri", 0) for t in history_slice) / 3
        if avg_tri < 0.85:
            return {"ready": False, "reason": f"Quality baseline not met (Avg TRI: {avg_tri:.2f})"}
            
        # 3. Extraction: Find potential new keywords
        corpus = [t.get("message", "") for t in turns]
        all_text = " ".join(corpus)
        
        # Filter for unique, meaningful words
        stop_words = {'what', 'that', 'with', 'this', 'from', 'your', 'have', 'been', 'were', 'explain', 'relationship'}
        words = [w.lower().strip("?,.!") for w in all_text.split() if len(w) > 5]
        unique_words = [w for w in set(words) if w not in stop_words]
        
        # Entropy Check: Must have at least 2 potential keywords to optimize
        if len(unique_words) < 2:
            return {"ready": False, "reason": "Insufficient semantic entropy for meaningful gain"}
            
        candidates = unique_words[:6]
        
        return {
            "ready": True,
            "domain": target_domain,
            "avg_tri": avg_tri,
            "suggested_keywords": candidates
        }

    def log_violation(self, session_id: str) -> Dict:
        """Handle protocol violations (3-strike rule)"""
        session = self.get(session_id)
        if not session: 
            return {"status": "error", "message": "Session not found"}
        
        session["strike_count"] = session.get("strike_count", 0) + 1
        
        if session["strike_count"] >= 3:
            session["blacklisted"] = True
            self.update(session_id, session)
            return {"status": "banned", "strikes": session["strike_count"]}
            
        self.update(session_id, session)
        return {"status": "warned", "strikes": session["strike_count"]}