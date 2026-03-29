import re
from typing import Dict, List, Tuple, Set

class CompressionEngine:
    def __init__(self):
        self.filler_words = {
            'um', 'uh', 'like', 'you know', 'i mean', 'so', 'actually', 
            'basically', 'literally', 'just', 'well', 'sort of', 'kind of'
        }
        
        self.direction_patterns = [
            (r'\b(increases?|rises?|climbs?|goes up)\b', '↑'),
            (r'\b(decreases?|falls?|drops?|goes down|contracts?)\b', '↓'),
            (r'\b(causes?|leads to|results in|triggers?)\b', '→'),
            (r'\b(affects?|impacts?)\b', '→')
        ]
    
    def compress(self, text: str, mode: str = "moderate", anchors: Dict = None) -> Tuple[str, Dict]:
        """Compress text using specified mode"""
        if mode == "light":
            return self._light_compress(text)
        elif mode == "deep":
            return self._deep_compress(text, anchors)
        else:  # moderate
            return self._moderate_compress(text, anchors)
    
    def _light_compress(self, text: str) -> Tuple[str, Dict]:
        """Remove filler words only"""
        original_len = len(text.split())
        compressed = text.lower()
        
        for filler in self.filler_words:
            compressed = re.sub(rf'\b{re.escape(filler)}\b', '', compressed, flags=re.IGNORECASE)
        
        compressed = re.sub(r'\s+', ' ', compressed).strip()
        compressed_len = len(compressed.split())
        savings = (original_len - compressed_len) / original_len if original_len > 0 else 0
        
        return compressed, {"mode": "light", "savings": savings}
    
    def _moderate_compress(self, text: str, anchors: Dict) -> Tuple[str, Dict]:
        """Replace concepts with anchors"""
        if not anchors:
            return self._light_compress(text)
        
        original_len = len(text.split())
        compressed = text
        replacements = []
        
        # Sort by length to avoid partial replacements
        for code, anchor in sorted(anchors.items(), key=lambda x: -len(x[1].get("expansion", ""))):
            expansion = anchor.get("expansion", "")
            if expansion and expansion.lower() in compressed.lower():
                compressed = re.sub(
                    rf'\b{re.escape(expansion)}\b',
                    code,
                    compressed,
                    flags=re.IGNORECASE
                )
                replacements.append({"original": expansion, "replacement": code})
        
        compressed_len = len(compressed.split())
        savings = (original_len - compressed_len) / original_len if original_len > 0 else 0
        
        return compressed, {"mode": "moderate", "savings": savings, "replacements": replacements}
    
    def _deep_compress(self, text: str, anchors: Dict) -> Tuple[str, Dict]:
        """Symbolic encoding with direction mapping"""
        # First apply moderate compression
        compressed, stats = self._moderate_compress(text, anchors)
        
        # Apply direction symbols
        for pattern, symbol in self.direction_patterns:
            compressed = re.sub(pattern, symbol, compressed, flags=re.IGNORECASE)
        
        # Remove common stop words for deep compression
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with'}
        words = compressed.split()
        compressed = ' '.join([w for w in words if w.lower() not in stop_words])
        
        compressed_len = len(compressed.split())
        original_len = len(text.split())
        savings = (original_len - compressed_len) / original_len if original_len > 0 else 0
        stats["savings"] = savings
        stats["mode"] = "deep"
        
        return compressed, stats
    
    def expand(self, compressed: str, anchors: Dict) -> str:
        """Expand compressed text back to natural language"""
        expanded = compressed
        
        # Expand direction symbols
        expanded = expanded.replace('↑', ' increases')
        expanded = expanded.replace('↓', ' decreases')
        expanded = expanded.replace('→', ' affects')
        
        # Expand anchors
        for code, anchor in anchors.items():
            if code in expanded:
                expanded = expanded.replace(code, anchor.get("expansion", code))
        
        return expanded