def build_execution_flow_prompt(context):
    return f"""
You are a senior software architect analyzing repository execution behavior.

Analyze execution flows using ONLY the provided repository signals.

Repository Signals:
{context}

IMPORTANT RULES:
- Respond with STRICT JSON only.
- Do NOT wrap JSON in markdown.
- Do NOT include explanations.
- Do NOT hallucinate files, modules, or flows.
- If uncertain, lower the confidence score instead of guessing.
- Every flow MUST have a type.

----------------------------

RETURN THIS EXACT JSON SCHEMA:

{{
  "entry_points": [
    {{
      "id": "string",
      "file": "string",
      "symbol": "string",
      "type": "web_entry | cli_entry | library_entry | worker_entry | scheduler_entry",
      "confidence": float
    }}
  ],

  "execution_flows": [
    {{
      "id": "string",
      "name": "string",
      "type": "sequential | directed_graph | branching | event_driven",
      "description": "string",
      "confidence": float,
      "architectural_complexity": "low | medium | high",

      "nodes": ["string"],
      
      "edges": [
        {{
          "from": "string",
          "to": "string",
          "interaction": "function_call | network_call | io | event | unknown"
        }}
      ],

      "branches": [
        {{
          "condition": "string",
          "from": "string",
          "to": "string"
        }}
      ],

      "failure_points": ["string"],
      "latency_risk": "low | medium | high"
    }}
  ],

  "async_or_background_tasks": {{
    "execution_model": "synchronous | async | hybrid | unknown",
    "confidence": float,
    "detected_workers": ["string"],
    "notes": ["string"],
    "scaling_implication": "string"
  }}
}}

----------------------------

FLOW TYPE RULES:

- sequential → linear lifecycle
- directed_graph → layered architecture or transport pipelines
- branching → redirects, retries, auth paths
- event_driven → queues, pub/sub, workers

Prefer directed_graph when components interact across layers.

Confidence must be between 0.0 and 1.0.
"""
