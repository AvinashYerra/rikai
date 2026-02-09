from llm.gemini_client import client, MODEL_NAME
from prompts.risks import build_risks_prompt

def analyze_risks(context: dict) -> dict:
    """
    Identifies code smells and risks.
    """
    prompt = build_risks_prompt(context)

    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=prompt,
        config={
            'response_mime_type': 'application/json'
        }
    )

    return response.text
