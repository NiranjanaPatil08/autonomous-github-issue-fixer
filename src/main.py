from src.rag.repo_loader import clone_repo
from src.rag.file_loader import list_repo_files, load_selected_files
from src.rag.chunker import chunk_documents
from src.rag.vector_store import build_vector_store
from src.rag.retriever import get_relevant_chunks
from src.agents.issue_classifier import classify_issue
from src.agents.research_agent import research_issue
from src.agents.fix_generator_agent import generate_fix
from src.agents.reviewer_agent import review_fix
from src.agents.file_finder_agent import find_relevant_files

def solve_github_issue(repo_url, issue):
    """
    Returns a report containing:
    - llm_reasoning: Full LLM text output exactly as received
    - final_fix: Corrected code only (for PR, not shown on website)
    - pull_request_file: file path to be modified
    """
    report = {}

    # 1. Classify Issue
    classification = classify_issue(issue)
    if classification != "BUG":
        report["llm_reasoning"] = f"Issue classified as: {classification}. No code fix required."
        report["final_fix"] = None
        report["pull_request_file"] = None
        return report

    # 2. Clone repository
    repo_path = clone_repo(repo_url)

    # 3. List repo files
    repo_files = list_repo_files(repo_path)

    # 4. Find relevant files
    relevant_files = find_relevant_files(issue, repo_files)

    # 5. Load files
    files = load_selected_files(relevant_files, repo_path)
    if not files:
        files = load_selected_files(repo_files[:10], repo_path)

    # 6. Chunk files
    chunks = chunk_documents(files)

    # 7. Build vector store
    vectorstore = build_vector_store(chunks)

    # 8. Research issue
    keywords = research_issue(issue)

    # 9. Retrieve relevant code
    docs = get_relevant_chunks(vectorstore, keywords)

    # 10. Generate fix
    fix_response = generate_fix(issue, docs)

    # 11. Review fix
    review_response = review_fix(issue, fix_response.get("code", ""))

    # 12. Combine full LLM reasoning
    report["llm_reasoning"] = fix_response.get("reasoning", "") + "\n\n" + review_response.get("reasoning", "")

    # 13. Prepare final corrected code for PR
    report["final_fix"] = review_response.get("code", "")

    # 14. Determine file for pull request
    report["pull_request_file"] = relevant_files[0] if relevant_files else repo_files[0]

    return report
