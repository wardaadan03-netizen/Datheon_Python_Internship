"""RetrievalQA chain with structured, cited answers."""
import os
from dataclasses import dataclass
from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import RetrievalQA
from langchain_core.documents import Document

from src.config import settings
from src.retriever import get_retriever
from src.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Citation:
    source_file: str
    page: int
    snippet: str


@dataclass
class RAGAnswer:
    answer: str
    citations: List[Citation]


PROMPT_TEMPLATE = """You are a strict document Q&A assistant.

Rules:
- Answer ONLY using the provided context.
- If the answer is not in the context, respond exactly with:
  "I could not find that information in the provided documents."
- Be concise and factual.
- Do not speculate or use outside knowledge.

Context:
{context}

Question: {question}

Answer:"""


class QAEngine:
    def __init__(self) -> None:
        self.llm = ChatGoogleGenerativeAI(
            model=settings.gemini_chat_model,
            temperature=0,
            google_api_key=settings.google_api_key,
        )
        self.retriever = get_retriever()
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": _build_prompt()},
        )

    def ask(self, question: str) -> RAGAnswer:
        logger.info(f"Query: {question}")
        result = self.chain.invoke({"query": question})

        citations = _extract_citations(result["source_documents"])
        return RAGAnswer(answer=result["result"].strip(), citations=citations)


def _build_prompt():
    from langchain_core.prompts import PromptTemplate
    return PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )


def _extract_citations(docs: List[Document]) -> List[Citation]:
    """Deduplicate by (file, page) and keep first snippet."""
    seen, citations = set(), []
    for doc in docs:
        src = os.path.basename(doc.metadata.get("source", "unknown"))
        page = int(doc.metadata.get("page", 0)) + 1  # 1-indexed
        key = (src, page)
        if key in seen:
            continue
        seen.add(key)
        citations.append(
            Citation(
                source_file=src,
                page=page,
                snippet=doc.page_content[:180].replace("\n", " ").strip() + "...",
            )
        )
    return citations