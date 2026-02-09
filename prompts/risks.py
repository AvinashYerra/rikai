def build_risks_prompt(context: dict) -> str:
    return f"""
Identify code smells and technical risks in the context below.

CONTEXT:
{context}

Respond in STRICT JSON:
{{
  "risks": [
    {{
      "area": "str",
      "issue": "str",
      "suggestion": "str",
      "risk_level": "low|medium|high"
    }}
  ]
}}

Return ONLY JSON.
"""
