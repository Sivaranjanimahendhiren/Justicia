"""
Agent Executor — runs the tool plan sequentially, passing outputs as context.
"""
from typing import List, Dict, Any
from tools import (
    juris_sync, JurisSyncInput,
    fact_conflict, FactConflictInput,
    gap_detector, GapDetectorInput,
    precedent_ranker, PrecedentRankerInput,
    ethical_guard, EthicalGuardInput,
    strategy_gen, StrategyGenInput
)
from tools.fact_conflict import ClientStatement, RetrievedFacts


MAX_REPLAN_ATTEMPTS = 2


def execute_plan(plan: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute tool plan and accumulate results into context."""
    results = {}

    for tool_name in plan:
        try:
            if tool_name == "juris_sync":
                out = juris_sync(JurisSyncInput(
                    topic=context.get("topic", "delayed possession RERA"),
                    jurisdiction=context.get("jurisdiction", "Maharashtra"),
                    year_from=2016
                ))
                results["applicable_statutes"] = out.legal_text
                context["applicable_statutes"] = out.legal_text

            elif tool_name == "gap_detector":
                out = gap_detector(GapDetectorInput(
                    provided_documents=context.get("provided_documents", []),
                    checklist_id="JUSTICIA-RERA-CHECKLIST-v1"
                ))
                results["missing_documents"] = out.missing_documents
                results["completeness_score"] = out.completeness_score
                results["case_readiness"] = out.case_readiness
                context["missing_documents"] = out.missing_documents

            elif tool_name == "fact_conflict":
                out = fact_conflict(FactConflictInput(
                    client_statement=ClientStatement(
                        claimed_payment_date=context.get("claimed_payment_date"),
                        claimed_amount_paid=context.get("claimed_amount_paid"),
                        claimed_possession_date=context.get("claimed_possession_date"),
                        documents_claimed=context.get("provided_documents", [])
                    ),
                    retrieved_facts=RetrievedFacts(
                        receipt_payment_date=context.get("receipt_payment_date"),
                        receipt_amount=context.get("receipt_amount"),
                        agreement_possession_date=context.get("agreement_possession_date"),
                        documents_verified=context.get("provided_documents", [])
                    )
                ))
                results["conflict_list"] = out.conflict_list
                results["risk_score"] = out.risk_score
                results["overall_assessment"] = out.overall_assessment
                context["conflict_list"] = out.conflict_list
                context["risk_score"] = out.risk_score

            elif tool_name == "precedent_ranker":
                out = precedent_ranker(PrecedentRankerInput(
                    case_summary=context.get("case_summary", "delayed possession RERA complaint"),
                    key_factors=context.get("key_factors", ["delayed possession", "RERA", "Maharashtra"]),
                    top_n=3
                ))
                results["ranked_cases"] = out.ranked_cases
                context["ranked_cases"] = out.ranked_cases

            elif tool_name == "strategy_gen":
                out = strategy_gen(StrategyGenInput(
                    case_summary=context.get("case_summary", ""),
                    conflict_list=context.get("conflict_list", []),
                    missing_documents=context.get("missing_documents", []),
                    ranked_cases=context.get("ranked_cases", []),
                    applicable_statutes=context.get("applicable_statutes", []),
                    risk_score=context.get("risk_score", 0),
                    client_desired_outcome=context.get("client_desired_outcome", "possession or refund with compensation"),
                    ethical_issues_to_fix=context.get("ethical_issues_to_fix", [])
                ))
                results["strategy_draft"] = out.structured_court_argument
                context["strategy_draft"] = out.structured_court_argument

            elif tool_name == "ethical_guard":
                draft = context.get("strategy_draft")
                draft_text = str(draft.dict()) if draft else ""
                out = ethical_guard(EthicalGuardInput(
                    strategy_draft=draft_text,
                    case_facts=context
                ))
                results["compliance_flag"] = out.compliance_flag
                results["ethical_issues"] = out.issues_found
                results["neutrality_score"] = out.neutrality_score
                results["approved_for_output"] = out.approved_for_output
                context["approved_for_output"] = out.approved_for_output
                context["ethical_issues_to_fix"] = out.issues_found

        except Exception as e:
            results[f"{tool_name}_error"] = str(e)

    return results
