from src.rag.repo_loader import clone_repo
from src.rag.file_loader import load_repo_files
from src.rag.chunker import chunk_documents

repo_url = "https://github.com/pallets/flask"

repo_path = clone_repo(repo_url)

docs = load_repo_files(repo_path)

chunks = chunk_documents(docs)

print("Total files:", len(docs))
print("Total chunks:", len(chunks))

print("\nExample chunk:\n")
print(chunks[0]["content"][:500])
