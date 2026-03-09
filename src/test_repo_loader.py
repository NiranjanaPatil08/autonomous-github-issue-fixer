from src.rag.repo_loader import clone_repo

repo_url = "https://github.com/octocat/Hello-World"

path = clone_repo(repo_url)

print("Repo cloned at:")
print(path)
