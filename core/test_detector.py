def detect_tests(files: list):
    test_files = [
        f["path"] for f in files
        if "test" in f["path"].lower()
    ]

    return {
        "test_file_count": len(test_files),
        "has_tests": len(test_files) > 0,
        "test_files": test_files[:10]
    }
