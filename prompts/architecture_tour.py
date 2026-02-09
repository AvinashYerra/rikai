def build_architecture_tour_prompt(context: dict, flow_name: str = "Core Flow", beginner_mode: bool = False) -> str:
    mode_instruction = "Focus on high-level concepts and simplified explanations for a new contributor." if beginner_mode else "Provide detailed technical depth and architectural rationale for an experienced engineer."
    
    return f"""
You are a senior staff engineer explaining a complex system to a colleague.
We are performing an interactive architecture walkthrough for the flow: "{flow_name}".

REPOSITORY CONTEXT:
{context}

MODE:
{mode_instruction}

YOUR TASK:
Break down the "{flow_name}" into a logical, step-by-step sequence of operations.
Think like a teacher narrating a real-time tour.

For each step, provide:
1. **Title**: A clear name for this step (e.g., "Request Validation").
2. **Component/File**: The specific module or file where this happens.
3. **Narration**: A paragraph explaining what happens in this step.
4. **Rationale**: Why this step is important for the system's integrity or performance.
5. **Visual Context**: A Mermaid-style node name to represent this step in a graph.

RESPOND STRICTLY IN JSON:
JSON SCHEMA:
{{
  "flow_name": "string",
  "steps": [
    {{
      "step_number": int,
      "title": "string",
      "file": "string",
      "narration": "string",
      "rationale": "string",
      "visual_id": "string"
    }}
  ],
  "graph_definition": "string" // A Mermaid graph definition (graph TD) connecting the visual_ids of all steps.
}}

Return ONLY the JSON.
"""
