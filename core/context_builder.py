def build_context(repo_index: dict, repo_analysis: dict):
    return {
        "repo_metadata": {
            "total_files": repo_index["total_files"],
            "file_types": list(
                {f["suffix"] for f in repo_index["files"]}
            )
        },
        "project_type": repo_analysis["project_type"],
        "dependencies": repo_analysis["dependencies"],
        "entrypoints": repo_analysis["entrypoints"],
        "testing": repo_analysis["testing"],
        "complexity_summary": sorted(
            repo_analysis["complexity"],
            key=lambda x: x["cyclomatic_complexity"],
            reverse=True
        )[:5]
    }
