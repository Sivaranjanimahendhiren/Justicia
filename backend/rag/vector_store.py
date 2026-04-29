"""
ChromaDB vector store for Justicia RAG pipeline.
Handles storage and retrieval of embedded document chunks.
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from .embedder import embed_texts, embed_single

COLLECTION_NAME = "justicia_legal_kb"
TOP_K = 5

# Persistent ChromaDB client
_client = chromadb.PersistentClient(path="./chroma_db")


def get_collection():
    return _client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )


def _sanitize_metadata(meta: dict) -> dict:
    """ChromaDB only accepts str/int/float/bool metadata values."""
    clean = {k: v for k, v in meta.items() if isinstance(v, (str, int, float, bool))}
    return clean


def store_chunks(chunks: List[Dict[str, Any]]):
    """Embed and store document chunks in ChromaDB."""
    collection = get_collection()
    texts = [c["content"] for c in chunks]
    embeddings = embed_texts(texts)

    collection.upsert(
        ids=[c["chunk_id"] for c in chunks],
        embeddings=embeddings,
        documents=texts,
        metadatas=[_sanitize_metadata(c["metadata"]) for c in chunks]
    )
    print(f"[VectorStore] Stored {len(chunks)} chunks in ChromaDB.")


def retrieve(query: str, top_k: int = TOP_K, source_filter: str = None) -> List[Dict[str, Any]]:
    """Retrieve top-K relevant chunks for a query."""
    collection = get_collection()
    query_embedding = embed_single(query)

    where = {"source": source_filter} if source_filter else None

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where,
        include=["documents", "metadatas", "distances"]
    )

    hits = []
    for i in range(len(results["ids"][0])):
        hits.append({
            "chunk_id": results["ids"][0][i],
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "score": 1 - results["distances"][0][i]  # cosine similarity
        })
    return hits


def collection_count() -> int:
    return get_collection().count()
