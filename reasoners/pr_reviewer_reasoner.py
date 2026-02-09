from llm.gemini_client import client, MODEL_NAME
from prompts.pr_reviewer import build_pr_reviewer_prompt

def analyze_pr(context: dict, pr_diff: str) -> dict:
    """
    Performs a deep PR review reasoning pass.
    """
    prompt = build_pr_reviewer_prompt(context, pr_diff)

    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=prompt,
        config={
            'response_mime_type': 'application/json'
        }
    )

    return response.text
