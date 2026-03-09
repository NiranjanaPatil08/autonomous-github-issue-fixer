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
    Returns a structured report containing:
    - steps: list of reasoning steps (title + description)
    - final_fix: Python code only
    - pull_request_file: file path to be modified
    """
    report = {"steps": []}

    # 1. Classify Issue
    classification = classify_issue(issue)
    report["steps"].append({
        "title": "Classify Issue",
        "description": f"Issue classified as: {classification}"
    })
    if classification != "BUG":
        report["final_fix"] = None
        report["pull_request_file"] = None
        report["steps"].append({
            "title": "Decision",
            "description": "No code fix required for non-bug issue."
        })
        return report

    # 2. Clone repository
    repo_path = clone_repo(repo_url)
    report["steps"].append({
        "title": "Clone Repository",
        "description": f"Repository cloned to: {repo_path}"
    })

    # 3. List repo files
    repo_files = list_repo_files(repo_path)
    report["steps"].append({
        "title": "List Repository Files",
        "description": f"Found {len(repo_files)} files."
    })

    # 4. Find relevant files
    relevant_files = find_relevant_files(issue, repo_files)
    report["steps"].append({
        "title": "Find Relevant Files",
        "description": f"Files selected by AI: {relevant_files}"
    })

    # 5. Load files
    files = load_selected_files(relevant_files, repo_path)
    if not files:
        files = load_selected_files(repo_files[:10], repo_path)
        report["steps"].append({
            "title": "Fallback File Loading",
            "description": "No files loaded from AI selection. Using first 10 repo files."
        })
    else:
        report["steps"].append({
            "title": "Load Selected Files",
            "description": f"{len(files)} files loaded successfully."
        })

    # 6. Chunk files
    chunks = chunk_documents(files)
    if not chunks:
        report["final_fix"] = None
        report["pull_request_file"] = None
        report["steps"].append({
            "title": "Chunking",
            "description": "Error: No code chunks could be created."
        })
        return report
    report["steps"].append({
        "title": "Chunk Documents",
        "description": f"Created {len(chunks)} code chunks for analysis."
    })

    # 7. Build vector store
    vectorstore = build_vector_store(chunks)
    report["steps"].append({
        "title": "Build Vector Database",
        "description": "Vector database created from code chunks."
    })

    # 8. Research issue
    keywords = research_issue(issue)
    report["steps"].append({
        "title": "Research Issue",
        "description": f"Keywords extracted: {keywords}"
    })

    # 9. Retrieve relevant code
    docs = get_relevant_chunks(vectorstore, keywords)
    report["steps"].append({
        "title": "Retrieve Relevant Code",
        "description": f"{len(docs)} relevant code chunks retrieved."
    })

    # 10. Generate fix
    fix_response = generate_fix(issue, docs)
    report["steps"].append({
        "title": "Generate Fix",
        "description": fix_response.get("reasoning", "AI-generated reasoning not available.")
    })
    fix_code = fix_response.get("code", "")

    # 11. Review fix
    review_response = review_fix(issue, fix_code)
    report["steps"].append({
        "title": "Review Fix",
        "description": review_response.get("reasoning", "AI review reasoning not available.")
    })
    final_fix_code = review_response.get("code", "")

    # 12. Prepare pull request
    pull_request_file = relevant_files[0] if relevant_files else repo_files[0]
    report["final_fix"] = final_fix_code
    report["pull_request_file"] = pull_request_file

    return report
