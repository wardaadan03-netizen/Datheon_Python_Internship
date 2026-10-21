SYSTEM_PROMPT = """
You are an expert data extraction assistant. Your task is to extract structured data
from unstructured text and output it as a valid JSON object.

Rules:
1. Follow the provided JSON schema EXACTLY.
2. Do NOT wrap the output in markdown (no ```json ... ```).
3. Return ONLY the raw JSON object.
4. If a field is not present, use null for optional fields.
5. Never invent data that is not in the source text.
"""

# Few-shot examples to anchor the model's behavior
FEW_SHOT_EXAMPLES = [
    {
        "role": "user",
        "content": (
            "Extract data from this text: 'Invoice #INV-2023-001 from Acme Corp "
            "dated 2023-10-25. We bought 2 Widgets for $50 each and 1 Gadget "
            "for $100. Total is $200.'"
        ),
    },
    {
        "role": "assistant",
        "content": (
            '{"invoice_number": "INV-2023-001", "vendor_name": "Acme Corp", '
            '"invoice_date": "2023-10-25", "items": ['
            '{"description": "Widgets", "quantity": 2, "unit_price": 50.0, "total": 100.0}, '
            '{"description": "Gadget", "quantity": 1, "unit_price": 100.0, "total": 100.0}], '
            '"total_amount": 200.0, "currency": "USD"}'
        ),
    },
]


def build_user_prompt(text: str, schema_json: str) -> str:
    return f"""
Extract the relevant data from the following unstructured text.
Here is the JSON schema you must conform to:
{schema_json}

Unstructured text:
\"\"\"{text}\"\"\"

Return ONLY raw JSON, no markdown blocks.
"""