"""
Justicia — Dev Server (no OpenAI key, no PostgreSQL needed)
Patches OpenAI with mock before loading any modules.

Run: python main_dev.py
"""
import sys, os, json, math, hashlib

# ── Mock OpenAI ───────────────────────────────────────────────────────────────
class _FakeEmbedding:
    def __init__(self, text):
        h = hashlib.md5(text.encode()).hexdigest()
        seed = int(h, 16)
        vec = []
        for i in range(128):
            seed = (seed * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
            val = ((seed >> 33) / (2**31)) - 1.0
            vec.append(val)
        mag = math.sqrt(sum(v*v for v in vec)) or 1.0
        self.embedding = [v/mag for v in vec]

class _FakeEmbeddingsResponse:
    def __init__(self, texts):
        self.data = [_FakeEmbedding(t) for t in texts]

class _FakeEmbeddingsAPI:
    def create(self, model, input):
        texts = input if isinstance(input, list) else [input]
        return _FakeEmbeddingsResponse(texts)

class _FakeChatMessage:
    def __init__(self, content): self.content = content

class _FakeChatChoice:
    def __init__(self, content): self.message = _FakeChatMessage(content)

class _FakeChatResponse:
    def __init__(self, content): self.choices = [_FakeChatChoice(content)]

class _FakeChatAPI:
    def create(self, model, messages, response_format=None, temperature=0.3):
        user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
        # Lazy import to avoid circular issues
        from agent.domain_guard import detect_category
        from agent.strategy_builder import get_strategy_for_query
        category = detect_category(user_msg)
        strategy = get_strategy_for_query(user_msg, category, {})
        return _FakeChatResponse(json.dumps(strategy))

class _FakeOpenAI:
    def __init__(self, api_key=None):
        self.embeddings = _FakeEmbeddingsAPI()
        self.chat = type("Chat", (), {"completions": _FakeChatAPI()})()

import openai as _openai_module
_openai_module.OpenAI = _FakeOpenAI

# ── Seed ChromaDB on startup ──────────────────────────────────────────────────
from rag.loader import load_all_documents
from rag.chunker import chunk_documents
from rag.vector_store import store_chunks, collection_count

def seed_if_empty():
    if collection_count() == 0:
        print("[Justicia] Seeding knowledge base...")
        docs = load_all_documents()
        chunks = chunk_documents(docs)
        store_chunks(chunks)
        print(f"[Justicia] {collection_count()} chunks ready in ChromaDB.")
    else:
        print(f"[Justicia] ChromaDB already has {collection_count()} chunks.")

seed_if_empty()

# ── In-memory query log (replaces PostgreSQL for dev) ────────────────────────
from datetime import datetime
_query_log = []

def log_query(session_id, query, result):
    _query_log.append({
        "session_id": session_id,
        "query": query,
        "risk_score": result.get("risk_score"),
        "compliance_flag": result.get("compliance_flag"),
        "timestamp": datetime.utcnow().isoformat()
    })

# ── FastAPI app ───────────────────────────────────────────────────────────────
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from agent.controller import run_agent

app = FastAPI(
    title="Justicia — AI Legal Assistant (Dev)",
    description="Agentic RAG for Indian Real Estate Disputes under RERA Act",
    version="1.0.0-dev"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    client_ref: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "Justicia Dev API", "chunks_in_db": collection_count()}

@app.post("/api/v1/chat")
def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    result = run_agent(req.query)
    log_query(session_id, req.query, result)
    return {"session_id": session_id, **result}

@app.get("/api/v1/logs")
def get_logs():
    return {"queries": _query_log}

# ── Tool endpoints (direct invocation) ───────────────────────────────────────
from tools.juris_sync import juris_sync, JurisSyncInput
from tools.fact_conflict import fact_conflict, FactConflictInput
from tools.gap_detector import gap_detector, GapDetectorInput
from tools.precedent_ranker import precedent_ranker, PrecedentRankerInput
from tools.ethical_guard import ethical_guard, EthicalGuardInput
from tools.strategy_gen import strategy_gen, StrategyGenInput

@app.post("/api/v1/tools/juris-sync")
def api_juris_sync(inp: JurisSyncInput): return juris_sync(inp)

@app.post("/api/v1/tools/fact-conflict")
def api_fact_conflict(inp: FactConflictInput): return fact_conflict(inp)

@app.post("/api/v1/tools/gap-detector")
def api_gap_detector(inp: GapDetectorInput): return gap_detector(inp)

@app.post("/api/v1/tools/precedent-ranker")
def api_precedent_ranker(inp: PrecedentRankerInput): return precedent_ranker(inp)

@app.post("/api/v1/tools/ethical-guard")
def api_ethical_guard(inp: EthicalGuardInput): return ethical_guard(inp)

@app.post("/api/v1/tools/strategy-gen")
def api_strategy_gen(inp: StrategyGenInput): return strategy_gen(inp)

if __name__ == "__main__":
    import uvicorn
    print("\n[Justicia] Starting dev server on http://localhost:8000")
    print("[Justicia] API docs: http://localhost:8000/docs")
    print("[Justicia] Frontend should point to: http://localhost:8000/api/v1\n")
    uvicorn.run("main_dev:app", host="0.0.0.0", port=8000, reload=False)
