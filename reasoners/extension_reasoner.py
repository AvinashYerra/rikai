from llm.gemini_client import model
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

    response = model.generate_content(prompt)

    return response.candidates[0].content.parts[0].text
