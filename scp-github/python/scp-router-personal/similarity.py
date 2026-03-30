from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from typing import List, Optional

class SimilarityEngine:
    def __init__(self, max_features: int = 1000):
        # We use a broad range of n-grams (1-2) for better semantic capture
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self._fitted = False
        
        # Pre-seed with some common domain terms to ensure stable dimensions
        self._seed_vocabulary = [
            "finance market liquidity risk premium asset capital funding",
            "governance policy regulation compliance law authority mandate",
            "education learning knowledge study research academic school",
            "cosmology universe galaxy space physics quantum entropy"
        ]

    def _ensure_fitted(self, texts: List[str]):
        """Ensure the vectorizer is fitted, using seed vocabulary if necessary"""
        if not self._fitted:
            # Combine provided texts with seed vocabulary for a more robust base
            fit_corpus = self._seed_vocabulary + list(texts)
            self.vectorizer.fit(fit_corpus)
            self._fitted = True

    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity between two texts"""
        if not text1 or not text2:
            return 0.0
        
        if not text1.strip() or not text2.strip():
            return 0.0

        # Transform texts
        self._ensure_fitted([text1, text2])
        vectors = self.vectorizer.transform([text1, text2])
        
        vec1 = vectors[0].toarray()[0]
        vec2 = vectors[1].toarray()[0]
        
        # Manual cosine similarity Calculation
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return float(dot_product / (norm1 * norm2))

    def batch_similarity(self, target: str, candidates: List[str]) -> List[float]:
        """Compute similarity of one target text against a list of candidates"""
        if not target or not candidates:
            return [0.0] * len(candidates)

        self._ensure_fitted([target] + candidates)
        vectors = self.vectorizer.transform([target] + candidates)
        
        target_vec = vectors[0].toarray()[0]
        similarities = []
        
        target_norm = np.linalg.norm(target_vec)
        if target_norm == 0:
            return [0.0] * len(candidates)

        for i in range(1, len(candidates) + 1):
            cand_vec = vectors[i].toarray()[0]
            cand_norm = np.linalg.norm(cand_vec)
            
            if cand_norm == 0:
                similarities.append(0.0)
                continue
                
            sim = np.dot(target_vec, cand_vec) / (target_norm * cand_norm)
            similarities.append(float(sim))
            
        return similarities

class DomainClassifier:
    def __init__(self, engine: Optional[SimilarityEngine] = None):
        self.engine = engine or SimilarityEngine()
        self.domains = {
            "finance": "finance market liquidity risk premium asset capital funding trading economy debt interest bank investment stock portfolio",
            "governance": "governance policy regulation compliance law authority mandate ethics legal contract audit regulatory oversight sovereign treaty jurisdiction",
            "education": "education learning knowledge study research academic school teacher student curriculum mentor university teaching literacy pedagogy instruction",
            "cosmology": "cosmology universe galaxy space physics quantum entropy star blackhole telescope astrophysics astronomy relativity spacetime matter expansion cosmic"
        }

    def predict(self, text: str) -> str:
        """Predict the most likely domain for the given text"""
        if not text or not text.strip():
            return "finance" # Default to finance if empty
            
        categories = list(self.domains.keys())
        seeds = list(self.domains.values())
        
        # Get similarities across all domain seeds
        scores = self.engine.batch_similarity(text, seeds)
        
        # Find index of max score
        max_idx = np.argmax(scores)
        max_score = scores[max_idx]
        
        # Low confidence threshold
        if max_score < 0.01:
            return "finance"
            
        return categories[max_idx]
