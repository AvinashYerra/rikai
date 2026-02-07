def classify_project(dependencies: list, files: list):
    dep_set = {dep.lower() for dep in dependencies}
    file_paths = [f["path"].lower() for f in files]

    SIGNALS = {
        "Web Service": {
            "deps": ["fastapi", "flask", "django", "starlette"],
            "files": []
        },
        "Data Pipeline": {
            "deps": ["airflow", "dbt", "pyspark"],
            "files": ["dag"]
        },
        "CLI Tool": {
            "deps": ["click", "typer"],
            "files": ["argparse", "cli"]
        },
        "UI Application": {
            "deps": ["streamlit", "gradio"],
            "files": []
        },
        "ML System": {
            "deps": ["torch", "tensorflow", "sklearn"],
            "files": []
        }
    }

    scores = {category: 0 for category in SIGNALS}

    # Score dependency signals
    for category, signal in SIGNALS.items():
        for dep in signal["deps"]:
            if dep in dep_set:
                scores[category] += 2  # deps are strong signals

    # Score file-path signals
    for category, signal in SIGNALS.items():
        for token in signal["files"]:
            if any(token in path for path in file_paths):
                scores[category] += 1  # file names are weaker signals

    # Filter categories with non-zero scores
    detected = {k: v for k, v in scores.items() if v > 0}

    if not detected:
        return "Library / Unknown"

    # Sort by score
    sorted_types = sorted(detected.items(), key=lambda x: x[1], reverse=True)

    # Mixed system if multiple strong signals
    if len(sorted_types) > 1 and sorted_types[0][1] == sorted_types[1][1]:
        return "Mixed System"

    return sorted_types[0][0]
