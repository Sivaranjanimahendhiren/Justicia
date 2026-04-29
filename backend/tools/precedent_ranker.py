"""
TOOL-004: Precedent-Ranker
Ranks case law precedents by relevance to the current case using RAG retrieval.
"""
from pydantic import BaseModel
from typing import List, Optional
from rag.vector_store import retrieve


class PrecedentRankerInput(BaseModel):
    case_summary: str
    key_factors: Optional[List[str]] = []
    top_n: Optional[int] = 3


class RankedCase(BaseModel):
    rank: int
    case_name: str
    content_snippet: str
    relevance_score: float
    source: str
    applicable_to_current_case: str


class PrecedentRankerOutput(BaseModel):
    ranked_cases: List[RankedCase]


def precedent_ranker(inp: PrecedentRankerInput) -> PrecedentRankerOutput:
    query = inp.case_summary
    if inp.key_factors:
        query += " " + " ".join(inp.key_factors)

    # Search across all sources — dataset has 100 cases with precedents
    hits = retrieve(query, top_k=inp.top_n * 2)

    # Score by factor overlap
    scored = []
    for hit in hits:
        factor_score = 0
        if inp.key_factors:
            factor_score = sum(
                1 for f in inp.key_factors if f.lower() in hit["content"].lower()
            ) / max(len(inp.key_factors), 1)
        combined = (hit["score"] * 0.6) + (factor_score * 0.4)
        scored.append({**hit, "combined_score": round(combined, 4)})

    scored.sort(key=lambda x: x["combined_score"], reverse=True)
    top = scored[:inp.top_n]

    ranked = []
    for i, item in enumerate(top):
        lines = item["content"].strip().split("\n")
        case_name = next(
            (l.replace("**Case Name**:", "").replace("case_name", "").strip()
             for l in lines if "Case Name" in l or "case_name" in l),
            f"Relevant Precedent {i+1}"
        )
        ranked.append(RankedCase(
            rank=i + 1,
            case_name=case_name[:80],
            content_snippet=item["content"][:400],
            relevance_score=item["combined_score"],
            source=item["metadata"].get("source", "Justicia-Legal-KB"),
            applicable_to_current_case=(
                f"Relevance score {item['combined_score']:.2f} — "
                "supports your legal claim based on similar facts and applicable law."
            )
        ))

    return PrecedentRankerOutput(ranked_cases=ranked)
