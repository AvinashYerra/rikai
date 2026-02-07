from git import Repo
from pathlib import Path

BASE_DIR = Path("data/repos")

def clone_repo(owner: str, repo: str):
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    target = BASE_DIR / f"{owner}__{repo}"

    if target.exists():
        return target

    url = f"https://github.com/{owner}/{repo}.git"
    Repo.clone_from(url, target, depth=1)
    return target
