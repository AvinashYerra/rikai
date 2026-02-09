from llm.gemini_client import client, MODEL_NAME
from prompts.architecture_tour import build_architecture_tour_prompt

def analyze_architecture_tour(context: dict, flow_name: str = "Core Flow", beginner_mode: bool = False) -> dict:
    """
    Generates a step-by-step architectural tour data.
    """
    prompt = build_architecture_tour_prompt(context, flow_name, beginner_mode)

    response = client.models.generate_content(
        model=MODEL_NAME, 
        contents=prompt,
        config={
            'response_mime_type': 'application/json'
        }
    )

    return response.text
