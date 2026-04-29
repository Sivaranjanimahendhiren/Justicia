"""
TOOL-003: Gap-Detector
Audits client's documents against the mandatory RERA evidence checklist.
"""
import json
from pathlib import Path
from pydantic import BaseModel
from typing import List


CHECKLIST_PATH = Path(__file__).parent.parent.parent / "knowledge" / "evidence_checklist.json"


class GapDetectorInput(BaseModel):
    provided_documents: List[str]
    checklist_id: str = "JUSTICIA-RERA-CHECKLIST-v1"


class MissingDoc(BaseModel):
    doc_id: str
    document_type: str
    mandatory: bool
    how_to_obtain: str


class GapDetectorOutput(BaseModel):
    missing_documents: List[MissingDoc]
    completeness_score: float
    case_readiness: str


def gap_detector(inp: GapDetectorInput) -> GapDetectorOutput:
    with open(CHECKLIST_PATH, "r") as f:
        checklist = json.load(f)

    mandatory_docs = [d for d in checklist["required_documents"] if d["mandatory"]]
    provided_lower = [p.lower().strip() for p in inp.provided_documents]

    missing = []
    for doc in mandatory_docs:
        doc_type_lower = doc["document_type"].lower()
        # Fuzzy match: check if any provided doc contains the doc type keyword
        matched = any(
            doc_type_lower in p or any(word in p for word in doc_type_lower.split())
            for p in provided_lower
        )
        if not matched:
            missing.append(MissingDoc(
                doc_id=doc["doc_id"],
                document_type=doc["document_type"],
                mandatory=True,
                how_to_obtain=doc.get("how_to_obtain", "Contact builder or relevant authority.")
            ))

    total_mandatory = len(mandatory_docs)
    provided_count = total_mandatory - len(missing)
    score = round((provided_count / total_mandatory) * 100, 1) if total_mandatory > 0 else 0.0

    if score == 100:
        readiness = "ready"
    elif score >= 70:
        readiness = "needs_attention"
    else:
        readiness = "not_ready"

    return GapDetectorOutput(
        missing_documents=missing,
        completeness_score=score,
        case_readiness=readiness
    )
