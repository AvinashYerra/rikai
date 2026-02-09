import requests
import re
from typing import Optional

def fetch_pr_diff(pr_url: str) -> Optional[str]:
    """
    Fetches the diff of a GitHub Pull Request.
    Appends '.diff' to the URL to get the plain text diff.
    """
    # Normalize URL: remove trailing slashes and ensure it ends with .diff
    pr_url = pr_url.strip().rstrip("/")
    if not pr_url.endswith(".diff"):
        diff_url = f"{pr_url}.diff"
    else:
        diff_url = pr_url

    try:
        response = requests.get(diff_url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(f"Error fetching PR diff: {e}")
        return None

def parse_pr_url(pr_url: str) -> Optional[dict]:
    """
    Parses a GitHub PR URL to extract owner, repo, and PR number.
    Example: https://github.com/streamlit/streamlit/pull/123
    """
    pattern = r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)"
    match = re.match(pattern, pr_url)
    if match:
        return {
            "owner": match.group(1),
            "repo": match.group(2),
            "number": match.group(3)
        }
    return None
