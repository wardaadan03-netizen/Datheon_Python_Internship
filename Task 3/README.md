# Multi-Tool Autonomous AI Agent

A LangChain-powered autonomous AI agent that selects and uses tools to solve multi-step queries through a Thought → Action → Observation loop.

Built as **Task 3** for the Multi-Tool Autonomous AI Agent assignment.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Example Queries](#example-queries)
- [Design Decisions](#design-decisions)
- [Tool Reference](#tool-reference)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Limitations and Future Work](#limitations-and-future-work)
- [License](#license)

## 🧭 Overview

This project implements an autonomous AI agent using LangChain and Google Gemini via `langchain-google-genai`.

The agent is equipped with three tools:

1. **Safe Python Calculator:** Evaluates mathematical expressions using an AST-based approach without `eval()`.
2. **Sandboxed Local File Reader:** Reads local text files while preventing path-traversal attacks.
3. **Web Search:** Retrieves search results using DuckDuckGo with retry logic.

Given a user query, the agent determines which tools are needed, executes them in sequence when necessary, and generates a final response based on the results.

### Example

**User query:**

"Search for the price of an iPhone 16, then calculate 10% tax on it."

**Expected workflow:**

1. Search the web for the product price.
2. Extract the relevant price from the search results.
3. Calculate the price including 10% tax.
4. Return the final answer.

The actual result depends on the search results available when the agent runs.

## ✨ Features

| Feature | Description |
|---|---|
| Autonomous Tool Selection | The language model selects tools based on the user's query. |
| Multi-Step Execution | Supports workflows involving multiple tools. |
| Safe Calculator | Uses AST-based expression evaluation instead of `eval()`. |
| Sandboxed File Reader | Blocks attempts to access files outside the permitted project directory. |
| Web Search | Uses DuckDuckGo with retry logic. |
| Error Handling | Handles common tool and search failures. |
| Configurable Agent | Supports model and iteration-limit configuration. |
| Automated Tests | Includes Pytest tests for tool functionality and safety. |

## 📁 Project Structure

```text
autonomous-agent/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── main.py
│
├── tools/
│   ├── __init__.py
│   ├── calculator.py
│   ├── file_reader.py
│   └── web_search.py
│
└── tests/
    └── test_tools.py
```

**File descriptions:**

- `main.py`: Configures and runs the autonomous agent.
- `tools/calculator.py`: Implements safe mathematical expression evaluation.
- `tools/file_reader.py`: Implements restricted local file access.
- `tools/web_search.py`: Implements DuckDuckGo web search.
- `tests/test_tools.py`: Tests calculator and file-reader behavior.
- `.env.example`: Provides a template for environment variables.
- `requirements.txt`: Lists the project's Python dependencies.

## 🛠️ Prerequisites

Before running the project, ensure you have:

- Python 3.10 or later, compatible with the installed dependencies.
- pip package manager.
- A Google Gemini API key.
- Internet access for model requests and web searches.

Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

## 🚀 Installation

### 1. Clone the repository

Replace the placeholder with your actual repository URL.

```bash
git clone <your-repository-url>
cd autonomous-agent
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Create the environment file

Create a file named `.env` in the project root, or copy the example file if it exists.

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

**macOS/Linux:**

```bash
cp .env.example .env
```

### 2. Add your API key

Open `.env` and add your actual Gemini API key:

```env
GOOGLE_API_KEY=your_actual_google_api_key
```

Do not include quotation marks unless your configuration requires them.

**Security note:** Never upload your real API key to GitHub. Keep `.env` in `.gitignore` and commit only `.env.example` with a placeholder value.

### 3. Verify your model configuration

Ensure `main.py` uses a Gemini model currently supported by your installed `langchain-google-genai` package and available to your API key.

Model availability can change, so check the current Google Gemini documentation if you encounter a model-not-found error.

## ▶️ Usage

From the project root, activate your virtual environment and run:

```bash
python main.py
```

If the application starts successfully, enter a query in the terminal.

Example:

```text
🤖 Autonomous Agent Ready. Type 'exit' to quit.

You: What is 17 * 23 + 4?
```

The agent should select the calculator tool when appropriate and return a response.

To stop the application, enter:

```text
exit
```

You can also use `quit` if supported by your implementation.

## 💬 Example Queries

### Single-tool queries

| Query | Expected Tool |
|---|---|
| What is 17 * 23 + 4? | Python Calculator |
| Read `data.txt` and tell me the budget. | Local File Reader |
| Search for the latest LangChain documentation. | Web Search |

### Multi-step queries

| Query | Expected Tool Sequence |
|---|---|
| Read `data.txt`, find the budget, and calculate 15% of it. | File Reader → Calculator |
| Search for a laptop price, then calculate 10% tax. | Web Search → Calculator |
| Search for Tokyo's population and calculate 5% of it. | Web Search → Calculator |
| Calculate a mathematical expression, then search for related information. | Calculator → Web Search |

Actual tool selection and execution depend on the model's response and the agent configuration.

## 🏗️ Design Decisions

### 1. Safe Calculator

**Problem:** Python's `eval()` can execute arbitrary code if used with untrusted input.

**Solution:** Parse mathematical expressions using Python's Abstract Syntax Tree (AST) and evaluate only explicitly supported operations.

Supported operations may include:

- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Division (`/`)
- Exponentiation (`**`)
- Modulo (`%`)
- Parentheses and unary operators

Function calls, imports, attribute access, and unsupported syntax should be rejected.

### 2. Sandboxed File Reader

**Problem:** Unrestricted file access can expose files outside the intended project directory.

**Solution:** Resolve requested paths against a fixed project root and reject paths that escape the permitted directory.

The implementation also includes a file-size limit to help prevent excessive memory usage.

### 3. Retry-Wrapped Web Search

**Problem:** Web searches may fail because of network errors, timeouts, or rate limits.

**Solution:** Retry selected failures with delays between attempts and return a manageable error message if all attempts fail.

### 4. Iteration Limit

The agent can use a maximum iteration limit to prevent excessive repeated tool calls.

A limit of eight iterations is suitable for a demonstration, although the appropriate value depends on the complexity of the task.

### 5. Low-Temperature Configuration

A low temperature can make tool selection more consistent, although it does not guarantee identical results on every run.

## 🔧 Tool Reference

### `python_calculator(expression: str)`

Evaluates supported arithmetic expressions.

**Example:**

```python
python_calculator.invoke("(3 + 5) * 2")
```

Expected result:

```text
16
```

Only explicitly permitted mathematical syntax should be accepted.

### `local_file_reader(file_path: str)`

Reads a text file located inside the permitted project directory.

**Example:**

```python
local_file_reader.invoke("data.txt")
```

The tool should reject missing files, oversized files, and paths attempting to access locations outside the permitted directory.

### `web_search(query: str)`

Searches the web using DuckDuckGo.

**Example:**

```python
web_search.invoke("LangChain documentation")
```

Results depend on network availability and the search service's response.

## 🧪 Testing

Run the test suite from the project root:

```bash
pytest tests/ -v
```

The project is intended to test cases such as:

- Basic calculator operations.
- Mathematical operator precedence.
- Rejection of unsafe calculator expressions.
- Handling missing files.
- Blocking path-traversal attempts.

Example test names may include:

```text
test_calculator_basic
test_calculator_precedence
test_calculator_rejects_code_injection
test_file_reader_missing_file
test_file_reader_blocks_traversal
```

The actual test results depend on the implementation and the tests included in the repository.

## 🔧 Troubleshooting

### Error: `GOOGLE_API_KEY` missing

- Check that `.env` exists in the project root.
- Confirm the key is correctly named `GOOGLE_API_KEY`.
- Ensure the application loads environment variables before initializing the model.

### Error: Model not found

- Check that the configured Gemini model is still available.
- Update the model identifier if required.
- Verify that your installed LangChain integration supports the selected model.

### Error: Search failed

- Check your internet connection.
- Retry after a short delay if the service is rate-limiting requests.
- Review the search tool's error-handling configuration.

### Error: `ModuleNotFoundError: No module named 'tools'`

- Open the terminal in the project root.
- Activate the project's virtual environment.
- Run `python main.py` from the directory containing `main.py` and the `tools` folder.

### Agent stops at the iteration limit

The agent may have reached its configured maximum number of iterations. Simplify the query or adjust the limit if appropriate.

## 🚧 Limitations and Future Work

This project is a demonstration of tool-using AI agents rather than a production-ready service.

### Current Limitations

- No persistent conversation memory unless explicitly implemented.
- No guaranteed accuracy of model-generated responses.
- Web search depends on an external service.
- Tool selection depends on model behavior.
- API access may have usage limits or costs.
- A command-line interface may be less accessible than a graphical interface.

### Future Improvements

Potential extensions include:

1. Add conversation memory for follow-up questions.
2. Build a Streamlit or FastAPI interface.
3. Improve structured logging and error reporting.
4. Add LangSmith tracing for agent execution monitoring.
5. Introduce more tools with appropriate safety controls.
6. Add Docker support for easier setup.
7. Expand automated tests for edge cases and integration behavior.

These improvements can make the agent easier to use, debug, and extend.

## 📄 License

This project is licensed under the MIT License. Add a `LICENSE` file containing the appropriate MIT License text to the repository if it is not already present.

## 🙏 Acknowledgements

- [LangChain](https://www.langchain.com/) for the agent framework.
- [Google AI Studio](https://aistudio.google.com/) for Gemini API access.
- [DuckDuckGo](https://duckduckgo.com/) for web search.
- [Pytest](https://pytest.org/) for automated testing.

---

**Project:** Multi-Tool Autonomous AI Agent  
**Task:** Task 3  
**Language:** Python  
**Framework:** LangChain  
**Model Provider:** Google Gemini  
**Search Provider:** DuckDuckGo
