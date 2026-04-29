"""
Agent Controller — orchestrates Plan → Execute → Verify → Replan loop.
Supports all 10 legal categories from the Justicia dataset.
"""
import json
from typing import Dict, Any
from .domain_guard import is_legal_query, detect_category, OUT_OF_SCOPE_RESPONSE
from .planner import plan_tools
from .executor import execute_plan, MAX_REPLAN_ATTEMPTS
from rag.vector_store import retrieve

# ── Category-specific context builders ───────────────────────────────────────

CATEGORY_TOPICS = {
    "Family Law": "family law divorce maintenance custody marriage",
    "Dowry & Domestic Violence": "dowry domestic violence 498A DV Act protection order",
    "Consumer Complaints": "consumer complaint deficiency service refund Consumer Protection Act",
    "Financial Disputes": "financial dispute cheque bounce loan recovery NI Act",
    "Property & RERA Issues": "delayed possession RERA Section 18 property dispute",
    "Employment Disputes": "employment dispute wrongful termination gratuity labour law",
    "Cyber Complaints": "cyber crime online fraud IT Act cybercrime",
    "General Criminal Issues": "FIR criminal complaint IPC CrPC bail police",
    "Small Civil Disputes": "civil dispute recovery compensation consumer court",
    "General Legal Advice": "legal advice rights procedure Indian law",
}

CATEGORY_KEY_FACTORS = {
    "Family Law": ["marriage", "maintenance", "custody", "divorce", "family court"],
    "Dowry & Domestic Violence": ["dowry", "domestic violence", "498A", "DV Act", "protection order"],
    "Consumer Complaints": ["consumer", "deficiency", "refund", "Consumer Protection Act", "District Commission"],
    "Financial Disputes": ["cheque bounce", "loan", "NI Act", "recovery", "bank"],
    "Property & RERA Issues": ["delayed possession", "RERA", "property", "builder", "Section 18"],
    "Employment Disputes": ["employment", "termination", "labour law", "gratuity", "wages"],
    "Cyber Complaints": ["cyber crime", "IT Act", "online fraud", "FIR", "cybercrime portal"],
    "General Criminal Issues": ["FIR", "IPC", "CrPC", "bail", "criminal complaint"],
    "Small Civil Disputes": ["civil dispute", "compensation", "recovery", "legal notice", "court"],
    "General Legal Advice": ["legal rights", "procedure", "Indian law", "advice", "how to"],
}

CATEGORY_OUTCOMES = {
    "Family Law": "fair resolution including maintenance, custody, or divorce as applicable",
    "Dowry & Domestic Violence": "protection, compensation, and criminal action against perpetrators",
    "Consumer Complaints": "full refund, replacement, or compensation for deficiency in service",
    "Financial Disputes": "recovery of money owed with interest and legal action against defaulter",
    "Property & RERA Issues": "possession or full refund with interest and compensation",
    "Employment Disputes": "reinstatement or compensation and enforcement of employment rights",
    "Cyber Complaints": "FIR registration, recovery of money, and action against perpetrators",
    "General Criminal Issues": "FIR registration, bail, and justice through criminal proceedings",
    "Small Civil Disputes": "compensation and recovery through consumer forum or civil court",
    "General Legal Advice": "clear understanding of legal rights and recommended next steps",
}


def build_context_from_query(query: str) -> Dict[str, Any]:
    """Build structured context from query using RAG + category detection."""
    category = detect_category(query)
    topic = CATEGORY_TOPICS.get(category, query)

    # RAG retrieval — search both the dataset and knowledge files
    hits = retrieve(query, top_k=5)
    rag_context = "\n".join([h["content"] for h in hits])

    query_lower = query.lower()

    # Jurisdiction detection
    jurisdiction = "India"
    for state in ["maharashtra", "karnataka", "delhi", "gujarat", "tamil nadu",
                  "kerala", "rajasthan", "uttar pradesh", "west bengal", "pune",
                  "mumbai", "bangalore", "chennai", "hyderabad", "kolkata"]:
        if state in query_lower:
            jurisdiction = state.title()
            break

    context = {
        "raw_query": query,
        "rag_context": rag_context,
        "category": category,
        "topic": topic,
        "jurisdiction": jurisdiction,
        "case_summary": query,
        "key_factors": CATEGORY_KEY_FACTORS.get(category, ["legal dispute", "India"]),
        "provided_documents": [],
        "client_desired_outcome": CATEGORY_OUTCOMES.get(category, "justice and legal remedy"),
    }

    # ── Document extraction ───────────────────────────────────────────────────
    doc_map = {
        "sale agreement": "Sale Agreement",
        "allotment letter": "Allotment Letter",
        "receipt": "Payment Receipts",
        "bank statement": "Bank Statements",
        "email": "Communication Logs",
        "pan": "Identity Proof",
        "aadhaar": "Identity Proof",
        "rera certificate": "RERA Registration Certificate",
        "salary slip": "Salary Slips",
        "appointment letter": "Appointment Letter",
        "cheque": "Cheque Copy",
        "medical record": "Medical Records",
        "fir": "FIR Copy",
        "marriage certificate": "Marriage Certificate",
        "birth certificate": "Birth Certificate",
        "rent agreement": "Rent Agreement",
        "invoice": "Invoice/Bill",
        "warranty": "Warranty Card",
    }
    for keyword, doc_name in doc_map.items():
        if keyword in query_lower:
            context["provided_documents"].append(doc_name)

    # ── Category-specific enrichment ─────────────────────────────────────────
    if category == "Financial Disputes":
        if "cheque" in query_lower or "bounce" in query_lower:
            context["key_factors"] = ["cheque bounce", "NI Act 138", "demand notice", "Magistrate"]
        elif "salary" in query_lower or "wages" in query_lower:
            context["key_factors"] = ["unpaid salary", "Payment of Wages Act", "Labour Commissioner"]
        elif "loan" in query_lower:
            context["key_factors"] = ["loan recovery", "RBI guidelines", "Banking Ombudsman"]

    elif category == "Family Law":
        if "divorce" in query_lower:
            context["key_factors"] = ["divorce", "Hindu Marriage Act", "Family Court", "grounds"]
        elif "maintenance" in query_lower or "alimony" in query_lower:
            context["key_factors"] = ["maintenance", "CrPC 125", "Family Court", "monthly allowance"]
        elif "custody" in query_lower:
            context["key_factors"] = ["custody", "child welfare", "Guardians and Wards Act", "Family Court"]

    elif category == "Cyber Complaints":
        if "upi" in query_lower or "otp" in query_lower or "fraud" in query_lower:
            context["key_factors"] = ["UPI fraud", "IT Act 66C", "cybercrime portal", "bank reversal"]
        elif "hack" in query_lower:
            context["key_factors"] = ["hacking", "IT Act 66", "cybercrime", "account recovery"]

    elif category == "General Criminal Issues":
        if "bail" in query_lower:
            context["key_factors"] = ["bail", "CrPC 436", "CrPC 437", "Magistrate", "Sessions Court"]
        elif "fir" in query_lower or "police" in query_lower:
            context["key_factors"] = ["FIR", "CrPC 154", "police complaint", "Magistrate"]

    return context


def run_agent(query: str) -> Dict[str, Any]:
    """
    Main agent loop: Domain Guard → Detect Category → Plan → Execute → Verify → Replan.
    """
    # Step 1: Domain Guard
    if not is_legal_query(query):
        return {
            "status": "out_of_scope",
            "message": OUT_OF_SCOPE_RESPONSE,
            "query": query
        }

    # Step 2: Build context with category detection
    context = build_context_from_query(query)

    # Step 3: Plan
    plan = plan_tools(query, context)

    # Step 4: Execute
    results = execute_plan(plan, context)

    # Step 5: Verify — replan if ethical guard failed
    attempts = 0
    while not context.get("approved_for_output", True) and attempts < MAX_REPLAN_ATTEMPTS:
        attempts += 1
        replan = ["strategy_gen", "ethical_guard"]
        results.update(execute_plan(replan, context))

    # Step 6: Assemble final output
    strategy = context.get("strategy_draft")
    return {
        "status": "success",
        "query": query,
        "category": context.get("category", "General Legal Advice"),
        "case_summary": context.get("case_summary"),
        "applicable_laws": _format_statutes(context.get("applicable_statutes", [])),
        "detected_conflicts": [
            c.model_dump() if hasattr(c, "model_dump") else c
            for c in context.get("conflict_list", [])
        ],
        "missing_evidence": [
            m.model_dump() if hasattr(m, "model_dump") else m
            for m in context.get("missing_documents", [])
        ],
        "judicial_precedents": [
            r.model_dump() if hasattr(r, "model_dump") else r
            for r in context.get("ranked_cases", [])
        ],
        "legal_strategy": (
            strategy.model_dump() if strategy and hasattr(strategy, "model_dump")
            else strategy
        ),
        "risk_score": context.get("risk_score", 0),
        "compliance_flag": results.get("compliance_flag", "PASS"),
        "completeness_score": results.get("completeness_score"),
        "case_readiness": results.get("case_readiness"),
        "rag_context_used": bool(context.get("rag_context")),
    }


def _format_statutes(statutes) -> list:
    if not statutes:
        return []
    return [
        {
            "section": s.section if hasattr(s, "section") else s.get("section", ""),
            "content": (s.content if hasattr(s, "content") else s.get("content", ""))[:300],
            "source": s.source if hasattr(s, "source") else s.get("source", ""),
        }
        for s in statutes
    ]
