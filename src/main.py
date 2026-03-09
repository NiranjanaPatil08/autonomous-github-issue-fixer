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

# Define allowed code extensions for fallback
CODE_EXTENSIONS = [".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".go", ".rb"]

def filter_code_files(file_list):
    return [f for f in file_list if any(f.endswith(ext) for ext in CODE_EXTENSIONS)]

def solve_github_issue(repo_url, issue, fallback_file_count=10):
    print("\nClassifying issue...")
    classification = classify_issue(issue)
    print("Issue type:", classification)

    if classification != "BUG":
        return "This issue does not require a code fix."

    print("\nCloning repository...")
    repo_path = clone_repo(repo_url)

    print("\nListing repository files...")
    repo_files = list_repo_files(repo_path)

    print("\nFinding relevant files...")
    relevant_files = find_relevant_files(issue, repo_files)
    print("Relevant files:", relevant_files)

    print("\nLoading selected files...")
    files = load_selected_files(relevant_files, repo_path)

    # Fallback 1: if AI selection empty, pick first N code files from repo
    if not files:
        code_files = filter_code_files(repo_files)
        fallback_files = code_files[:fallback_file_count]
        print(f"Fallback: loading first {len(fallback_files)} code files from repo...")
        files = load_selected_files(fallback_files, repo_path)

    if not files:
        return "Error: No code files found to analyze."

    print("\nChunking files...")
    chunks = chunk_documents(files)

    # Fallback 2: if chunking fails, try fallback files if not already used
    if not chunks:
        print("Chunking failed, trying fallback files...")
        code_files = filter_code_files(repo_files)
        fallback_files = code_files[:fallback_file_count]
        files = load_selected_files(fallback_files, repo_path)
        chunks = chunk_documents(files)

        if not chunks:
            return "Error: Unable to create chunks from code files."

    print("\nBuilding vector database...")
    vectorstore = build_vector_store(chunks)

    print("\nAnalyzing issue...")
    keywords = research_issue(issue)

    print("\nRetrieving relevant code...")
    docs = get_relevant_chunks(vectorstore, keywords)

    print("\nGenerating fix...")
    fix = generate_fix(issue, docs)

    print("\nReviewing fix...")
    final_fix = review_fix(issue, fix)

    return final_fix


if __name__ == "__main__":
    repo_url = input("Enter GitHub repository URL: ")
    issue = input("Describe the GitHub issue: ")
    result = solve_github_issue(repo_url, issue)
    print("\nAI Suggested Fix:\n")
    print(result)
