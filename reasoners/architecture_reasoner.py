from llm.gemini_client import model
from prompts.architecture import build_architecture_prompt

def analyze_architecture(repo_context: dict) -> dict:
    """
    Produces:
    - high_level_components
    - data flow
    - boundaries
    """

    prompt = build_architecture_prompt(repo_context)

    response = model.generate_content(prompt)

    return response.candidates[0].content.parts[0].text
