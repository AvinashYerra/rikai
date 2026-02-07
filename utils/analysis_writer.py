import json
from datetime import datetime
from pathlib import Path

def save_repo_analysis(
    repo_path: Path,
    project_type: str,
    dependencies: list,
    entrypoints: list,
    complexity: list,
    test_info: dict
):
    output = {
        "generated_at": datetime.utcnow().isoformat(),
        "project_type": project_type,
        "dependencies": dependencies,
        "entrypoints": entrypoints,
        "complexity": complexity,
        "testing": test_info
    }

    output_path = repo_path / "repo_analysis.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return output_path
