"""
Pytest configuration.
Ensures the project root is on sys.path so `from tools import ...` works
regardless of which directory pytest is invoked from.
"""
import sys
from pathlib import Path

# Add the project root (parent of this conftest.py) to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))