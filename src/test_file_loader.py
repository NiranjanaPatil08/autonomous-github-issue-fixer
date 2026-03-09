from src.rag.repo_loader import clone_repo
from src.rag.file_loader import load_repo_files

repo_url = "https://github.com/pallets/flask"

repo_path = clone_repo(repo_url)

docs = load_repo_files(repo_path)

print("Files loaded:", len(docs))

for doc in docs[:5]:
    print(doc["file_path"])
