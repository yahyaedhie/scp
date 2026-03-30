import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory import SessionMemory

def test_optimization_readiness():
    print("Testing Semantic Timing & Optimization readiness...")
    memory = SessionMemory()
    session_id = str(uuid_uuid()) if 'uuid_uuid' in globals() else "test-session"
    
    # helper to mock turns
    def add_mock_turn(id, domain, tri):
        memory.add_turn(id, {
            "message": "This is a long enough message to extract keywords from.",
            "detected_domain": domain,
            "tri": tri
        })

    # Test Case 1: Insufficient turns
    print("\nCase 1: Insufficient turns (2 turns)")
    sid1 = memory.create()
    add_mock_turn(sid1, "finance", 0.9)
    add_mock_turn(sid1, "finance", 0.9)
    report = memory.get_readiness_report(sid1)
    print(f"Result: {report['ready']}, Reason: {report.get('reason')}")
    assert report['ready'] == False

    # Test Case 2: Consistent High Quality (3 turns)
    print("\nCase 2: Consistent High Quality (3 turns, same domain, TRI > 0.85)")
    sid2 = memory.create()
    for _ in range(3): add_mock_turn(sid2, "cosmology", 0.95)
    report = memory.get_readiness_report(sid2)
    print(f"Result: {report['ready']}, Suggested Keywords: {report.get('suggested_keywords')}")
    assert report['ready'] == True
    assert "cosmology" == report['domain']

    # Test Case 3: Inconsistent Domains
    print("\nCase 3: Inconsistent Domains (Switching mid-session)")
    sid3 = memory.create()
    add_mock_turn(sid3, "finance", 0.9)
    add_mock_turn(sid3, "cosmology", 0.9)
    add_mock_turn(sid3, "finance", 0.9)
    report = memory.get_readiness_report(sid3)
    print(f"Result: {report['ready']}, Reason: {report.get('reason')}")
    assert report['ready'] == False

    # Test Case 4: Low Quality
    print("\nCase 4: Low Quality (TRI < 0.85)")
    sid4 = memory.create()
    for _ in range(3): add_mock_turn(sid4, "finance", 0.70)
    report = memory.get_readiness_report(sid4)
    print(f"Result: {report['ready']}, Reason: {report.get('reason')}")
    assert report['ready'] == False

    print("\n--- ALL OPTIMIZATION LOGIC TESTS PASSED ---")

if __name__ == "__main__":
    test_optimization_readiness()
