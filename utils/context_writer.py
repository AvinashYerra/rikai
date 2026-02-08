import json
from pathlib import Path


def save_repo_context(repo_path: str, context: dict):
    out_dir = Path(repo_path) / ".analysis"
    out_dir.mkdir(exist_ok=True)

    path = out_dir / "repo_context.json"
    with open(path, "w") as f:
        json.dump(context, f, indent=2)

    return str(path)
