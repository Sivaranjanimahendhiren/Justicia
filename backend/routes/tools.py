"""
Individual tool API endpoints — for direct tool invocation and Kore.ai integration.
"""
from fastapi import APIRouter
from backend.tools import (
    juris_sync, JurisSyncInput,
    fact_conflict, FactConflictInput,
    gap_detector, GapDetectorInput,
    precedent_ranker, PrecedentRankerInput,
    ethical_guard, EthicalGuardInput,
    strategy_gen, StrategyGenInput
)

router = APIRouter(prefix="/tools")


@router.post("/juris-sync")
def api_juris_sync(inp: JurisSyncInput):
    return juris_sync(inp)


@router.post("/fact-conflict")
def api_fact_conflict(inp: FactConflictInput):
    return fact_conflict(inp)


@router.post("/gap-detector")
def api_gap_detector(inp: GapDetectorInput):
    return gap_detector(inp)


@router.post("/precedent-ranker")
def api_precedent_ranker(inp: PrecedentRankerInput):
    return precedent_ranker(inp)


@router.post("/ethical-guard")
def api_ethical_guard(inp: EthicalGuardInput):
    return ethical_guard(inp)


@router.post("/strategy-gen")
def api_strategy_gen(inp: StrategyGenInput):
    return strategy_gen(inp)
