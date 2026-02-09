def build_design_tradeoffs_prompt(context: dict) -> str:
    return f"""
Infer design decisions and tradeoffs from the context below.

CONTEXT:
{context}

Respond in STRICT JSON:
{{
  "decisions": [
    {{
      "decision": "str",
      "rationale": "str",
      "tradeoff": "str",
      "confidence": int // 1-10
    }}
  ]
}}

Return ONLY JSON.
"""
