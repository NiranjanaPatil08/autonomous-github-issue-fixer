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
    report_steps = []

    # Step 1: Classify issue
    classification = classify_issue(issue_text)
    report_steps.append({
        "title": "Step 1: Classify Issue",
        "description": f"Issue type detected: **{classification}**"
    })

    if classification != "BUG":
        return {
            "steps": report_steps,
            "final_fix": None,
            "pull_request_url": None
        }

    # Step 2: Clone repository
    repo_path = clone_repo(repo_url)
    report_steps.append({
        "title": "Step 2: Clone Repository",
        "description": f"Repository cloned at `{repo_path}`"
    })

    # Step 3: List files
    repo_files = list_repo_files(repo_path)
    report_steps.append({
        "title": "Step 3: List Repository Files",
        "description": f"Total files found: {len(repo_files)}"
    })

    # Step 4: Find relevant files
    relevant_files = find_relevant_files(issue_text, repo_files)
    report_steps.append({
        "title": "Step 4: Find Relevant Files",
        "description": f"Relevant files: {relevant_files}"
    })

    # Step 5: Load files
    files = load_selected_files(relevant_files, repo_path)
    if not files:  # fallback
        files = load_selected_files(repo_files[:10], repo_path)
        report_steps.append({
            "title": "Step 5: Load Selected Files",
            "description": "Fallback used: first 10 repo files loaded",
        })
    else:
        report_steps.append({
            "title": "Step 5: Load Selected Files",
            "description": f"Loaded files: {[f['name'] for f in files]}"
        })

    # Step 6: Chunk files
    chunks = chunk_documents(files)
    report_steps.append({
        "title": "Step 6: Chunk Files",
        "description": f"Total chunks created: {len(chunks)}"
    })

    # Step 7: Build vector store
    vectorstore = build_vector_store(chunks)
    report_steps.append({
        "title": "Step 7: Build Vector Store",
        "description": "Vector database built for semantic search"
    })

    # Step 8: Research issue
    keywords = research_issue(issue_text)
    report_steps.append({
        "title": "Step 8: Research Issue",
        "description": f"Keywords extracted for relevant code retrieval: {keywords}"
    })

    # Step 9: Retrieve relevant code
    docs = get_relevant_chunks(vectorstore, keywords)
    report_steps.append({
        "title": "Step 9: Retrieve Relevant Code",
        "description": f"Number of relevant code chunks found: {len(docs)}"
    })

    # Step 10: Generate fix
    fix = generate_fix(issue_text, docs)
    report_steps.append({
        "title": "Step 10: Generate Fix",
        "description": "Initial AI-generated fix created"
    })

    # Step 11: Review fix
    final_fix = review_fix(issue_text, fix)
    report_steps.append({
        "title": "Step 11: Review Fix",
        "description": "Final fix reviewed and improved by AI"
    })

    # Step 12: Create PR (code only)
    pr_url = create_pull_request(repo_url, final_fix, relevant_files[0])
    report_steps.append({
        "title": "Step 12: Create Pull Request",
        "description": f"Pull request created at [PR link]({pr_url})"
    })

    return {
        "steps": report_steps,         # For browser reasoning display
        "final_fix": final_fix,        # Only code for PR
        "pull_request_url": pr_url     # GitHub PR link
    }
