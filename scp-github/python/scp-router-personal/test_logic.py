import sys
import os
import asyncio

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from similarity import SimilarityEngine
from tri import TRICalculator
from drift import DriftFirewall

def test_similarity():
    print("Testing SimilarityEngine...")
    engine = SimilarityEngine()
    
    # Test identical
    s1 = engine.compute_similarity("The quick brown fox", "The quick brown fox")
    print(f"Identical similarity: {s1:.4f}")
    assert s1 > 0.99
    
    # Test partial
    s2 = engine.compute_similarity("The quick brown fox", "A fast ginger fox")
    print(f"Partial similarity: {s2:.4f}")
    assert 0.1 < s2 < 0.9
    
    # Test unrelated
    s3 = engine.compute_similarity("The quick brown fox", "I like to eat apples")
    print(f"Unrelated similarity: {s3:.4f}")
    assert s3 < 0.2
    
    print("✅ SimilarityEngine passed.\n")

def test_tri():
    print("Testing TRICalculator...")
    calc = TRICalculator()
    
    # Perfect match
    t1 = calc.calculate("Increase liquidity by 25%", "Increase liquidity by 25%")
    print(f"Perfect TRI: {t1:.4f}")
    assert t1 > 0.95
    
    # Good match with different wording
    t2 = calc.calculate("The market is currently highly volatile and risky.", "High volatility and risk detected in the market.")
    print(f"Good TRI (different wording): {t2:.4f}")
    assert t2 > 0.6
    
    # Failed keywords/numbers
    t3 = calc.calculate("The BTC price is 50000", "The price of ETH is 2000")
    print(f"Poor TRI (mismatched numbers/keywords): {t3:.4f}")
    assert t3 < 0.5
    
    print("✅ TRICalculator passed.\n")

def test_drift():
    print("Testing DriftFirewall...")
    firewall = DriftFirewall(threshold=0.8)
    
    # Pass
    p1, s1 = firewall.check("Deep liquidity in the bond market", "Availability of trading capital")
    print(f"Drift check (Pass): {p1} ({s1:.4f})")
    
    # Fail
    p2, s2 = firewall.check("The weather is nice today", "Availability of trading capital")
    print(f"Drift check (Fail): {p2} ({s2:.4f})")
    assert not p2
    
    print("✅ DriftFirewall passed.\n")

if __name__ == "__main__":
    test_similarity()
    test_tri()
    test_drift()
    print("--- ALL LOGIC TESTS PASSED ---")
