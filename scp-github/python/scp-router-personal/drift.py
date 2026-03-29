from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from typing import Tuple, Dict, List
import re

class DriftFirewall:
    def __init__(self, threshold: float = 0.70):
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(
            max_features=500,  # Limit features for speed
            stop_words='english',
            ngram_range=(1, 2)  # Unigrams and bigrams
        )
        self._fitted = False
    
    def _get_tfidf_vectors(self, texts: List[str]):
        """Get TF-IDF vectors for texts"""
        if not self._fitted:
            self.vectorizer.fit(texts)
            self._fitted = True
        
        return self.vectorizer.transform(texts)
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity using TF-IDF"""
        if not text1 or not text2:
            return 0.0
        
        # Handle empty strings
        if len(text1.strip()) == 0 or len(text2.strip()) == 0:
            return 0.0
        
        # Get vectors
        vectors = self._get_tfidf_vectors([text1, text2])
        vec1, vec2 = vectors[0], vectors[1]
        
        # Compute cosine similarity
        dot_product = vec1.dot(vec2.T).toarray()[0][0]
        norm1 = np.linalg.norm(vec1.toarray())
        norm2 = np.linalg.norm(vec2.toarray())
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def check(self, response: str, anchor_definition: str) -> Tuple[bool, float]:
        """Check if response drifts from anchor definition"""
        similarity = self.compute_similarity(response, anchor_definition)
        passed = similarity >= self.threshold
        return passed, similarity
    
    def batch_check(self, response: str, anchors: List[Dict]) -> Dict:
        """Check response against multiple anchors"""
        results = {}
        for anchor in anchors:
            passed, sim = self.check(response, anchor["definition"])
            results[anchor["code"]] = {
                "passed": passed,
                "similarity": sim,
                "anchor": anchor["expansion"]
            }
        return results