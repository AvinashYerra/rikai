def build_architecture_prompt(context: dict) -> str:
    return f"""
Analyze the architecture using the context below. 

CONTEXT:
{context}

Respond in STRICT JSON:
{{
  "components": [ {{ "name": "str", "description": "str", "files": ["str"] }} ],
  "flows": [ {{ "from": "str", "to": "str", "description": "str" }} ],
  "boundaries": [ {{ "name": "str", "description": "str", "includes": ["str"] }} ]
}}

Return ONLY the JSON.
"""
