import re
from typing import Dict, List, Set
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class TRICalculator:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        self._fitted = False
    
    def _get_vectors(self, texts: List[str]):
        if not self._fitted:
            self.vectorizer.fit(texts)
            self._fitted = True
        return self.vectorizer.transform(texts)
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords (simple approach)"""
        # Remove punctuation
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        # Split and filter
        words = set(text.split())
        # Remove common stopwords (simplified)
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        return words - stopwords
    
    def _extract_numbers(self, text: str) -> List[float]:
        """Extract numbers from text"""
        pattern = r'\b\d+(?:\.\d+)?%?\b'
        numbers = re.findall(pattern, text)
        return [float(n.replace('%', '')) for n in numbers]
    
    def calculate(self, original: str, compressed: str) -> float:
        """Calculate TRI score (0-1)"""
        if not original or not compressed:
            return 0.0
        
        # Component 1: Semantic similarity (TF-IDF)
        vectors = self._get_vectors([original, compressed])
        vec1, vec2 = vectors[0], vectors[1]
        dot = vec1.dot(vec2.T).toarray()[0][0]
        norm1 = np.linalg.norm(vec1.toarray())
        norm2 = np.linalg.norm(vec2.toarray())
        semantic = dot / (norm1 * norm2) if norm1 * norm2 > 0 else 0
        
        # Component 2: Keyword preservation
        orig_keywords = self._extract_keywords(original)
        comp_keywords = self._extract_keywords(compressed)
        if orig_keywords:
            preserved = len(orig_keywords & comp_keywords)
            keyword_score = preserved / len(orig_keywords)
        else:
            keyword_score = 1.0
        
        # Component 3: Number preservation
        orig_numbers = self._extract_numbers(original)
        comp_numbers = self._extract_numbers(compressed)
        if orig_numbers:
            # Simple: if any number matches
            matches = sum(1 for n in orig_numbers if any(abs(n - cn) < 0.01 for cn in comp_numbers))
            number_score = matches / len(orig_numbers)
        else:
            number_score = 1.0
        
        # Weighted average
        TRI = (semantic * 0.5) + (keyword_score * 0.3) + (number_score * 0.2)
        return round(min(1.0, TRI), 3)