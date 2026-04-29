"""
/chat endpoint — main entry point for Justicia agent.
"""
import uuid
import time
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.agent.controller import run_agent
from backend.db import get_db, Query, AuditLog

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    session_id: str = None
    client_ref: str = None


class ChatResponse(BaseModel):
    session_id: str
    status: str
    query: str
    case_summary: str = None
    applicable_laws: list = []
    detected_conflicts: list = []
    missing_evidence: list = []
    judicial_precedents: list = []
    legal_strategy: dict = None
    risk_score: float = None
    compliance_flag: str = None
    completeness_score: float = None
    case_readiness: str = None
    message: str = None


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    session_id = req.session_id or str(uuid.uuid4())
    start = time.time()

    # Log agent start
    db.add(AuditLog(
        session_id=session_id,
        event_type="agent_start",
        input_data={"query": req.query}
    ))
    db.commit()

    # Run agent
    result = run_agent(req.query)

    duration_ms = int((time.time() - start) * 1000)

    # Persist query record
    db.add(Query(
        session_id=session_id,
        client_ref=req.client_ref,
        query_text=req.query,
        response_summary=str(result.get("legal_strategy", ""))[:500],
        risk_score=result.get("risk_score"),
        compliance_flag=result.get("compliance_flag"),
        tools_used=["juris_sync", "gap_detector", "fact_conflict", "precedent_ranker", "strategy_gen", "ethical_guard"]
    ))

    # Log agent end
    db.add(AuditLog(
        session_id=session_id,
        event_type="agent_end",
        output_data={"status": result.get("status"), "risk_score": result.get("risk_score")},
        duration_ms=duration_ms
    ))
    db.commit()

    return ChatResponse(session_id=session_id, **result)
