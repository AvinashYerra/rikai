def build_repo_context_prompt(repo_url: str, repo_index: dict) -> str:
    return f"""
You are analyzing a GitHub repository to support deep technical understanding
and education.

Repository URL:
{repo_url}

Repository file structure and metadata:
{repo_index}

Your goal is to build a SEMANTIC CONTEXT that downstream agents can use to:
- Explain architecture
- Teach engineering principles
- Create learning materials grounded in this repo

Infer and extract:

1. Repository purpose and problem being solved
2. Intended audience (library users, contributors, end users, learners)
3. System type (service, tool, library, pipeline, framework, demo)
4. High-level architectural style if visible
5. Files or directories that are central to understanding the system
6. Areas that demonstrate good engineering practices
7. Areas that appear complex, subtle, or educationally valuable

Respond STRICTLY in JSON with keys:
- purpose
- target_audience
- system_type
- architectural_style
- key_learning_components
- notable_engineering_patterns
- complex_or_important_areas
"""
