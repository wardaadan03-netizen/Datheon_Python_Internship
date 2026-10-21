# src/config.py
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    google_api_key: str = Field(..., alias="GOOGLE_API_KEY")
    gemini_chat_model: str = Field("gemini-2.5-flash", alias="GEMINI_CHAT_MODEL")
    gemini_embedding_model: str = Field("models/embedding-001", alias="GEMINI_EMBEDDING_MODEL")
    chunk_size: int = Field(1000, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(200, alias="CHUNK_OVERLAP")
    retriever_top_k: int = Field(4, alias="RETRIEVER_TOP_K")
    vectorstore_dir: Path = Field(Path("./vectorstore"), alias="VECTORSTORE_DIR")
    data_dir: Path = Field(Path("./data"), alias="DATA_DIR")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
settings.vectorstore_dir.mkdir(parents=True, exist_ok=True)