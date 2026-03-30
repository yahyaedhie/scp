import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from similarity import SimilarityEngine, DomainClassifier

def test_classification():
    print("Testing AI Domain Classification Engine...")
    classifier = DomainClassifier()
    
    test_cases = [
        ("What is the current market liquidity for treasury bonds?", "finance"),
        ("How do I ensure compliance with the new GDPR regulations?", "governance"),
        ("Explain the curriculum for the advanced machine learning course.", "education"),
        ("What is the relationship between dark matter and galactic expansion?", "cosmology"),
        ("The asset capital funding is secured.", "finance"),
        ("Ethics and legal protocols are mandatory for this project.", "governance"),
        ("I need a research mentor for my academic studies.", "education"),
        ("Quantum entropy in a black hole is fascinating.", "cosmology")
    ]
    
    passed = 0
    for text, expected in test_cases:
        predicted = classifier.predict(text)
        
        # Debugging: show scores for failed cases
        if predicted != expected:
            scores = classifier.engine.batch_similarity(text, list(classifier.domains.values()))
            print(f"DEBUG Scores: {dict(zip(classifier.domains.keys(), [round(s, 4) for s in scores]))}")
            
        status = "✅" if predicted == expected else "❌"
        print(f"[{status}] Input: \"{text[:40]}...\"")
        print(f"      Expected: {expected}, Predicted: {predicted}")
        if predicted == expected:
            passed += 1
            
    print(f"\nFinal Result: {passed}/{len(test_cases)} cases passed.")
    if passed == len(test_cases):
        print("--- ALL CLASSIFICATION TESTS PASSED ---")
    else:
        print("--- SOME TESTS FAILED ---")
        sys.exit(1)

if __name__ == "__main__":
    test_classification()
