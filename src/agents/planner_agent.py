from src.llm import llm
import json

def plan_issue(issue_title, issue_body):
    """
    Takes a GitHub issue (title + body) and returns a structured plan.
    """
    prompt = f"""
You are an expert software engineer AI assistant.

Read the following GitHub issue and create a step-by-step plan to fix it.

Title: {issue_title}
Description: {issue_body}

Output a valid JSON with keys:
- research_needed: true if additional research on the repo is needed, false otherwise
- target_files: list of files that might be relevant for the fix
- action: short string describing the main action (e.g., "generate_fix", "refactor", "add_test")

Make sure the output is valid JSON only.
"""
    response = llm.invoke(prompt)
    
    # Try parsing JSON safely
    try:
        plan = json.loads(response.content)
    except json.JSONDecodeError:
        # fallback if LLM output is not strict JSON
        plan = {"raw_output": response.content}
    
    return plan
