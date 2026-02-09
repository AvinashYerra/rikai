def build_extension_prompt(context: dict) -> str:
    return f"""
Suggest a roadmap for extending the system based on the context below.

CONTEXT:
{context}

Respond in STRICT JSON:
{{
  "roadmap": [
    {{
      "feature": "str",
      "description": "str",
      "impact": "low|med|high",
      "effort": "low|med|high",
      "difficulty": "str"
    }}
  ]
}}

Return ONLY JSON.
"""
