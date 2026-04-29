"""
Justicia — FastAPI Application Entry Point
Run: uvicorn backend.main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.chat import router as chat_router
from backend.routes.tools import router as tools_router
from backend.routes.health import router as health_router
from backend.db.database import create_tables

app = FastAPI(
    title="Justicia — AI Legal Assistant",
    description="Agentic RAG system for Indian Real Estate Disputes under RERA Act",
    version="1.0.0"
)

# CORS — allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(health_router)
app.include_router(chat_router, prefix="/api/v1")
app.include_router(tools_router, prefix="/api/v1")


@app.on_event("startup")
def startup():
    create_tables()
    print("[Justicia] Database tables ready.")
    print("[Justicia] API running at http://localhost:8000")
    print("[Justicia] Docs at http://localhost:8000/docs")
