"""
Agent Planner — determines which tools to invoke based on query analysis.
"""
from typing import List


TOOL_PLAN_FULL = [
    "juris_sync",
    "gap_detector",
    "fact_conflict",
    "precedent_ranker",
    "strategy_gen",
    "ethical_guard"
]


def plan_tools(query: str, context: dict) -> List[str]:
    """
    Determine tool execution plan based on query and available context.
    Returns ordered list of tool names to execute.
    """
    query_lower = query.lower()
    plan = []

    # Always fetch statutes for legal queries
    plan.append("juris_sync")

    # Check documents if client mentions having docs
    doc_keywords = ["receipt", "agreement", "letter", "document", "allotment", "bank"]
    if any(k in query_lower for k in doc_keywords) or context.get("provided_documents"):
        plan.append("gap_detector")

    # Detect conflicts if statement details are present
    if context.get("claimed_payment_date") or context.get("claimed_amount"):
        plan.append("fact_conflict")

    # Always rank precedents for strategy
    plan.append("precedent_ranker")

    # Always generate strategy
    plan.append("strategy_gen")

    # Always validate with ethical guard
    plan.append("ethical_guard")

    return plan
