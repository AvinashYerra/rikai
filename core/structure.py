import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import collections

# Common programming languages by extension
EXTENSION_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "JavaScript (React)",
    ".tsx": "TypeScript (React)",
    ".html": "HTML",
    ".css": "CSS",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".h": "C/C++ Header",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".scala": "Scala",
    ".sh": "Shell",
    ".md": "Markdown",
    ".json": "JSON",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".xml": "XML",
    ".sql": "SQL",
}

def get_file_stats(path: Path) -> Dict[str, Any]:
    """Get file statistics."""
    stats = path.stat()
    return {
        "size": stats.st_size,
        "extension": path.suffix,
        "language": EXTENSION_MAP.get(path.suffix, "Unknown"),
        "name": path.name,
        "path": str(path)
    }

def generate_file_tree(root_path: Path, ignore_dirs: List[str] = None) -> Dict[str, Any]:
    """
    Generates a nested dictionary representing the file structure.
    Also collects aggregate stats.
    """
    if ignore_dirs is None:
        ignore_dirs = {".git", "__pycache__", "venv", "node_modules", ".idea", ".vscode", "dist", "build"}
    
    tree = {"name": root_path.name, "type": "directory", "children": []}
    
    # Walk the directory
    try:
        # Sort for consistent order: directories first, then files
        items = sorted(list(root_path.iterdir()), key=lambda x: (not x.is_dir(), x.name.lower()))
        
        for item in items:
            if item.name in ignore_dirs:
                continue
                
            if item.is_dir():
                child_tree = generate_file_tree(item, ignore_dirs)
                if child_tree: # Only add if not empty or ignored
                    tree["children"].append(child_tree)
            else:
                tree["children"].append({
                    "name": item.name,
                    "type": "file",
                    "stats": get_file_stats(item)
                })
                
    except PermissionError:
        pass # Skip unreadable directories
        
    return tree

def get_repo_summary(root_path: Path) -> Dict[str, Any]:
    """
    Analyzes the repository to provide a high-level summary.
    """
    file_count = 0
    extensions = collections.Counter()
    total_size = 0
    
    for root, dirs, files in os.walk(root_path):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "venv", "node_modules"}]
        
        for file in files:
            file_path = Path(root) / file
            file_count += 1
            extensions[file_path.suffix] += 1
            try:
                total_size += file_path.stat().st_size
            except (FileNotFoundError, PermissionError):
                pass

    # Determine main language
    main_language = "Unknown"
    if extensions:
        most_common_ext = extensions.most_common(1)[0][0]
        main_language = EXTENSION_MAP.get(most_common_ext, "Unknown")

    return {
        "file_count": file_count,
        "total_size_bytes": total_size,
        "main_language": main_language,
        "extensions_distribution": dict(extensions)
    }

def render_ascii_tree(tree: Dict[str, Any], prefix: str = "", is_last: bool = True, is_root: bool = True) -> str:
    """
    Renders a file tree as an ASCII string.
    """
    lines = []
    name = tree.get("name", "root")
    node_type = tree.get("type", "directory")
    
    if is_root:
        lines.append(f"{name}/")
    else:
        connector = "└── " if is_last else "├── "
        display_name = f"{name}/" if node_type == "directory" else name
        lines.append(f"{prefix}{connector}{display_name}")
    
    # Calculate new prefix for children
    if is_root:
        new_prefix = ""
    else:
        new_prefix = prefix + ("    " if is_last else "│   ")
    
    children = tree.get("children", [])
    for i, child in enumerate(children):
        last_child = (i == len(children) - 1)
        lines.append(render_ascii_tree(child, new_prefix, last_child, False))
        
        # Add a placeholder line between directories for spacing if needed
        # if child.get("type") == "directory" and not last_child:
        #     lines.append(f"{new_prefix}│")
            
    return "\n".join(lines)
