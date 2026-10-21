"""Basic smoke tests (no LLM calls)."""
from pathlib import Path
from src.ingestion import split_documents
from langchain_core.documents import Document


def test_split_documents_preserves_metadata():
    docs = [Document(page_content="word " * 500, metadata={"source": "a.pdf", "page": 0})]
    chunks = split_documents(docs)
    assert len(chunks) > 1
    assert all("source" in c.metadata for c in chunks)