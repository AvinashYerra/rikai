from llm.gemini_client import client, MODEL_NAME
from prompts.execution_flow import build_execution_flow_prompt

def analyze_execution_flows(context: dict) -> dict:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=build_execution_flow_prompt(context),
        config={
            'response_mime_type': 'application/json'
        }
    )
    return response.text
