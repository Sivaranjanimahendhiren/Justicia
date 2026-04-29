"""
Text chunker for Justicia RAG pipeline.
Chunk size: 500 tokens, overlap: 50 tokens.
"""
from typing import List, Dict, Any


CHUNK_SIZE = 500   # characters (approx 125 tokens)
OVERLAP = 50


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def chunk_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Chunk all documents and return list of chunk dicts."""
    chunked = []
    for doc in documents:
        chunks = chunk_text(doc["content"])
        for i, chunk in enumerate(chunks):
            chunked.append({
                "chunk_id": f"{doc['source']}::chunk_{i}",
                "source": doc["source"],
                "type": doc["type"],
                "content": chunk,
                "metadata": {
                    **{k: v for k, v in doc["metadata"].items() if isinstance(v, (str, int, float, bool))},
                    "source": doc["source"],
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            })
    print(f"[Chunker] Created {len(chunked)} chunks from {len(documents)} documents.")
    return chunked
