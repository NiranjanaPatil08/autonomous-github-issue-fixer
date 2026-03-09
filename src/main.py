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
from src.agents.pr_agent import create_pull_request

def solve_github_issue(repo_url, issue):
    """
    Returns:
    - llm_reasoning: full reasoning from the LLM
    - final_fix: Python code only
    - pull_request_url: PR URL if created
    """
    report = {}

    # Classify issue
    classification = classify_issue(issue)
    if classification != "BUG":
        report["llm_reasoning"] = f"Issue classified as {classification}. No fix required."
        report["final_fix"] = None
        report["pull_request_url"] = None
        return report

    # Clone repo and find files
    repo_path = clone_repo(repo_url)
    repo_files = list_repo_files(repo_path)
    relevant_files = find_relevant_files(issue, repo_files)
    files = load_selected_files(relevant_files, repo_path)
    if not files:
        files = load_selected_files(repo_files[:10], repo_path)

    # Chunk, vector store, and retrieval
    chunks = chunk_documents(files)
    vectorstore = build_vector_store(chunks)
    keywords = research_issue(issue)
    docs = get_relevant_chunks(vectorstore, keywords)

    # Generate fix
    fix_response = generate_fix(issue, docs)
    final_code = review_fix(issue, fix_response["code"])["code"]

    # Store reasoning
    report["llm_reasoning"] = fix_response["reasoning"]
    report["final_fix"] = final_code

    # Optionally create pull request (PR contains only final code)
    if relevant_files:
        pr_url = create_pull_request(repo_url, final_code, relevant_files[0])
        report["pull_request_url"] = pr_url
    else:
        report["pull_request_url"] = None

    return report
