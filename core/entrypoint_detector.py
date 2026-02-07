from pathlib import Path

def detect_entrypoints(repo_path: Path):
    entrypoints = []

    for path in repo_path.rglob("*.py"):
        if path.name in ("main.py", "app.py"):
            entrypoints.append(str(path.relative_to(repo_path)))
            continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                if 'if __name__ == "__main__"' in content:
                    entrypoints.append(str(path.relative_to(repo_path)))
        except Exception:
            pass

    return list(set(entrypoints))
