def build_execution_flow_prompt(context):
    return f"""
Analyze execution flows for this repo:
{context}

Focus on:
- Entry points
- Request / job lifecycle
- Control branching

Output JSON:
- entry_points
- main_flows
- async_or_background_tasks
"""
