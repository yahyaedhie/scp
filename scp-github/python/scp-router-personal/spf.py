import hashlib
import json
from datetime import datetime
from typing import Dict, List

class SPFGenerator:
    VERSION = "3.2"
    
    def generate(self, anchor: Dict) -> Dict:
        """Generate SPF packet from anchor"""
        return {
            "code": anchor["code"],
            "expansion": anchor["expansion"],
            "definition": anchor["definition"],
            "domain": anchor["domain"],
            "anchor_id": f"{anchor['code']}-ANCHOR",
            "hash": anchor["hash"],
            "version": self.VERSION,
            "constraints": anchor.get("constraints", []),
            "keywords": anchor.get("keywords", []),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def export_bundle(self, session_id: str, anchors: List[Dict], 
                      turns: int, savings: float) -> Dict:
        """Export complete session bundle"""
        return {
            "handoff_bundle": {
                "session_id": session_id,
                "export_time": datetime.utcnow().isoformat(),
                "version": self.VERSION,
                "anchors": [self.generate(a) for a in anchors],
                "metrics": {
                    "turns": turns,
                    "token_savings": savings
                }
            }
        }