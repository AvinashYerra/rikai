import json
from pathlib import Path

def save_reasoning_output(repo_path: str, reasoning: dict):
    out_dir = Path(repo_path) / ".analysis"
    out_dir.mkdir(exist_ok=True)

    path = out_dir / "reasoning.json"
    with open(path, "w") as f:
        json.dump(reasoning, f, indent=2)

    return str(path)
