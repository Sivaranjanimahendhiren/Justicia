"""
PART 10 — Sample Test Case
Input: "I paid full amount but builder delayed possession"
Run: python -m backend.test_sample
"""
import json
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.agent.controller import run_agent


def test_sample_case():
    query = "I paid full amount but builder delayed possession by 28 months in Maharashtra. I have sale agreement and payment receipts."

    print("\n" + "="*60)
    print("JUSTICIA — SAMPLE TEST CASE")
    print("="*60)
    print(f"Query: {query}\n")

    result = run_agent(query)

    print(f"Status: {result['status']}")
    print(f"Risk Score: {result.get('risk_score', 'N/A')}/100")
    print(f"Compliance: {result.get('compliance_flag', 'N/A')}")
    print(f"Case Readiness: {result.get('case_readiness', 'N/A')}")

    print("\n--- APPLICABLE LAWS ---")
    for law in result.get("applicable_laws", []):
        print(f"  [{law['section']}] {law['content'][:100]}...")

    print("\n--- DETECTED CONFLICTS ---")
    conflicts = result.get("detected_conflicts", [])
    if conflicts:
        for c in conflicts:
            print(f"  Field: {c['field']} | Severity: {c['severity']}")
    else:
        print("  None detected")

    print("\n--- MISSING EVIDENCE ---")
    missing = result.get("missing_evidence", [])
    if missing:
        for m in missing:
            print(f"  - {m['document_type']}")
    else:
        print("  None")

    print("\n--- JUDICIAL PRECEDENTS ---")
    for p in result.get("judicial_precedents", []):
        print(f"  #{p['rank']} {p['case_name']} (score: {p['relevance_score']})")

    print("\n--- LEGAL STRATEGY ---")
    strategy = result.get("legal_strategy")
    if strategy:
        print(f"  Compensation: {strategy.get('compensation_calculation', 'N/A')}")
        print(f"  Relief: {strategy.get('recommended_relief', 'N/A')}")
        print(f"  Risk: {strategy.get('risk_assessment', 'N/A')}")
        print("\n  Action Items:")
        for item in strategy.get("immediate_action_items", []):
            print(f"    - {item}")
        print(f"\n  Disclaimer: {strategy.get('disclaimer', '')}")

    print("\n" + "="*60)


if __name__ == "__main__":
    test_sample_case()
