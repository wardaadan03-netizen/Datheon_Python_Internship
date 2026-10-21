import json
import re


def clean_json_output(raw: str) -> str:
    """
    Strips markdown code fences or stray whitespace in case the LLM ignores instructions.
    """
    raw = raw.strip()
    # Remove ```json ... ``` or ``` ... ```
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return raw.strip()


def try_parse_json(raw: str) -> dict:
    """Attempts to parse cleaned JSON; raises a clear error on failure."""
    cleaned = clean_json_output(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}\nRaw output:\n{raw}")