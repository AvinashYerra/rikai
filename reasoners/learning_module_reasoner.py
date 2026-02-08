from llm.gemini_client import client, MODEL_NAME
from prompts.learning_module import build_learning_module_prompt


def generate_learning_module(enriched_context: dict) -> dict:
    """
    Generates a structured learning module from a real codebase.

    Target audience:
    - Intermediate developers
    - Engineers learning real-world patterns

    Output:
    - Structured, educational, code-grounded content
    """

    prompt = build_learning_module_prompt(enriched_context)

    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=prompt,
        config={
            'response_mime_type': 'application/json'
        }
    )

    return response.text
