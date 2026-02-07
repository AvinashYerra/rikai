from radon.complexity import cc_visit
from radon.metrics import mi_visit
from pathlib import Path

def analyze_complexity(repo_path: Path):
    results = []

    for path in repo_path.rglob("*.py"):
        try:
            code = path.read_text(encoding="utf-8")
            cc = sum(block.complexity for block in cc_visit(code))
            mi = mi_visit(code, True)

            results.append({
                "path": str(path.relative_to(repo_path)),
                "cyclomatic_complexity": cc,
                "maintainability_index": mi
            })
        except Exception:
            pass

    return results
