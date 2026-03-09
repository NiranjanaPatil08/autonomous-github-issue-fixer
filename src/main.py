from src.rag.repo_loader import clone_repo
from src.rag.file_loader import load_repo_files
from src.rag.chunker import chunk_documents
from src.rag.vector_store import build_vector_store
from src.rag.retriever import get_relevant_chunks
from src.agents.issue_classifier import classify_issue
from src.agents.research_agent import research_issue
from src.agents.fix_generator_agent import generate_fix
from src.agents.reviewer_agent import review_fix
from src.agents.file_finder_agent import find_relevant_files
from src.rag.file_loader import list_repo_files, load_selected_files
from src.agents.pr_agent import create_pull_request


def solve_github_issue(repo_url, issue):
    report = {}

    # Step 1: Classify issue
    classification = classify_issue(issue)
    report["classification"] = classification
    if classification != "BUG":
        report["message"] = "This issue does not require a code fix."
        return report

    # Step 2: Clone repo
    repo_path = clone_repo(repo_url)
    report["repo_path"] = repo_path

    # Step 3: List repo files
    repo_files = list_repo_files(repo_path)
    report["repo_files"] = repo_files

    # Step 4: Find relevant files
    relevant_files = find_relevant_files(issue, repo_files)
    report["relevant_files"] = relevant_files

    # Step 5: Load selected files
    files = load_selected_files(relevant_files, repo_path)
    if not files:
        files = load_selected_files(repo_files[:10], repo_path)
    report["loaded_files"] = list(files.keys())

    # Step 6: Chunk documents
    chunks = chunk_documents(files)
    report["num_chunks"] = len(chunks)
    if not chunks:
        report["error"] = "No code chunks could be created."
        return report

    # Step 7: Build vector store
    vectorstore = build_vector_store(chunks)
    report["vectorstore"] = "Built successfully"

    # Step 8: Research issue
    keywords = research_issue(issue)
    report["research_keywords"] = keywords

    # Step 9: Retrieve relevant code
    docs = get_relevant_chunks(vectorstore, keywords)
    report["retrieved_docs_count"] = len(docs)

    # Step 10: Generate fix
    fix = generate_fix(issue, docs)
    report["generated_fix"] = fix

    # Step 11: Review fix
    final_fix = review_fix(issue, fix)
    report["reviewed_fix"] = final_fix

    # Step 12: Create Pull Request
    pr_url = create_pull_request(
        repo_url,
        final_fix,
        relevant_files[0] if relevant_files else None
    )
    report["pull_request_url"] = pr_url

    return report



if __name__ == "__main__":

    repo_url = input("Enter GitHub repository URL: ")

    issue = input("Describe the GitHub issue: ")

    solve_github_issue(repo_url, issue)
