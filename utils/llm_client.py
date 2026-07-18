"""
llm_client.py
Simple wrapper so all agents call the LLM the same way.
Uses the modern google-genai SDK.
"""

import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # reads GEMINI_API_KEY from a .env file in the project root

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Create a file named '.env' in the project root "
        "with this line inside it:\nGEMINI_API_KEY=your-key-here"
    )

client = genai.Client(api_key=api_key)

DEFAULT_MODEL = "gemini-3.1-flash-lite"


def call_llm(system_prompt: str, user_prompt: str, model: str = DEFAULT_MODEL, json_mode: bool = False) -> str:
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json" if json_mode else None,
    )
    response = client.models.generate_content(
        model=model,
        contents=user_prompt,
        config=config,
    )
    return response.text


def call_llm_json(system_prompt: str, user_prompt: str, model: str = DEFAULT_MODEL) -> dict:
    raw = call_llm(system_prompt, user_prompt, model=model, json_mode=True)
    return json.loads(raw)