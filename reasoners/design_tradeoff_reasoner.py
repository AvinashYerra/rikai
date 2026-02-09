from llm.gemini_client import client, MODEL_NAME
from prompts.design_tradeoffs import build_design_tradeoffs_prompt

def analyze_design_tradeoffs(context: dict) -> dict:
    """
    Infers design decisions and tradeoffs.
    """
    prompt = build_design_tradeoffs_prompt(context)

    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=prompt,
        config={
            'response_mime_type': 'application/json'
        }
    )

    return response.text
