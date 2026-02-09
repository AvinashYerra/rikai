def build_principles_prompt(context: dict) -> str:
    return f"""
Analyze engineering principles in the context below.

CONTEXT:
{context}

Respond in STRICT JSON:
{{
  "principles": [
    {{
      "principle": "str",
      "implementation": "str",
      "status": "followed|violated|partial"
    }}
  ],
  "consistency_score": int // 0-100
}}

Return ONLY JSON.
"""
