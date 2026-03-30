import re
from typing import Dict, List, Set, Optional
from similarity import SimilarityEngine

class TRICalculator:
    def __init__(self, similarity_engine: Optional[SimilarityEngine] = None):
        self.similarity_engine = similarity_engine or SimilarityEngine()
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords (simple approach)"""
        # Remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        # Split and filter
        words = set(text.split())
        # Remove common stopwords (consistent set)
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        return {w for w in words if w not in stopwords and len(w) > 2}
    
    def _extract_numbers(self, text: str) -> List[float]:
        """Extract numbers from text"""
        pattern = r'\b\d+(?:\.\d+)?%?\b'
        numbers = re.findall(pattern, text)
        return [float(n.replace('%', '')) for n in numbers]
    
    def calculate(self, original: str, response: str) -> float:
        """Calculate TRI score (0-1) between input and response"""
        if not original or not response:
            return 0.0
        
        # Component 1: Semantic similarity (via shared engine)
        semantic = self.similarity_engine.compute_similarity(original, response)
        
        # Component 2: Keyword preservation
        orig_keywords = self._extract_keywords(original)
        resp_keywords = self._extract_keywords(response)
        
        if orig_keywords:
            # We want to see how many of the original keywords are mentioned in the response
            # (Semantic overlap)
            preserved = len(orig_keywords & resp_keywords)
            keyword_score = preserved / len(orig_keywords)
        else:
            keyword_score = 1.0
        
        # Component 3: Number preservation
        orig_numbers = self._extract_numbers(original)
        resp_numbers = self._extract_numbers(response)
        
        if orig_numbers:
            # Simple threshold: if any number in the response matches an original number approx
            matches = sum(1 for n in orig_numbers if any(abs(n - rn) < 0.01 for rn in resp_numbers))
            number_score = matches / len(orig_numbers)
        else:
            number_score = 1.0
        
        # Weighted average (Weighted toward semantic accuracy)
        TRI = (semantic * 0.5) + (keyword_score * 0.3) + (number_score * 0.2)
        return round(min(1.0, TRI), 3)