"""
TOOL-005: Ethical-Guard
Validates generated legal strategy for neutrality, factual grounding, and compliance.
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class EthicalGuardInput(BaseModel):
    strategy_draft: str
    case_facts: Optional[Dict[str, Any]] = {}


class Issue(BaseModel):
    issue_type: str
    description: str
    severity: str  # low | medium | high


class EthicalGuardOutput(BaseModel):
    compliance_flag: str  # PASS | FAIL | REVIEW
    issues_found: List[Issue]
    neutrality_score: float
    approved_for_output: bool


DISCLAIMER_PHRASES = ["not legal advice", "consult a qualified", "ai-assisted", "advocate"]
OVERCONFIDENCE_PHRASES = ["guaranteed win", "certain victory", "will definitely win", "100% success"]
UNGROUNDED_PHRASES = ["fraud", "criminal", "cheating", "scam"]


def ethical_guard(inp: EthicalGuardInput) -> EthicalGuardOutput:
    issues = []
    score = 100.0
    draft_lower = inp.strategy_draft.lower()
    facts_str = str(inp.case_facts).lower()

    # Check for overconfidence
    for phrase in OVERCONFIDENCE_PHRASES:
        if phrase in draft_lower:
            issues.append(Issue(
                issue_type="overconfidence",
                description=f"Strategy contains outcome guarantee: '{phrase}'",
                severity="high"
            ))
            score -= 30
            break

    # Check for ungrounded allegations
    for phrase in UNGROUNDED_PHRASES:
        if phrase in draft_lower and phrase not in facts_str:
            issues.append(Issue(
                issue_type="ungrounded_allegation",
                description=f"'{phrase}' alleged without factual basis in case facts",
                severity="high"
            ))
            score -= 40
            break

    # Check for missing disclaimer
    has_disclaimer = any(p in draft_lower for p in DISCLAIMER_PHRASES)
    if not has_disclaimer:
        issues.append(Issue(
            issue_type="missing_disclaimer",
            description="Legal disclaimer absent from strategy output",
            severity="medium"
        ))
        score -= 10

    # Check minimum length (strategy should be substantive)
    if len(inp.strategy_draft) < 200:
        issues.append(Issue(
            issue_type="insufficient_content",
            description="Strategy draft is too brief to be useful",
            severity="medium"
        ))
        score -= 15

    score = max(score, 0.0)

    if score >= 70:
        flag = "PASS"
    elif score >= 50:
        flag = "REVIEW"
    else:
        flag = "FAIL"

    return EthicalGuardOutput(
        compliance_flag=flag,
        issues_found=issues,
        neutrality_score=score,
        approved_for_output=(score >= 70)
    )
