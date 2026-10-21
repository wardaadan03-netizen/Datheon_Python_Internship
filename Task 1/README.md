# 🏗️ Structured LLM Prompt Pipeline & JSON Extractor

A production-grade Python pipeline that extracts structured data from unstructured text (such as invoices and resumes) and enforces strict schema validation using **Google Gemini**, **Pydantic**, and **Few-Shot Prompt Engineering**.

## 📖 Overview

This project demonstrates how to build a reliable, deterministic data extraction pipeline using Large Language Models (LLMs). Instead of relying on fragile regex or hoping the LLM returns the correct format, this pipeline dynamically injects a JSON schema into the prompt, utilizes few-shot examples to anchor the model's behavior, and strictly validates the output using Pydantic.

### ✨ Key Features

- **Schema-First Design:** Uses Pydantic `BaseModel` to define the target output structure. The schema is automatically converted and injected into the LLM prompt.
- **Native JSON Enforcement:** Leverages Gemini's `response_mime_type="application/json"` and `response_schema` to force the model to return valid, parseable JSON.
- **Few-Shot Prompting:** Includes curated examples in the prompt to guide the LLM's tone, formatting, and edge-case handling.
- **Strict Validation:** The LLM output is parsed and fed directly into Pydantic, raising clear errors if the model hallucinates fields or uses incorrect data types.
- **Zero-Cost Tier:** Fully compatible with Google AI Studio's free tier (Gemini 3.8 Flash).

## 📂 Project Structure

```text
structured-llm-extractor/
│
├── .env.example                  # Environment variable template
├── .gitignore                    # Prevents committing secrets and venv
├── requirements.txt              # Project dependencies
├── README.md
├── main.py                       # Executable entry point
│
├── app/
│   ├── __init__.py
│   ├── config.py                 # SDK initialization & model config
│   ├── schemas.py                # Pydantic models (Invoice, Resume)
│   ├── prompts.py                # System prompt & few-shot templates
│   ├── extractor.py              # Core pipeline logic
│   └── utils.py                  # Helper functions (JSON cleaning)
│
└── examples/
    ├── invoice_sample.txt        # Sample unstructured invoice
    └── resume_sample.txt         # Sample unstructured resume

    🚀 Quick Start
1. Prerequisites
Python 3.9+

A free Google AI Studio account.

2. Installation
Clone the repository and set up a virtual environment:

bash
git clone https://github.com/yourusername/structured-llm-extractor.git
cd structured-llm-extractor

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
3. Environment Configuration
Copy the example environment file and add your API key:

bash
cp .env.example .env
Open .env and add your Gemini API key:

env
GEMINI_API_KEY=AIzaSy...your-actual-key-here
4. Run the Pipeline
bash
python main.py
🛠️ Usage
To use this pipeline for your own custom data models, simply define a new Pydantic schema in app/schemas.py, then pass it to the extractor function.

python
from app.schemas import Resume
from app.extractor import extract_structured_data

raw_text = "Hi, I'm John Doe. I'm a Senior Python Developer with 5 years of experience."

# Extract and validate
validated_resume = extract_structured_data(raw_text, Resume)

# Access typed data securely
print(validated_resume.candidate_name)
print(validated_resume.skills)
Adding a New Schema (Example: Receipt)
python
# In app/schemas.py
from pydantic import BaseModel, Field

class Receipt(BaseModel):
    store_name: str = Field(description="Name of the store")
    total_amount: float = Field(description="Total amount paid")
    date: str = Field(description="Date of purchase in YYYY-MM-DD format")
🧠 Architecture & Design Decisions
Why Pydantic? LLMs are probabilistic. Even with JSON mode enabled, they occasionally omit optional fields or return strings instead of floats. Pydantic acts as a strict gatekeeper, ensuring your application only receives perfectly typed data.

Why Few-Shot? A zero-shot prompt often results in the LLM adding conversational filler (e.g., "Here is the JSON you requested:"). Few-shot examples train the model to output only the raw JSON.

Why Gemini 3.8 Flash? It provides an excellent balance of speed, reasoning capability, and a generous free tier, making it perfect for development and testing without incurring costs.

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📄 License
This project is licensed under the MIT License.

text

### Next Steps for you:
1. Create the `README.md` file in your project.
2. Paste the text above into it.
3. Run your git commands again:
   ```bash
   git add README.md
   git commit -m "docs: add professional README"
   git push

