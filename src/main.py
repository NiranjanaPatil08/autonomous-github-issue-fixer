from src.rag.repo_loader import clone_repo
from src.rag.file_loader import load_repo_files, list_repo_files, load_selected_files
from src.rag.chunker import chunk_documents
from src.rag.vector_store import build_vector_store
from src.rag.retriever import get_relevant_chunks
from src.agents.issue_classifier import classify_issue
from src.agents.research_agent import research_issue
from src.agents.fix_generator_agent import generate_fix
from src.agents.reviewer_agent import review_fix
from src.agents.file_finder_agent import find_relevant_files
from src.agents.pr_agent import create_pull_request


def solve_github_issue(repo_url, issue_text):
    """
    Complete GitHub issue solver pipeline:
    - Classify issue
    - Clone repo & load relevant files
    - Chunk & embed code
    - Generate fix using AI agents
    - Review fix
    - Create PR

    Returns a detailed report dictionary for Streamlit.
    """
    report = {}

    # --- Issue classification ---
    report["classification"] = classify_issue(issue_text)

    if report["classification"] != "BUG":
        report["message"] = "This issue does not require a code fix."
        return report

    # --- Clone repository ---
    report["repo_path"] = clone_repo(repo_url)

    # --- List repo files ---
    all_files = list_repo_files(report["repo_path"])
    report["all_files"] = all_files

    # --- Find relevant files ---
    relevant_files = find_relevant_files(issue_text, all_files)
    report["relevant_files"] = relevant_files

    if not relevant_files:
        # Fallback: use first 10 repo files
        relevant_files = all_files[:10]
        report["fallback_files_used"] = True
    else:
        report["fallback_files_used"] = False

    # --- Load selected files ---
    loaded_files = load_selected_files(relevant_files, report["repo_path"])
    report["loaded_files"] = [f["path"] for f in loaded_files]

    if not loaded_files:
        report["message"] = "Error: No files could be loaded for processing."
        return report

    # --- Chunk documents ---
    chunks = chunk_documents(loaded_files)
    report["num_chunks"] = len(chunks)

    if not chunks:
        report["message"] = "Error: No code chunks could be created."
        return report

    # --- Build vector database ---
    vectorstore = build_vector_store(chunks)

    # --- Research keywords ---
    keywords = research_issue(issue_text)
    report["research_keywords"] = keywords

    # --- Retrieve relevant chunks ---
    docs = get_relevant_chunks(vectorstore, keywords)
    report["retrieved_docs_count"] = len(docs)

    # --- Generate fix ---
    fix = generate_fix(issue_text, docs)

    # --- Review fix ---
    final_fix = review_fix(issue_text, fix)

    # Ensure final fix is a string (join if it's a list)
    if isinstance(final_fix, list):
        final_fix = "\n".join(final_fix)
    report["reviewed_fix"] = final_fix

    # --- Create Pull Request ---
    if not relevant_files:
        report["pr_url"] = None
        report["message"] = "No relevant files found; PR not created."
    else:
        pr_url = create_pull_request(
            repo_url,
            final_fix,
            relevant_files[0]  # Modify first relevant file
        )
        report["pull_request_url"] = pr_url

    return report


if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    issue_text = input("Describe the GitHub issue: ")
    result = solve_github_issue(repo_url, issue_text)
    print(result)
