"""
SCP Self-Monitoring Drift Firewall
Real-time validation of output against anchor definitions
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class DriftAlert:
    code: str
    event_type: str  # definition_contradiction | constraint_violation | domain_mismatch
    severity: str    # warning | error
    detail: str
    anchor_definition: str
    statement_made: str
    timestamp: str
    auto_corrected: bool

class SelfMonitoringDriftFirewall:
    def __init__(self):
        self.anchors = {}
        self.active_codes = []
        self.response_buffer = ""
        self.alerts = []
    
    def register_anchor(self, code: str, definition: str, constraints: List[str], domain: str):
        """Register an anchor in the firewall."""
        self.anchors[code] = {
            "definition": definition,
            "constraints": constraints,
            "domain": domain,
            "registered_at": datetime.utcnow().isoformat()
        }
    
    def extract_codes(self, text: str) -> List[str]:
        """Extract all [CODE] references from text."""
        return re.findall(r'\[([A-Z\-]+)\]', text)
    
    def validate_statement(self, statement: str) -> Tuple[bool, List[DriftAlert]]:
        """
        Validate a statement BEFORE it's output.
        Returns: (is_clean, alerts)
        """
        alerts = []
        codes = self.extract_codes(statement)
        
        for code in codes:
            if code not in self.anchors:
                alerts.append(DriftAlert(
                    code=f"[{code}]",
                    event_type="unknown_code",
                    severity="warning",
                    detail=f"Code [{code}] not registered in firewall",
                    anchor_definition="N/A",
                    statement_made=statement[:100],
                    timestamp=datetime.utcnow().isoformat(),
                    auto_corrected=False
                ))
                continue
            
            anchor = self.anchors[code]
            definition = anchor["definition"]
            constraints = anchor["constraints"]
            
            # Check 1: Definition contradiction
            if self._contradicts_definition(statement, code, definition):
                alerts.append(DriftAlert(
                    code=f"[{code}]",
                    event_type="definition_contradiction",
                    severity="error",
                    detail=f"Statement contradicts anchor definition. Definition says: '{definition}'",
                    anchor_definition=definition,
                    statement_made=statement,
                    timestamp=datetime.utcnow().isoformat(),
                    auto_corrected=False
                ))
            
            # Check 2: Constraint violation
            if constraints and not self._satisfies_constraints(statement, constraints):
                alerts.append(DriftAlert(
                    code=f"[{code}]",
                    event_type="constraint_violation",
                    severity="warning",
                    detail=f"Statement may violate constraints: {constraints}",
                    anchor_definition=definition,
                    statement_made=statement[:100],
                    timestamp=datetime.utcnow().isoformat(),
                    auto_corrected=False
                ))
        
        is_clean = len([a for a in alerts if a.severity == "error"]) == 0
        return is_clean, alerts
    
    def _contradicts_definition(self, statement: str, code: str, definition: str) -> bool:
        """Check if statement contradicts the anchor definition."""
        anchor = self.anchors[code]
        
        # Extract key concepts from definition (e.g., "prevents drift", "compresses tokens")
        definition_lower = definition.lower()
        statement_lower = statement.lower()
        
        # Key contradiction patterns
        if "prevent" in definition_lower or "prevent" in definition_lower:
            if "increase" in statement_lower and code in statement_lower:
                return True
            if "ignore" in statement_lower and code in statement_lower:
                return True
        
        if "compress" in definition_lower:
            if "maximize" in statement_lower and "token" in statement_lower:
                return True
            if "expand" in statement_lower and code in statement_lower:
                return True
        
        if "stable" in definition_lower or "stability" in definition_lower:
            if "drift" in statement_lower and "increase" in statement_lower:
                return True
        
        return False
    
    def _satisfies_constraints(self, statement: str, constraints: List[str]) -> bool:
        """Check if statement satisfies the anchor constraints."""
        statement_lower = statement.lower()
        
        # If code is mentioned, at least one constraint keyword should be present
        matching_constraints = sum(1 for c in constraints if c.lower() in statement_lower)
        return matching_constraints > 0 or len(constraints) == 0
    
    def generate_alert_report(self, alerts: List[DriftAlert]) -> str:
        """Generate a human-readable alert report."""
        if not alerts:
            return "[DRIFT-FIREWALL] ✅ All checks passed. No drift detected."
        
        report = "[DRIFT-FIREWALL] ⚠️ ALERTS DETECTED:\n"
        report += "=" * 60 + "\n"
        
        errors = [a for a in alerts if a.severity == "error"]
        warnings = [a for a in alerts if a.severity == "warning"]
        
        if errors:
            report += f"\n🔴 ERRORS ({len(errors)}):\n"
            for alert in errors:
                report += f"\n  Code: {alert.code}\n"
                report += f"  Type: {alert.event_type}\n"
                report += f"  Anchor: {alert.anchor_definition}\n"
                report += f"  Issue: {alert.detail}\n"
        
        if warnings:
            report += f"\n🟡 WARNINGS ({len(warnings)}):\n"
            for alert in warnings:
                report += f"\n  Code: {alert.code}\n"
                report += f"  Issue: {alert.detail}\n"
        
        return report
    
    def process_response(self, response: str) -> Tuple[str, str, bool]:
        """
        Process a response through the drift firewall.
        Returns: (response, alert_report, is_clean)
        """
        is_clean, alerts = self.validate_statement(response)
        report = self.generate_alert_report(alerts)
        
        return response, report, is_clean


# Example usage and test
if __name__ == "__main__":
    firewall = SelfMonitoringDriftFirewall()
    
    # Register anchors
    firewall.register_anchor(
        code="SCP",
        definition="Semantic Compression Protocol — meaning-stable AI communication layer that prevents drift and compresses tokens",
        constraints=["prevent drift", "compress tokens", "anchor definitions"],
        domain="ai-protocol"
    )
    
    firewall.register_anchor(
        code="COPILOT-CTX",
        definition="200K token budget for managing conversation context with SCP compression",
        constraints=["200K tokens", "efficiency"],
        domain="copilot"
    )
    
    # Test Case 1: Clean statement
    print("TEST 1: Clean statement")
    print("-" * 60)
    clean_response = "SCP prevents drift by using anchors and compressing tokens efficiently."
    response, report, is_clean = firewall.process_response(clean_response)
    print(f"Response: {response}")
    print(f"Report:\n{report}")
    print(f"Is Clean: {is_clean}\n")
    
    # Test Case 2: Drift statement (contradiction)
    print("\nTEST 2: Drift statement (CONTRADICTION)")
    print("-" * 60)
    drift_response = "Actually, [SCP] is really about maximizing token usage by making conversations longer and increasing meaning drift."
    response, report, is_clean = firewall.process_response(drift_response)
    print(f"Response: {response}")
    print(f"Report:\n{report}")
    print(f"Is Clean: {is_clean}\n")
    
    # Test Case 3: Constraint violation
    print("\nTEST 3: Constraint violation warning")
    print("-" * 60)
    constraint_response = "[SCP] is cool but doesn't really matter much."
    response, report, is_clean = firewall.process_response(constraint_response)
    print(f"Response: {response}")
    print(f"Report:\n{report}")
    print(f"Is Clean: {is_clean}\n")