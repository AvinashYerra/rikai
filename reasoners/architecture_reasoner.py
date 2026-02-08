from llm.gemini_client import client, MODEL_NAME
from prompts.architecture import build_architecture_prompt

def analyze_architecture(repo_context: dict) -> dict:
    """
    Produces:
    - high_level_components
    - data flow
    - boundaries
    """

    prompt = build_architecture_prompt(repo_context)

    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=prompt,
        config={
            'response_mime_type': 'application/json'
        }
    )

    return response.text
