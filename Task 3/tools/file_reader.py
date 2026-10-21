import os
from pathlib import Path
from langchain_core.tools import tool

# Anchor sandbox to the directory containing this project (parent of tools/)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent

@tool
def local_file_reader(file_path: str) -> str:
    """Read the contents of a local text file inside the project directory.
    Input must be a relative path, e.g., 'data.txt' or 'notes/todo.txt'."""
    try:
        resolved = (_PROJECT_ROOT / file_path).resolve()

        # Reject path traversal attempts
        if not str(resolved).startswith(str(_PROJECT_ROOT)):
            return "Error: Access outside the project directory is denied."

        if not resolved.exists():
            return f"Error: File '{file_path}' not found."

        if not resolved.is_file():
            return f"Error: '{file_path}' is not a file."

        # Basic size guard (prevent loading 10GB files into memory)
        if resolved.stat().st_size > 1_000_000:
            return "Error: File is too large (max 1MB)."

        return resolved.read_text(encoding="utf-8")

    except Exception as e:
        return f"Error reading file: {e}"