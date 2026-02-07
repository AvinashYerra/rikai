def build_architecture_prompt(context: dict) -> str:
    return f"""
You are a senior software architect.

Given the following repository analysis:
{context}

Infer:
1. Major architectural components
2. How data/control flows between them
3. Logical boundaries (API, core logic, infra)

Respond strictly in JSON with keys:
- components
- flows
- boundaries
"""
