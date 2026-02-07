from pathlib import Path

def parse_requirements(repo_path: Path):
    deps = set()

    for req_file in repo_path.rglob("*requirements*.txt"):
        try:
            with open(req_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        deps.add(line.split("==")[0])
        except Exception:
            pass

    return sorted(deps)
