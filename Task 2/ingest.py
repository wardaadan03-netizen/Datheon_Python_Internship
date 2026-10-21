"""CLI entry point for document ingestion."""
from src.ingestion import run_ingestion
from src.logger import get_logger

logger = get_logger("ingest")

if __name__ == "__main__":
    try:
        run_ingestion()
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise