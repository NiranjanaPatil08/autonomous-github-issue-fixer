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

def solve_github_issue(repo_url, issue_text):
    """
    Returns a detailed, step-by-step structured report for Streamlit display.
    """
    report = {
        "steps": [],  # each element: {"title": str, "description": str, "details": dict}
        "final_fix": None,
        "pull_request_url": None
    }

    # --- Step 1: Classify Issue ---
    classification = classify_issue(issue_text)
    report["steps"].append({
        "title": "Issue Classification",
        "description": f"The issue was classified as: **{classification}**.",
        "details": {}
    })
    if classification != "BUG":
        report["steps"].append({
            "title": "No Code Fix Required",
            "description": "This issue does not require a code fix.",
            "details": {}
        })
        return report

    # --- Step 2: Clone Repository ---
    repo_path = clone_repo(repo_url)
    report["steps"].append({
        "title": "Repository Cloning",
        "description": f"Repository cloned to: `{repo_path}`",
        "details": {}
    })

    # --- Step 3: List and Select Files ---
    all_files = list_repo_files(repo_path)
    relevant_files = find_relevant_files(issue_text, all_files)
    fallback_used = False
    if not relevant_files:
        relevant_files = all_files[:10]
        fallback_used = True
    loaded_files = load_selected_files(relevant_files, repo_path)
    report["steps"].append({
        "title": "File Selection",
        "description": f"Selected {len(loaded_files)} relevant files.",
        "details": {
            "relevant_files": relevant_files,
            "fallback_used": fallback_used
        }
    })

    # --- Step 4: Chunk Documents ---
    chunks = chunk_documents(loaded_files)
    report["steps"].append({
        "title": "Document Chunking",
        "description": f"Created {len(chunks)} chunks for vector search.",
        "details": {}
    })
    if not chunks:
        report["steps"].append({
            "title": "Error",
            "description": "No code chunks could be created.",
            "details": {}
        })
        return report

    # --- Step 5: Build Vector Store ---
    vectorstore = build_vector_store(chunks)
    report["steps"].append({
        "title": "Vector Database",
        "description": "Vector store built successfully for semantic search.",
        "details": {}
    })

    # --- Step 6: Research Issue ---
    keywords = research_issue(issue_text)
    report["steps"].append({
        "title": "Issue Research / LLM Analysis",
        "description": "Keywords and insights extracted from the issue:",
        "details": {"keywords": keywords}
    })

    # --- Step 7: Retrieve Relevant Chunks ---
    docs = get_relevant_chunks(vectorstore, keywords)
    report["steps"].append({
        "title": "Retrieve Relevant Code Chunks",
        "description": f"{len(docs)} relevant code chunks retrieved for fix generation.",
        "details": {}
    })

    # --- Step 8: Generate Fix ---
    fix = generate_fix(issue_text, docs)
    llm_reasoning = getattr(fix, "reasoning", "No reasoning available")
    fix_code = "\n".join(fix) if isinstance(fix, list) else fix
    report["steps"].append({
        "title": "LLM Suggested Fix",
        "description": llm_reasoning,
        "details": {"generated_fix": fix_code}
    })

    # --- Step 9: Review Fix ---
    final_fix = review_fix(issue_text, fix)
    final_fix_code = "\n".join(final_fix) if isinstance(final_fix, list) else final_fix
    report["final_fix"] = final_fix_code
    report["steps"].append({
        "title": "Reviewed Fix",
        "description": "Final fix after review.",
        "details": {"reviewed_fix": final_fix_code}
    })

    # --- Step 10: Create Pull Request ---
    if relevant_files:
        pr_url = create_pull_request(repo_url, final_fix, relevant_files[0])
        report["pull_request_url"] = pr_url
        report["steps"].append({
            "title": "Pull Request Created",
            "description": f"PR created successfully: [View PR]({pr_url})",
            "details": {}
        })
    else:
        report["steps"].append({
            "title": "PR Not Created",
            "description": "No relevant files found; PR was not created.",
            "details": {}
        })

    return report


if __name__ == "__main__":

    repo_url = input("Enter GitHub repository URL: ")

    issue = input("Describe the GitHub issue: ")

    solve_github_issue(repo_url, issue)



