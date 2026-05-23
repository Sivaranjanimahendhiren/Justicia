"""
Tests for the empty-collection guard in rag/vector_store.py

Covers:
  - retrieve() returns [] when collection has 0 documents (was a crash before this fix)
  - retrieve() clamps n_results when collection has fewer docs than top_k
  - retrieve() passes through unchanged when collection is large enough
"""
import pytest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_collection(count: int):
    """Return a mock ChromaDB collection with the given document count."""
    col = MagicMock()
    col.count.return_value = count
    return col


def _make_query_result(n: int):
    """Return a minimal ChromaDB query result dict with n hits."""
    ids       = [f"chunk_{i}" for i in range(n)]
    documents = [f"content {i}" for i in range(n)]
    metadatas = [{"source": f"src_{i}"} for i in range(n)]
    distances = [0.1 * i for i in range(n)]
    return {"ids": [ids], "documents": [documents],
            "metadatas": [metadatas], "distances": [distances]}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestRetrieveEmptyGuard:

    @patch("backend.rag.vector_store.embed_single", return_value=[0.1] * 1536)
    @patch("backend.rag.vector_store.get_collection")
    def test_returns_empty_list_when_collection_is_empty(self, mock_get_col, mock_embed):
        """
        Before this fix, ChromaDB raised an exception when n_results > count.
        retrieve() must now return [] immediately without calling collection.query().
        """
        mock_get_col.return_value = _make_collection(count=0)

        from backend.rag.vector_store import retrieve
        result = retrieve("any query", top_k=5)

        assert result == [], "Expected [] for empty collection"
        mock_get_col.return_value.query.assert_not_called()

    @patch("backend.rag.vector_store.embed_single", return_value=[0.1] * 1536)
    @patch("backend.rag.vector_store.get_collection")
    def test_clamps_n_results_when_fewer_docs_than_top_k(self, mock_get_col, mock_embed):
        """
        When collection has 3 docs but top_k=5, n_results must be clamped to 3.
        """
        col = _make_collection(count=3)
        col.query.return_value = _make_query_result(3)
        mock_get_col.return_value = col

        from backend.rag.vector_store import retrieve
        result = retrieve("query", top_k=5)

        call_kwargs = col.query.call_args.kwargs
        assert call_kwargs["n_results"] == 3, (
            f"n_results should be clamped to 3, got {call_kwargs['n_results']}"
        )
        assert len(result) == 3

    @patch("backend.rag.vector_store.embed_single", return_value=[0.1] * 1536)
    @patch("backend.rag.vector_store.get_collection")
    def test_uses_full_top_k_when_collection_is_large_enough(self, mock_get_col, mock_embed):
        """
        When collection has more docs than top_k, n_results must equal top_k unchanged.
        """
        col = _make_collection(count=100)
        col.query.return_value = _make_query_result(5)
        mock_get_col.return_value = col

        from backend.rag.vector_store import retrieve
        result = retrieve("query", top_k=5)

        call_kwargs = col.query.call_args.kwargs
        assert call_kwargs["n_results"] == 5
        assert len(result) == 5

    @patch("backend.rag.vector_store.embed_single", return_value=[0.1] * 1536)
    @patch("backend.rag.vector_store.get_collection")
    def test_result_shape_is_correct(self, mock_get_col, mock_embed):
        """Each returned hit must have chunk_id, content, metadata, score keys."""
        col = _make_collection(count=10)
        col.query.return_value = _make_query_result(2)
        mock_get_col.return_value = col

        from backend.rag.vector_store import retrieve
        result = retrieve("query", top_k=2)

        assert len(result) == 2
        for hit in result:
            assert set(hit.keys()) == {"chunk_id", "content", "metadata", "score"}
            assert isinstance(hit["score"], float)

    @patch("backend.rag.vector_store.embed_single", return_value=[0.1] * 1536)
    @patch("backend.rag.vector_store.get_collection")
    def test_empty_collection_logs_warning(self, mock_get_col, mock_embed, caplog):
        """retrieve() should log a WARNING when the collection is empty."""
        import logging
        mock_get_col.return_value = _make_collection(count=0)

        from backend.rag.vector_store import retrieve
        with caplog.at_level(logging.WARNING, logger="backend.rag.vector_store"):
            retrieve("query", top_k=5)

        assert any("empty" in r.message.lower() for r in caplog.records), (
            "Expected a warning log mentioning empty collection"
        )

    @patch("backend.rag.vector_store.embed_single", return_value=[0.1] * 1536)
    @patch("backend.rag.vector_store.get_collection")
    def test_source_filter_passed_through(self, mock_get_col, mock_embed):
        """source_filter must be forwarded as a where clause to collection.query()."""
        col = _make_collection(count=10)
        col.query.return_value = _make_query_result(1)
        mock_get_col.return_value = col

        from backend.rag.vector_store import retrieve
        retrieve("query", top_k=3, source_filter="IPC")

        call_kwargs = col.query.call_args.kwargs
        assert call_kwargs["where"] == {"source": "IPC"}

    @patch("backend.rag.vector_store.embed_single", return_value=[0.1] * 1536)
    @patch("backend.rag.vector_store.get_collection")
    def test_no_where_clause_when_no_filter(self, mock_get_col, mock_embed):
        """When source_filter is None, where must be None (not an empty dict)."""
        col = _make_collection(count=10)
        col.query.return_value = _make_query_result(5)
        mock_get_col.return_value = col

        from backend.rag.vector_store import retrieve
        retrieve("query")

        call_kwargs = col.query.call_args.kwargs
        assert call_kwargs["where"] is None