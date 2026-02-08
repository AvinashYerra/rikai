def build_architecture_prompt(context: dict) -> str:
    return f"""
You are a senior software architect.

Repository semantic context:
{context['repo_context']}

Static analysis signals:
{context['static_analysis']}

Using BOTH:
- Infer the real architecture
- Avoid generic assumptions
- Ground decisions in repository intent

Respond in JSON with:
JSON SCHEMA:

{{
  "components": [
    {{
      "name": "API Layer",
      "description": "Entry point for external clients. Responsible for request routing, validation, authentication, and response formatting.",
      "files": [
        "app.py",
        "routes/*.py",
        "controllers/*.py"
      ]
    }}
  ],
  "flows": [
    {{
      "from": "API Layer",
      "to": "Service Layer",
      "description": "Validated requests are passed to services for business processing."
    }}
  ],
  "boundaries": [
    {{
      "name": "API",
      "description": "Handles HTTP interaction and request lifecycle.",
      "includes": ["API Layer"]
    }},
    {{
      "name": "Core Logic",
      "description": "Contains domain rules and business workflows.",
      "includes": ["Service Layer", "Domain Models"]
    }},
    {{
      "name": "Infrastructure",
      "description": "External integrations such as databases, queues, and third-party services.",
      "includes": ["Database Layer", "Messaging", "External Clients"]
    }}
  ]
}}

Return ONLY the JSON.
"""
