"""
Embedding layer for Justicia RAG pipeline.
Model: text-embedding-3-large (OpenAI)
"""
import os
from typing import List
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBEDDING_MODEL = "text-embedding-3-large"


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of texts using OpenAI text-embedding-3-large."""
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )
    return [item.embedding for item in response.data]


def embed_single(text: str) -> List[float]:
    """Embed a single text string."""
    return embed_texts([text])[0]
