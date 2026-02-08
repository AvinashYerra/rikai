from llm.gemini_client import client, MODEL_NAME
from prompts.extension import build_extension_prompt


def analyze_extensions(repo_context: dict) -> dict:
    """
    Suggests how the system can be extended.

    Expected output:
    - feature_ideas
    - refactor_opportunities
    - suggested_github_issues
    """

    prompt = build_extension_prompt(repo_context)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            'response_mime_type': 'application/json'
        }
    )

    return response.text
