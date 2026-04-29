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


SYSTEM_PROMPT = """You are JUSTICIA, an AI legal assistant specializing in Indian law across all categories:
Family Law, Domestic Violence, Consumer Complaints, Financial Disputes, Property/RERA,
Employment, Cyber Crimes, Criminal matters, Civil Disputes, and General Legal Advice.
Generate structured, factual, court-ready legal strategies citing specific Indian law sections.
Never guarantee outcomes. Always include a disclaimer.
Output must be valid JSON matching the CourtArgument schema."""


def strategy_gen(inp: StrategyGenInput) -> StrategyGenOutput:
    # Use category-aware builder (works without OpenAI key in dev)
    try:
        from agent.domain_guard import detect_category
        from agent.strategy_builder import get_strategy_for_query
        category = detect_category(inp.case_summary)
        raw = get_strategy_for_query(inp.case_summary, category, {})
        argument = CourtArgument(**raw)
        return StrategyGenOutput(structured_court_argument=argument)
    except Exception:
        pass

    # Fallback: real OpenAI call
    ethical_note = ""
    if inp.ethical_issues_to_fix:
        ethical_note = f"\n\nFix these issues: {json.dumps([e if isinstance(e, dict) else e.model_dump() for e in inp.ethical_issues_to_fix])}"

    user_prompt = f"""Generate a legal strategy for this Indian law case:

Case Summary: {inp.case_summary}
Client Goal: {inp.client_desired_outcome}
Risk Score: {inp.risk_score}/100
{ethical_note}

Return JSON with keys: case_summary, applicable_acts_sections (list), legal_grounds (list),
evidence_strategy, precedent_arguments (list), compensation_calculation,
recommended_relief, risk_assessment, immediate_action_items (list), disclaimer."""

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
