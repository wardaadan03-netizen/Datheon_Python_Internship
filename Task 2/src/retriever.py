"""Reusable retriever factory."""
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever

from src.config import settings
from src.logger import get_logger

logger = get_logger(__name__)


def get_retriever() -> VectorStoreRetriever:
    """Load the persisted Chroma store and return a retriever."""
    if not any(settings.vectorstore_dir.iterdir()):
        raise RuntimeError(
            "Vector store is empty. Run `python ingest.py` first."
        )
    embeddings = GoogleGenerativeAIEmbeddings(
        model=settings.gemini_embedding_model,
        google_api_key=settings.google_api_key,
    )
    vectorstore = Chroma(
        persist_directory=str(settings.vectorstore_dir),
        embedding_function=embeddings,
        collection_name="documents",
    )
    logger.info(f"Retriever ready (top_k={settings.retriever_top_k}).")
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.retriever_top_k},
    )