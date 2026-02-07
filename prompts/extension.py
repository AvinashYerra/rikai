def build_extension_prompt(context: dict) -> str:
    return f"""
You are a senior maintainer of this repository.

Based on the repository analysis below:
{context}

Suggest realistic ways the system can evolve.

Focus on:
1. New features aligned with existing architecture
2. Refactoring opportunities that improve maintainability
3. GitHub issues a new contributor could confidently raise
4. Areas safe for extension vs areas that require caution

Respond strictly in JSON with:
- feature_ideas
- refactor_opportunities
- suggested_github_issues
"""
