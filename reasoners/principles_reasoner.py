from llm.gemini_client import model
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

    response = model.generate_content(prompt)

    return response.candidates[0].content.parts[0].text
