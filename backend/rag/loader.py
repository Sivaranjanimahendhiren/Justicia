"""
Document loader for Justicia RAG pipeline.
Loads markdown, JSON, and CSV knowledge files.
"""
import os
import json
import csv
from pathlib import Path
from typing import List, Dict, Any


KNOWLEDGE_DIR = Path(__file__).parent.parent.parent / "knowledge"


def load_markdown(filepath: Path) -> Dict[str, Any]:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return {
        "source": filepath.name,
        "type": "markdown",
        "content": content,
        "metadata": {"filename": filepath.name, "path": str(filepath)}
    }


def load_json(filepath: Path) -> Dict[str, Any]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Flatten JSON to text for embedding
    content = json.dumps(data, indent=2)
    return {
        "source": filepath.name,
        "type": "json",
        "content": content,
        "metadata": {"filename": filepath.name, "path": str(filepath)}
    }


def load_csv(filepath: Path) -> Dict[str, Any]:
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    content = "\n".join([str(r) for r in rows])
    return {
        "source": filepath.name,
        "type": "csv",
        "content": content,
        "metadata": {"filename": filepath.name, "path": str(filepath)}
    }


def load_all_documents() -> List[Dict[str, Any]]:
    """Load all knowledge base documents."""
    docs = []
    for filepath in KNOWLEDGE_DIR.iterdir():
        if filepath.suffix == ".md":
            docs.append(load_markdown(filepath))
        elif filepath.suffix == ".json":
            docs.append(load_json(filepath))
        elif filepath.suffix == ".csv":
            docs.append(load_csv(filepath))
    print(f"[Loader] Loaded {len(docs)} documents from knowledge base.")
    return docs
