from llm.gemini_client import client, MODEL_NAME
from prompts.repo_context import build_repo_context_prompt


def analyze_repo_context(repo_url: str, repo_index: dict) -> dict:
    """
    Builds a high-level semantic understanding of the repository.
    """

    prompt = build_repo_context_prompt(
        repo_url=repo_url,
        repo_index=repo_index
    )

    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=prompt,
        config={
            'response_mime_type': 'application/json'
        }
    )

    return response.text