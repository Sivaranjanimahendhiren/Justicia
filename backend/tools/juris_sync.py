"""
TOOL-001: Juris-Sync
Fetches applicable statutory rules from the knowledge base for a given legal topic and jurisdiction.
"""
from pydantic import BaseModel
from typing import List, Optional
from rag.vector_store import retrieve


class JurisSyncInput(BaseModel):
    topic: str
    jurisdiction: str
    year_from: Optional[int] = 2016


class StatuteResult(BaseModel):
    section: str
    content: str
    source: str
    score: float


class JurisSyncOutput(BaseModel):
    legal_text: List[StatuteResult]
    source: str
    last_updated: str


def juris_sync(inp: JurisSyncInput) -> JurisSyncOutput:
    query = f"{inp.topic} {inp.jurisdiction} law section act"
    # Search across all knowledge sources, not just statutory_rules
    hits = retrieve(query, top_k=5)

    results = []
    for hit in hits:
        results.append(StatuteResult(
            section=hit["metadata"].get("source", "knowledge base"),
            content=hit["content"],
            source=hit["metadata"].get("source", "Justicia-Legal-KB"),
            score=round(hit["score"], 4)
        ))

    return JurisSyncOutput(
        legal_text=results,
        source="Justicia-Legal-KB",
        last_updated="2026-04-01"
    )
