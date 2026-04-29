"""
Seed script — run once to load knowledge base into ChromaDB.
Usage: python -m backend.rag.seed
"""
from .loader import load_all_documents
from .chunker import chunk_documents
from .vector_store import store_chunks, collection_count


def seed():
    print("[Seed] Starting knowledge base seeding...")
    docs = load_all_documents()
    chunks = chunk_documents(docs)
    store_chunks(chunks)
    print(f"[Seed] Done. Total chunks in DB: {collection_count()}")


if __name__ == "__main__":
    seed()
