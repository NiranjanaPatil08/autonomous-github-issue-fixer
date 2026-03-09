from src.rag.repo_loader import clone_repo
from src.rag.file_loader import load_repo_files
from src.rag.chunker import chunk_documents
from src.rag.vector_store import build_vector_store
from src.rag.retriever import get_relevant_chunks
from src.agents.fix_generator_agent import generate_fix
from src.agents.research_agent import research_issue
from src.agents.reviewer_agent import review_fix


repo_url = "https://github.com/pallets/flask"

issue = "Flask route is not working correctly in blueprint"

repo_path = clone_repo(repo_url)

files = load_repo_files(repo_path)

chunks = chunk_documents(files)

vectorstore = build_vector_store(chunks)

keywords = research_issue(issue)

print("\nResearch keywords:\n")
print(keywords)

docs = get_relevant_chunks(vectorstore, keywords)


fix = generate_fix(issue, docs)

final_fix = review_fix(issue, fix)

print("\nFinal Reviewed Fix:\n")
print(final_fix)
