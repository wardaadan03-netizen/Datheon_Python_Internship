import pytest
from tools import python_calculator, local_file_reader

def test_calculator_basic():
    assert python_calculator.invoke("2 + 2") == "4"

def test_calculator_precedence():
    assert python_calculator.invoke("(3 + 5) * 2") == "16"

def test_calculator_rejects_code_injection():
    # Must not execute function calls or attribute access
    result = python_calculator.invoke("__import__('os').system('ls')")
    assert "error" in result.lower()

def test_file_reader_missing_file():
    assert "not found" in local_file_reader.invoke("does_not_exist.txt").lower()

def test_file_reader_blocks_traversal():
    result = local_file_reader.invoke("../../etc/passwd")
    assert "denied" in result.lower()