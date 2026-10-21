"""Document ingestion: load → split → embed → persist to ChromaDB."""
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.config import settings
from src.logger import get_logger

logger = get_logger(__name__)


def load_documents(data_dir: Path) -> List[Document]:
    """Load all PDFs from a directory."""
    pdf_files = sorted(data_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDFs found in {data_dir}")

    docs: List[Document] = []
    for pdf in pdf_files:
        logger.info(f"Loading: {pdf.name}")
        loader = PyPDFLoader(str(pdf))
        docs.extend(loader.load())

    logger.info(f"Loaded {len(docs)} pages across {len(pdf_files)} file(s).")
    return docs


def split_documents(docs: List[Document]) -> List[Document]:
    """Recursive chunking with page-tracking metadata preserved."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        add_start_index=True,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    logger.info(f"Split into {len(chunks)} chunks.")
    return chunks


def build_vectorstore(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(
        model=settings.gemini_embedding_model,
        google_api_key=settings.google_api_key,
    )
    logger.info(f"Embedding {len(chunks)} chunks → ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(settings.vectorstore_dir),
        collection_name="documents",
    )
    logger.info(f"Vector store persisted at {settings.vectorstore_dir}")
    return vectorstore


def run_ingestion() -> None:
    """Full ingestion pipeline."""
    docs = load_documents(settings.data_dir)
    chunks = split_documents(docs)
    build_vectorstore(chunks)
    logger.info("✅ Ingestion complete.")