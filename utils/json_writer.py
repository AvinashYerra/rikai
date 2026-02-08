import json
from pathlib import Path
from datetime import datetime

def save_repo_index(
    repo_path: Path,
    owner: str,
    repo: str,
    files: list
):
    output = {
        "repo": f"{owner}/{repo}",
        "generated_at": datetime.utcnow().isoformat(),
        "total_files": len(files),
        "files": files
    }

    output_path = repo_path / "repo_index.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return output_path

