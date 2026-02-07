def build_principles_prompt(context: dict) -> str:
    return f"""
You are a senior software engineer performing a codebase review.

Given the repository analysis below:
{context}

Identify engineering principles in practice.

Analyze:
1. Modularity & separation of concerns
2. DRY vs duplication
3. Error handling discipline
4. Configuration vs hardcoding
5. Testability and extensibility

Respond strictly in JSON with:
- principles_detected: list of principles
- evidence: map of principle -> files or patterns
- violations: list of issues or weak spots
- consistency_score: number from 1 to 10
"""
