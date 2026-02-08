from llm.gemini_client import client, MODEL_NAME
from prompts.principles import build_principles_prompt


def analyze_principles(repo_context: dict) -> dict:
    """
    Analyzes engineering principles demonstrated in the codebase.

    Expected output:
    - principles_detected
    - evidence
    - violations
    - consistency_score
    """

    prompt = build_principles_prompt(repo_context)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            'response_mime_type': 'application/json'
        }
    )

    return response.text
