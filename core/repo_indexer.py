from pathlib import Path

def index_repository(root: Path, ignore_spec):
    files = []

    for path in root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(root)
            if ignore_spec.match_file(str(rel)):
                continue

            files.append({
                "path": str(rel),
                "suffix": path.suffix,
                "size": path.stat().st_size
            })

    return files
