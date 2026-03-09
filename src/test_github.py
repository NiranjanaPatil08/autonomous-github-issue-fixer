from src.tools.github_client import github_client


repo_name = "octocat/Hello-World"  # replace with your repo
repo = github_client.get_repo(repo_name)

issues = repo.get_issues(state="open")
for issue in issues[:5]:
    print(issue.title)
