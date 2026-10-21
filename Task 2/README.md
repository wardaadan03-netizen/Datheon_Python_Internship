# 📚 Document Q&A Assistant (RAG + Vector Embeddings)

> **Task 2 — Datheon Python + Generative AI & LangChain Internship**

A production-grade **Retrieval-Augmented Generation (RAG)** pipeline that
answers questions strictly from your own PDF documents — with **page-level
source citations** and an **anti-hallucination guardrail**.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Design Decisions](#-design-decisions)
- [Deliverables Checklist](#-deliverables-checklist)
- [License](#-license)

---

## 🎯 Overview

Most LLM chatbots hallucinate when asked about documents they've never seen.
This project solves that by implementing a **RAG pipeline**:

1. **Load** PDF documents from disk
2. **Split** them into overlapping text chunks
3. **Embed** each chunk into a high-dimensional vector
4. **Store** the vectors in a persistent vector database (ChromaDB)
5. **Retrieve** the most relevant chunks for each user query
6. **Generate** an answer using an LLM — **grounded only in retrieved context**
7. **Cite** the exact source file and page number for every answer

The assistant **refuses to answer** when the information isn't in the loaded
documents, eliminating hallucination.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **PDF Ingestion** | Loads all `.pdf` files from a configurable `data/` folder |
| ✂️ **Recursive Chunking** | Splits text with `RecursiveCharacterTextSplitter` (1000 chars / 200 overlap) |
| 🔢 **Vector Embeddings** | Uses Google's `gemini-embedding-001` model |
| 🗄️ **Persistent Vector Store** | ChromaDB persisted to disk — ingest once, query many times |
| 🔍 **Semantic Retrieval** | Top-K similarity search returns the most relevant chunks |
| 💬 **Grounded Answers** | LLM answers **only** from retrieved context |
| 📎 **Source Citations** | Every answer includes file name, page number, and snippet |
| 🛡️ **Anti-Hallucination** | Refuses out-of-scope questions with a clear message |
| ⚙️ **Centralized Config** | Pydantic settings load from `.env` with validation |
| 📝 **Structured Logging** | Timestamped INFO/ERROR logs across all modules |
| 🧪 **Unit Tests** | Pytest smoke tests for ingestion logic |

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1 — INGESTION (run once per document set)            │
│                                                             │
│  data/*.pdf  →  PyPDFLoader  →  TextSplitter  →  Gemini     │
│                                                      ↓      │
│                                              Embeddings     │
│                                                      ↓      │
│                                              ChromaDB       │
│                                         (vectorstore/)     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PHASE 2 — QUERY (run on every question)                    │
│                                                             │
│  User Question  →  Retriever  →  Top-K Chunks  →  Gemini    │
│                                                      ↓      │
│                                                  Answer     │
│                                                      ↓      │
│                                       Answer + Citations    │
└─────────────────────────────────────────────────────────────┘

Module Responsibilities
Module	Responsibility
src/config.py	Loads and validates env vars via Pydantic
src/logger.py	Centralized, structured logging
src/ingestion.py	Load PDFs → split → embed → persist to ChromaDB
src/retriever.py	Loads ChromaDB and returns a configured retriever
src/qa_engine.py	Builds the RAG chain, enforces grounding, formats citations
🧰 Tech Stack
Layer	Technology
Language	Python 3.10+
Orchestration	LangChain
LLM	Google Gemini (gemini-3.8-flash)
Embeddings	Google gemini-embedding-001
Vector Store	ChromaDB (persistent)
PDF Loader	PyPDF
Config	Pydantic Settings + python-dotenv
Testing	Pytest
📁 Project Structure
text
rag-document-assistant/
│
├── data/                          # Your PDF files go here (gitignored)
│   └── sample.pdf
│
├── src/
│   ├── __init__.py
│   ├── config.py                  # Pydantic settings
│   ├── logger.py                  # Structured logging
│   ├── ingestion.py               # Load → Split → Embed → Persist
│   ├── retriever.py               # Chroma retriever factory
│   └── qa_engine.py               # RAG chain + citations
│
├── tests/
│   └── test_ingestion.py          # Unit tests
│
├── vectorstore/                   # ChromaDB persistence (gitignored)
│   ├── chroma.sqlite3
│   └── ...
│
├── .env                           # Your secrets (gitignored)
├── .env.example                   # Template (safe to commit)
├── .gitignore
├── ingest.py                      # CLI: ingestion entry point
├── query.py                       # CLI: Q&A entry point
├── requirements.txt
└── README.md
📋 Prerequisites
Python 3.10 or higher

pip (comes with Python)

A Google Gemini API key — get one free at
aistudio.google.com/apikey

A text-based PDF (selectable text, not a scanned image)

⚠️ Scanned/image-only PDFs will produce empty results. OCR is out of scope.

🚀 Installation
1. Clone the repository
bash
git clone <your-repo-url>
cd rag-document-assistant
2. Create and activate a virtual environment
macOS / Linux:

bash
python3 -m venv .venv
source .venv/bin/activate
Windows (PowerShell):

powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
3. Install dependencies
bash
pip install -r requirements.txt
Or install manually:

bash
pip install langchain langchain-google-genai langchain-chroma langchain-classic \
            langchain-community chromadb pypdf python-dotenv \
            pydantic pydantic-settings pytest
⚙️ Configuration
1. Create your .env file
bash
cp .env.example .env
2. Edit .env and add your Gemini API key
env
# Required
GOOGLE_API_KEY=AIzaSy...your-real-key-here...

# Optional overrides (defaults shown)
GEMINI_CHAT_MODEL=gemini-3.8-flash
GEMINI_EMBEDDING_MODEL=models/gemini-embedding-001
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVER_TOP_K=4
VECTORSTORE_DIR=./vectorstore
DATA_DIR=./data
🔑 Where to get a key: aistudio.google.com/apikey
→ Create API key → copy the value that starts with AIzaSy

⚠️ Never commit .env — it's already listed in .gitignore.

3. Add your documents
Place one or more .pdf files into the data/ folder:

bash
mkdir -p data
cp /path/to/your_document.pdf data/
💻 Usage
Step 1 — Ingest your documents (run once)
bash
python ingest.py
Expected output:

text
2026-10-20 15:30:11 | INFO     | src.ingestion | Loading: sample.pdf
2026-10-20 15:30:12 | INFO     | src.ingestion | Loaded 12 pages across 1 file(s).
2026-10-20 15:30:12 | INFO     | src.ingestion | Split into 47 chunks.
2026-10-20 15:30:15 | INFO     | src.ingestion | Embedding 47 chunks → ChromaDB...
2026-10-20 15:30:18 | INFO     | src.ingestion | Vector store persisted at vectorstore
2026-10-20 15:30:18 | INFO     | src.ingestion | ✅ Ingestion complete.
Step 2 — Ask questions
bash
python query.py
Sample session:

text
💬 Document Q&A Assistant — type 'exit' to quit.

❓ Question: What are the main findings of the document?

============================================================
📖 Answer
============================================================
The document concludes that the primary findings are...

============================================================
📎 Sources
------------------------------------------------------------
  [1] sample.pdf  —  page 3
      "The main findings of this study indicate that..."
============================================================

❓ Question: What is the capital of France?

============================================================
📖 Answer
============================================================
I could not find that information in the provided documents.
============================================================

❓ Question: exit
Goodbye.
Re-ingestion
Scenario	Command
Added a new PDF	python ingest.py (appends to store)
Changed embedding model	rm -rf vectorstore/ then python ingest.py
Clean rebuild	rm -rf vectorstore/ then python ingest.py
💡 Always re-ingest after changing the embedding model — old vectors
become incompatible with new embeddings.

🔬 How It Works
1. Ingestion
python
# Load
loader = PyPDFLoader("data/sample.pdf")
docs = loader.load()                      # List[Document] with page metadata

# Split
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,                 # Preserves start offset
)
chunks = splitter.split_documents(docs)   # ~1000-char chunks with metadata

# Embed + Store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=GoogleGenerativeAIEmbeddings(model="gemini-embedding-001"),
    persist_directory="./vectorstore",
)
2. Retrieval
python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4},               # Top 4 most similar chunks
)
3. Generation with Grounding
The prompt enforces strict grounding:

text
You are a strict document Q&A assistant.

Rules:
- Answer ONLY using the provided context.
- If the answer is not in the context, respond exactly with:
  "I could not find that information in the provided documents."
- Be concise and factual.
- Do not speculate or use outside knowledge.

Context:
{context}

Question: {question}
4. Citation Extraction
Every retrieved chunk carries metadata:

python
{
    "source": "data/sample.pdf",
    "page": 2,             # 0-indexed
    "start_index": 1450
}
Citations are deduplicated by (file, page) and formatted:

text
[1] sample.pdf  —  page 3
    "The main findings..."
🧪 Testing
Run the unit test suite:

bash
pytest tests/ -v
Expected:

text
tests/test_ingestion.py::test_split_documents_preserves_metadata PASSED
The test verifies that chunking preserves source metadata — critical for
citation accuracy.

🐛 Troubleshooting
Error	Cause	Fix
ModuleNotFoundError: No module named 'langchain_google_genai'	Package not installed	pip install langchain-google-genai
ModuleNotFoundError: No module named 'langchain.chains'	LangChain v1 moved legacy chains	pip install langchain-classic, then from langchain_classic.chains import RetrievalQA
ValidationError: GOOGLE_API_KEY field required	.env missing or wrong var name	Variable must be exactly GOOGLE_API_KEY
404 NOT_FOUND: models/embedding-001	Deprecated embedding model	Set GEMINI_EMBEDDING_MODEL=models/gemini-embedding-001 and re-ingest
404 NOT_FOUND: gemini-2.5-flash	Model restricted to new users	Set GEMINI_CHAT_MODEL=gemini-3.8-flash
429 ResourceExhausted	Free-tier rate limit	Wait 60s or enable billing
401 Unauthenticated	Invalid API key	Regenerate at aistudio.google.com/apikey
RuntimeError: Vector store is empty	Ingestion not run	Run python ingest.py
FileNotFoundError: No PDFs found in data	No PDFs in data/	Add a .pdf to data/
Empty answers	PDF is scanned image	Use a text-based PDF
Debugging tips
bash
# 1. Verify .env is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GOOGLE_API_KEY'))"

# 2. Verify vectorstore exists
ls vectorstore/

# 3. Fix Notepad UTF-16 encoding issues
$content = Get-Content .env -Raw
[System.IO.File]::WriteAllText("$PWD\.env", $content, [System.Text.UTF8Encoding]::new($false))
🧠 Design Decisions
Decision	Rationale
Recursive chunking	Preserves paragraph/sentence boundaries better than naive splitting
Chunk overlap (200 chars)	Prevents context loss at chunk boundaries
add_start_index=True	Enables precise citation reconstruction
ChromaDB	Free, embedded, persistent — no server needed
gemini-3.8-flash	Fast, cheap, and available to new users
Anti-hallucination prompt	Explicit refusal instruction beats post-hoc filtering
Pydantic Settings	Fail-fast on missing config; no silent defaults for secrets
Structured logging	Debuggable in production; visible in CI logs
Separated modules	Each concern (ingest, retrieve, generate) is unit-testable
Why not OpenAI?
The task allows any LLM. Gemini offers a free tier, so the project is
reproducible at zero cost — ideal for an internship deliverable.

Why langchain-classic?
LangChain v1 moved legacy chains (RetrievalQA) into a separate package.
The project uses it for compatibility while remaining on the latest
langchain-core.

✅ Deliverables Checklist
☑ Load PDF/text documents
☑ Chunk text recursively
☑ Generate vector embeddings
☑ Store embeddings in ChromaDB
☑ Retrieve relevant context for user queries
☑ Answer questions strictly based on loaded documents
☑ Provide source page citations
☑ Anti-hallucination guardrail (refuses out-of-scope queries)
☑ Reproducible setup via .env.example + README
☑ Unit tests
☑ Structured logging
📸 Evidence (Screenshots)
#	Screenshot	Description
1	Ingestion success	python ingest.py completing with ✅
2	Grounded answer	Query returned with Sources block (file + page)
3	Refusal	Off-topic query returns "could not find"
4	Project structure	ls -Force showing .env, data/, vectorstore/, src/
📄 License
This project is part of the Datheon Python + Generative AI & LangChain
Internship (Task 2) and is intended for educational and evaluation purposes.

🙏 Acknowledgments
LangChain — RAG orchestration framework

ChromaDB — Embedded vector database

Google AI Studio — Gemini API access

PyPDF — PDF text extraction



