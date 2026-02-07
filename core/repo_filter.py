from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern

DEFAULT_IGNORES = [
    ".git/",
    "node_modules/",
    "venv/",
    "__pycache__/",
    "*.png",
    "*.jpg",
    "*.zip",
    "*.exe"
]

def build_ignore_spec():
    return PathSpec.from_lines(
        GitWildMatchPattern,
        DEFAULT_IGNORES
    )

def is_ignored(path, spec):
    return spec.match_file(path)
