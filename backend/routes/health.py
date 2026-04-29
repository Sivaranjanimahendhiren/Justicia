from fastapi import APIRouter
from backend.rag.vector_store import collection_count

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "Justicia API"}


@router.get("/health/rag")
def rag_health():
    count = collection_count()
    return {"status": "ok", "chunks_in_db": count, "ready": count > 0}
