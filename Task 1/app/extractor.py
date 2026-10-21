import json
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError
from google.genai import types

from app.config import client, DEFAULT_MODEL
from app.prompts import SYSTEM_PROMPT, FEW_SHOT_EXAMPLES, build_user_prompt

T = TypeVar("T", bound=BaseModel)


def extract_structured_data(text: str, schema: Type[T], model: str = DEFAULT_MODEL) -> T:
    # 1. Convert Pydantic schema to JSON string
    schema_json = json.dumps(schema.model_json_schema(), indent=2)
    user_prompt = build_user_prompt(text, schema_json)

    # 2. Build the conversation (Few-shot examples + actual prompt)
    contents = []
    for ex in FEW_SHOT_EXAMPLES:
        role = "user" if ex["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=ex["content"])]))
    
    # Add the actual user request
    contents.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))

    # 3. Configure Gemini (System prompt, temp 0, and FORCE JSON)
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.0,
        response_mime_type="application/json",
        # Passing the Pydantic schema directly makes Gemini strictly adhere to it
        response_schema=schema, 
    )

    # 4. Call the API
    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=config
        )
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}")

    raw_output = response.text

    # 5. Parse and Validate
    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini returned invalid JSON: {e}\nRaw: {raw_output}")

    try:
        validated = schema(**parsed)
    except ValidationError as e:
        raise ValueError(f"Pydantic validation failed:\n{e.json(indent=2)}")

    return validated