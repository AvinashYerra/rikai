import re

GITHUB_REPO_REGEX = re.compile(
    r"https?://github\.com/([^/]+)/([^/]+)(\.git)?/?$"
)

def parse_github_url(url: str):
    match = GITHUB_REPO_REGEX.match(url.strip())
    if not match:
        return None
    owner, repo, _ = match.groups()
    return owner, repo
