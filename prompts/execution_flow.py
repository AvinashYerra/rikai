def build_execution_flow_prompt(context):
    return f"""
Analyze repository execution behavior using the context below.

CONTEXT:
{context}

Respond with STRICT JSON:
{{
  "entry_points": [ {{ "id": "str", "file": "str", "symbol": "str", "type": "web|cli|lib|worker|scheduler", "confidence": float }} ],
  "execution_flows": [ {{
      "id": "str", "name": "str", "type": "sequential|graph|branching|event", "description": "str", 
      "nodes": ["str"], "edges": [ {{ "from": "str", "to": "str", "interaction": "call|net|io|event" }} ],
      "branches": [ {{ "condition": "str", "from": "str", "to": "str" }} ],
      "failure_points": ["str"], "latency_risk": "low|med|high"
  }} ],
  "async_or_background_tasks": {{ "execution_model": "sync|async|hybrid", "detected_workers": ["str"] }}
}}

Return ONLY the JSON. No wrap.
"""
