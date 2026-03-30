from typing import Tuple, Dict, List, Optional
from similarity import SimilarityEngine

class DriftFirewall:
    def __init__(self, threshold: float = 0.70, similarity_engine: Optional[SimilarityEngine] = None):
        self.threshold = threshold
        self.similarity_engine = similarity_engine or SimilarityEngine()
    
    def check(self, response: str, anchor_definition: str, custom_threshold: Optional[float] = None) -> Tuple[bool, float]:
        """Check if response drifts from anchor definition"""
        threshold = custom_threshold if custom_threshold is not None else self.threshold
        
        if not response or not anchor_definition:
            return True, 1.0  # Cannot check, assume passed
            
        similarity = self.similarity_engine.compute_similarity(response, anchor_definition)
        passed = similarity >= threshold
        return passed, similarity
    
    def batch_check(self, response: str, anchors: List[Dict], domain_thresholds: Optional[Dict] = None) -> Dict:
        """Check response against multiple anchors with optional domain-specific thresholds"""
        results = {}
        for anchor in anchors:
            # Determine threshold: domain-specific or default
            threshold = self.threshold
            if domain_thresholds and anchor.get("domain") in domain_thresholds:
                threshold = domain_thresholds[anchor["domain"]].get("drift", self.threshold)
            
            passed, sim = self.check(response, anchor["definition"], custom_threshold=threshold)
            results[anchor["code"]] = {
                "passed": passed,
                "similarity": round(sim, 3),
                "anchor": anchor["expansion"],
                "threshold_used": threshold
            }
        return results