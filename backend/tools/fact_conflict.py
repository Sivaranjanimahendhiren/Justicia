"""
TOOL-002: Fact-Conflict
Compares client's statement against documentary evidence to detect contradictions.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ClientStatement(BaseModel):
    claimed_payment_date: Optional[str] = None
    claimed_amount_paid: Optional[float] = None
    claimed_possession_date: Optional[str] = None
    documents_claimed: Optional[List[str]] = []


class RetrievedFacts(BaseModel):
    receipt_payment_date: Optional[str] = None
    receipt_amount: Optional[float] = None
    agreement_possession_date: Optional[str] = None
    documents_verified: Optional[List[str]] = []


class FactConflictInput(BaseModel):
    client_statement: ClientStatement
    retrieved_facts: RetrievedFacts


class Conflict(BaseModel):
    field: str
    client_value: str
    document_value: str
    severity: str  # low | medium | high
    recommendation: str


class FactConflictOutput(BaseModel):
    conflict_list: List[Conflict]
    risk_score: float
    overall_assessment: str


def fact_conflict(inp: FactConflictInput) -> FactConflictOutput:
    conflicts = []
    risk = 0

    cs = inp.client_statement
    rf = inp.retrieved_facts

    # Check payment date
    if cs.claimed_payment_date and rf.receipt_payment_date:
        if cs.claimed_payment_date.strip() != rf.receipt_payment_date.strip():
            conflicts.append(Conflict(
                field="final_payment_date",
                client_value=cs.claimed_payment_date,
                document_value=rf.receipt_payment_date,
                severity="medium",
                recommendation=(
                    "Acknowledge discrepancy in complaint. Use receipt date as authoritative. "
                    "Explain client's verbal statement was an approximation."
                )
            ))
            risk += 25

    # Check amount paid
    if cs.claimed_amount_paid and rf.receipt_amount:
        if abs(cs.claimed_amount_paid - rf.receipt_amount) > 1000:
            conflicts.append(Conflict(
                field="total_amount_paid",
                client_value=str(cs.claimed_amount_paid),
                document_value=str(rf.receipt_amount),
                severity="high",
                recommendation=(
                    "Reconcile payment amounts with all receipts and bank statements. "
                    "High severity — opposing counsel will exploit this."
                )
            ))
            risk += 40

    # Check possession date consistency
    if cs.claimed_possession_date and rf.agreement_possession_date:
        if cs.claimed_possession_date.strip() != rf.agreement_possession_date.strip():
            conflicts.append(Conflict(
                field="agreed_possession_date",
                client_value=cs.claimed_possession_date,
                document_value=rf.agreement_possession_date,
                severity="high",
                recommendation=(
                    "Use the registered Sale Agreement date as the authoritative possession date. "
                    "Verbal recollection is not admissible over registered document."
                )
            ))
            risk += 35

    risk = min(risk, 100)

    if risk == 0:
        assessment = "Low Risk — No contradictions detected"
    elif risk < 40:
        assessment = "Medium Risk — Minor discrepancies detected, addressable"
    elif risk < 70:
        assessment = "Medium-High Risk — Significant discrepancies, must be resolved before filing"
    else:
        assessment = "High Risk — Critical contradictions, case may be weakened"

    return FactConflictOutput(
        conflict_list=conflicts,
        risk_score=risk,
        overall_assessment=assessment
    )
