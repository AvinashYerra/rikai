def build_architecture_prompt(context: dict) -> str:
    return f"""
You are a principal software architect.

Analyze the following repository metadata:

{context}

Your task is to infer the system architecture and return EXACTLY ONE valid JSON object.
Do NOT include explanations, markdown, comments, or extra text.

STRICT OUTPUT RULES:
- Output must be valid JSON.
- Follow the schema EXACTLY.
- Do not add additional keys.
- Do not rename fields.
- Do not return null values.
- If something is unknown, return an empty array [].
- Keep descriptions concise (max 30 words).

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
