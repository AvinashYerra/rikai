from llm.gemini_client import model
from prompts.execution_flow import build_execution_flow_prompt

def analyze_execution_flows(context: dict) -> dict:
    response = model.generate_content(
        build_execution_flow_prompt(context)
    )
    return response.candidates[0].content.parts[0].text
