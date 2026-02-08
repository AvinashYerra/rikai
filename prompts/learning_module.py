def build_learning_module_prompt(context: dict) -> str:
    return f"""
You are a senior software engineer and technical educator.

Your task is to create a guided learning module based ENTIRELY on the provided
GitHub repository. This is NOT a theoretical tutorial.

Repository semantic context:
{context["repo_context"]}

Static and structural analysis:
{context["static_analysis"]}

Instructions:
- Treat this repository as a real-world case study
- Explain WHAT was built and WHY it was built this way
- Ground every explanation in the actual codebase
- Prefer concrete examples over abstractions
- Avoid generic best practices unless they clearly apply here

Create a SHORT but HIGH-QUALITY learning module aimed at INTERMEDIATE developers.

Structure the module as follows:

Module 1: Big Picture Architecture
- Explain the overall system architecture
- Identify core components and their responsibilities
- Describe how data or control flows through the system

Module 2: Key Execution Flows
- Walk through 1–2 critical execution paths
- Identify entry points and lifecycle of requests/jobs

Module 3: Engineering Principles in Practice
For each principle that genuinely appears in the codebase:
- Name the principle
- Explain how it is applied here
- Cite relevant files or folders
- Explain WHY this approach is beneficial in this system

Focus on (only if present):
- Separation of concerns
- Code reuse and modularity
- Error handling patterns
- Configuration management
- Performance or scalability considerations
- Readability and maintainability

Module 4: Design Decisions & Tradeoffs (if inferable)
- Highlight notable design choices
- Explain what was optimized for
- Mention any visible tradeoffs

Module 5: How to Learn From This Repo
- What an engineer should study first
- Which files are the best learning entry points
- What concepts this repo teaches particularly well

IMPORTANT:
- Include small, illustrative code snippets ONLY when they add clarity
- Snippets must be short and directly relevant
- Do NOT invent files or patterns that are not present

Output STRICTLY in JSON with keys:
- title
- modules (list of sections with heading + content)
"""
