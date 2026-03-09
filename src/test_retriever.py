from src.rag.repo_loader import clone_repo
from src.rag.file_loader import load_repo_files
from src.rag.chunker import chunk_documents
from src.rag.vector_store import build_vector_store
from src.rag.retriever import get_relevant_chunks

repo_url = "https://github.com/pallets/flask"

repo_path = clone_repo(repo_url)

files = load_repo_files(repo_path)

chunks = chunk_documents(files)

vectorstore = build_vector_store(chunks)

query = "How does Flask create routes?"

results = get_relevant_chunks(vectorstore, query)

print("Top results:\n")

for r in results:
    print(r.page_content[:300])
    print("\n---\n")
