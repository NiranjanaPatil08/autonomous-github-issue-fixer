import requests


def fetch_github_issue(repo_url, issue_number):

    # Example repo_url
    # https://github.com/pallets/flask

    parts = repo_url.rstrip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"

    response = requests.get(api_url)

    if response.status_code != 200:
        raise Exception("Failed to fetch issue from GitHub")

    data = response.json()

    issue_title = data["title"]
    issue_body = data["body"]

    return f"{issue_title}\n\n{issue_body}"
