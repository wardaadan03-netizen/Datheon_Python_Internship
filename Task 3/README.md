### Multi-Tool Autonomous Agent
A LangChain-powered autonomous AI agent that decides which tool to use, when, and why — solving compound research queries through a thought → action → observation reasoning loop.

Built as a Task 3 deliverable for the Multi-Tool Autonomous AI Agent assignment.

### 📋 Table of Contents
## Overview

Features

Project Structure

Prerequisites

Installation

Configuration

Usage

Example Queries

Design Decisions

Tool Reference

Testing

Troubleshooting

Limitations & Future Work

### License

### 🧭 Overview
This project implements an autonomous AI agent using LangChain and OpenAI's gpt-4o-mini. The agent is equipped with three distinct tools:

A safe Python calculator (AST-based — no eval())

A sandboxed local file reader (path-traversal protected)

A real-time web search tool (DuckDuckGo with retry logic)

Given a user query, the agent autonomously decides whether it needs one tool, multiple tools in sequence, or none at all — and returns a final answer after verifying intermediate results.

Example of what it does:

User: "Search for the price of an iPhone 16, then calculate 10% tax on it."

Agent reasoning (printed live):

Thought: I need current pricing → call web_search

Action: web_search("iPhone 16 price 2024")

Observation: "iPhone 16 starts at $799..."

Thought: Now calculate 10% tax → call python_calculator

Action: python_calculator("799 * 1.10")

Observation: "878.9"

Final Answer: "The iPhone 16 costs $799, and with 10% tax it totals $878.90."

✨ Features
Feature	Description
🧠 Autonomous tool selection	The LLM decides which tool (if any) to invoke per step
🔁 Multi-step reasoning	Chains tools together (e.g., search → calculate)
🛡️ Safe calculator	AST-based evaluator — immune to code injection
🔒 Sandboxed file reader	Rejects ../ path traversal attempts
🌐 Real-time web search	DuckDuckGo with 3× retry + exponential backoff
📊 Transparent reasoning	Prints the full Thought → Action → Observation loop
✅ Tested	Pytest suite covering tool safety and correctness
📦 Pinned dependencies	Reproducible installs across machines
📁 Project Structure
text
autonomous-agent/
│
├── .env                  # Your API keys (DO NOT COMMIT)
├── .env.example          # Template — safe to commit
├── .gitignore            # Excludes .env, __pycache__, .venv
├── requirements.txt      # Pinned dependencies
├── README.md             # This file
├── main.py               # Entry point & agent loop
│
├── tools/
│   ├── __init__.py       # Central tool registry
│   ├── calculator.py     # Safe AST-based math evaluator
│   ├── file_reader.py    # Sandboxed project-directory reader
│   └── web_search.py     # DuckDuckGo with retry
│
└── tests/
    └── test_tools.py     # Pytest smoke tests
Why so lean? LangChain's AgentExecutor handles the reasoning loop, so the codebase focuses on tool definitions and agent configuration rather than orchestration. Every file has one responsibility.

🛠 Prerequisites
Python 3.10+ (uses match-style AST walking and type union syntax)


Model: Google Gemini 2.0 Flash via langchain-google-genai
Get a key: https://aistudio.google.com/apikey (free tier available)

pip and venv (bundled with Python)

🚀 Installation
1. Clone and enter the project
bash
git clone <your-repo-url> autonomous-agent
cd autonomous-agent
2. Create a virtual environment
bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
3. Install dependencies
bash
pip install -r requirements.txt
⚙️ Configuration
1. Create your .env file
bash
cp .env.example .env
2. Add your API key
Open .env and replace the placeholder:

bash
GOOGLE_API_KEY=sk-proj-your-actual-key-here
⚠️ Never commit .env. It's already listed in .gitignore.

3. (Optional) Add test data
Create a small file to test the file reader tool:

bash
echo "Project: Phoenix\nBudget: 5000\nStatus: Testing" > data.txt
▶️ Usage
Start the agent
bash
python main.py
You'll see:

text
🤖 Autonomous Agent Ready. Type 'exit' to quit.

You:
Interact
Type any query and press Enter. The agent will:

Print its reasoning steps (thoughts, tool calls, observations)

Return a final answer prefixed with ✅

Type exit or quit to leave, or Ctrl+C to interrupt.

💬 Example Queries
Try these to see different tool combinations in action:

Single-tool queries
Query	Tool used
What is 17 * 23 + 4?	python_calculator
Read data.txt and tell me the budget.	local_file_reader
Who won the 2024 Nobel Prize in Physics?	web_search
Multi-step queries (the interesting ones)
Query	Tools chained
Read data.txt, find the budget, and calculate 15% of it.	file_reader → calculator
Search for the price of a MacBook Air M3, then calculate 10% tax.	web_search → calculator
Look up the population of Tokyo, then find 5% of it.	web_search → calculator
Calculate (47 * 3) - 12, then search for what year that number is associated with.	calculator → web_search
The last two demonstrate autonomous chaining — the agent figures out the sequence itself.

🏗 Design Decisions
Each architectural choice was made with a specific failure mode in mind.

1. Safe calculator — no eval()
Problem: The naive approach (eval(expression)) allows code execution — __import__('os').system('rm -rf /') runs if you're not careful.

Solution: Parse the expression into an AST and recursively evaluate only whitelisted nodes (ast.BinOp, ast.Constant, ast.UnaryOp). Anything else — function calls, attribute access, imports — raises an error and returns a safe string.

python
# ❌ Rejected
result = eval(user_input)

# ✅ Accepted
tree = ast.parse(user_input, mode="eval")
result = _safe_eval(tree.body)
2. Sandboxed file reader — no path traversal
Problem: open(file_path) allows ../../etc/passwd.

Solution: Resolve the path against a fixed project root, then verify the resolved path still starts with that root.

python
resolved = (_PROJECT_ROOT / file_path).resolve()
if not str(resolved).startswith(str(_PROJECT_ROOT)):
    return "Error: Access outside the project directory is denied."
Additionally enforces a 1MB file-size limit to prevent memory issues.

3. Retry-wrapped web search
Problem: DuckDuckGo occasionally returns rate-limit errors or times out.

Solution: Three retry attempts with exponential backoff (1s → 2s → 3s). The agent receives a clean error string rather than crashing.

4. verbose=True on the AgentExecutor
Why: The assignment explicitly requires displaying the reasoning chain. LangChain's verbose mode prints every thought, action, and observation — demonstrating the agent is genuinely autonomous, not just a prompt wrapper.

5. max_iterations=8 cap
Why: Prevents runaway loops if the model gets confused (e.g., repeatedly calling the same failing tool). Eight iterations is enough for any realistic multi-step query.

6. Temperature = 0
Why: Deterministic tool selection. At temperature 0.7, the same query might choose different tools on different runs, which is confusing for a demo or test.

🔧 Tool Reference
python_calculator(expression: str) -> str
Evaluates arithmetic expressions safely.

Allowed: +, -, *, /, **, %, parentheses, unary minus/plus

Forbidden: function calls, names, attribute access, string literals

Example: python_calculator.invoke("(3 + 5) * 2") → "16"

local_file_reader(file_path: str) -> str
Reads a UTF-8 text file inside the project directory.

Sandboxed: Only files under the project root

Size limit: 1 MB

Example: local_file_reader.invoke("data.txt") → file contents

web_search(query: str) -> str
Real-time search via DuckDuckGo.

Retries: 3× with backoff

Example: web_search.invoke("LangChain release notes") → top results as text

🧪 Testing
The project includes a Pytest suite covering tool safety and correctness.

Run tests
bash
pytest tests/ -v
Expected output
text
tests/test_tools.py::test_calculator_basic PASSED
tests/test_tools.py::test_calculator_precedence PASSED
tests/test_tools.py::test_calculator_rejects_code_injection PASSED
tests/test_tools.py::test_file_reader_missing_file PASSED
tests/test_tools.py::test_file_reader_blocks_traversal PASSED

============================== 5 passed in 0.42s ==============================
What's covered
Test	Verifies
test_calculator_basic	"2 + 2" → "4"
test_calculator_precedence	Parentheses respected: "(3+5)*2" → "16"
test_calculator_rejects_code_injection	"__import__('os').system('ls')" returns an error, not execution
test_file_reader_missing_file	Graceful error on nonexistent files
test_file_reader_blocks_traversal	"../../etc/passwd" is denied
Note: Tests do not require an API key — they only exercise the tool functions directly.

🔧 Troubleshooting
Error: GOOGLE_API_KEY missing
You haven't created .env yet. Run cp .env.example .env and paste your key.

Or you created .env but forgot load_dotenv() ran — check that main.py is being run from the project root.

Search failed after 3 attempts
DuckDuckGo is rate-limiting you. Wait a minute and retry.

Or your network blocks the duckduckgo.com domain. Try a VPN or switch to Tavily (see Future Work).

Agent keeps calling the same tool
Rare at temperature=0, but possible with ambiguous prompts. Be more specific: instead of "tell me about iPhone 16", say "search for the iPhone 16 release date, then calculate how many days until launch."

Agent stopped due to iteration limit or time limit
The agent hit max_iterations=8. If your query genuinely needs more steps, raise the cap in main.py — but first, split the query into smaller parts.

ModuleNotFoundError: No module named 'tools'
You're running main.py from outside the project directory. cd into the project root first.

🚧 Limitations & Future Work
This is a demonstration-grade agent, not a production service. Honest limitations:

Known limitations
No memory across turns. Each invoke() is stateless. If you ask "what about the other one?", the agent has no idea what "the other one" refers to.

No conversation history. Same reason — a proper agent would use ConversationBufferMemory.

DuckDuckGo has no SLA. Not suitable for production reliability.

Single-file agent config. Prompt, model, and tool list are hardcoded in main.py. A production version would externalize these.

No streaming. Responses appear all at once rather than token-by-token.

If extended, the next priorities would be
Add conversation memory — ConversationBufferMemory or ConversationSummaryMemory

Swap DuckDuckGo for Tavily — better quality, structured results, SLA

Add structured logging — JSON logs of every tool call for post-hoc debugging

Add a Streamlit / FastAPI UI — turn the CLI into something demo-able

Add tracing — LangSmith integration for visualizing the reasoning chain

Dockerize — Dockerfile + docker-compose.yml for one-command deploy

These were deliberately out of scope for the assignment to keep the codebase readable and reviewable.

📄 License
MIT — free to use, modify, and learn from.

🙏 Acknowledgements
LangChain for the agent framework

Model: Google Gemini 2.0 Flash via langchain-google-genai
Get a key: https://aistudio.google.com/apikey (free tier available)

DuckDuckGo for a free search API

