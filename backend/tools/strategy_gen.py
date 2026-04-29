"""
TOOL-006: Strategy-Gen
Generates a structured court-ready legal strategy using OpenAI GPT-4o.
"""
import os
import json
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class StrategyGenInput(BaseModel):
    case_summary: str
    conflict_list: Optional[List[Any]] = []
    missing_documents: Optional[List[Any]] = []
    ranked_cases: Optional[List[Any]] = []
    applicable_statutes: Optional[List[Any]] = []
    risk_score: Optional[float] = 0
    client_desired_outcome: Optional[str] = "possession or full refund with compensation"
    ethical_issues_to_fix: Optional[List[Any]] = []


class CourtArgument(BaseModel):
    case_summary: str
    applicable_acts_sections: List[str]
    legal_grounds: List[str]
    evidence_strategy: str
    precedent_arguments: List[str]
    compensation_calculation: str
    recommended_relief: str
    risk_assessment: str
    immediate_action_items: List[str]
    disclaimer: str


class StrategyGenOutput(BaseModel):
    structured_court_argument: CourtArgument


SYSTEM_PROMPT = """You are JUSTICIA, an AI legal assistant specializing in Indian real estate disputes under RERA Act.
Generate structured, factual, court-ready legal strategies. 
Always cite specific RERA sections (Section 18, 19, 31) and relevant case law.
Never guarantee outcomes. Always include a disclaimer.
Output must be valid JSON matching the CourtArgument schema."""


def strategy_gen(inp: StrategyGenInput) -> StrategyGenOutput:
    ethical_note = ""
    if inp.ethical_issues_to_fix:
        ethical_note = f"\n\nIMPORTANT — Fix these ethical issues in your output: {json.dumps([e if isinstance(e, dict) else e.dict() for e in inp.ethical_issues_to_fix])}"

    user_prompt = f"""Generate a legal strategy for this RERA delayed possession case:

Case Summary: {inp.case_summary}
Detected Conflicts: {json.dumps([c if isinstance(c, dict) else c.dict() for c in inp.conflict_list])}
Missing Documents: {json.dumps([m if isinstance(m, dict) else m.dict() for m in inp.missing_documents])}
Relevant Precedents: {json.dumps([r if isinstance(r, dict) else r.dict() for r in inp.ranked_cases])}
Applicable Statutes: {json.dumps([s if isinstance(s, dict) else s.dict() for s in inp.applicable_statutes])}
Risk Score: {inp.risk_score}/100
Client Goal: {inp.client_desired_outcome}
{ethical_note}

Return a JSON object with these exact keys:
{{
  "case_summary": "...",
  "applicable_acts_sections": ["RERA Section 18 — ...", "RERA Section 19 — ..."],
  "legal_grounds": ["Ground 1: ...", "Ground 2: ..."],
  "evidence_strategy": "...",
  "precedent_arguments": ["Precedent 1: ...", "Precedent 2: ..."],
  "compensation_calculation": "...",
  "recommended_relief": "...",
  "risk_assessment": "...",
  "immediate_action_items": ["Step 1: ...", "Step 2: ..."],
  "disclaimer": "This is AI-assisted legal analysis, not legal advice. Consult a qualified advocate before taking any legal action."
}}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.3
    )

    raw = json.loads(response.choices[0].message.content)
    argument = CourtArgument(**raw)
    return StrategyGenOutput(structured_court_argument=argument)
