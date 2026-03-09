from src.llm import llm
import re

def generate_fix(issue, retrieved_docs):
    """
    Generate a code fix using the issue description and relevant code.
    Returns dict with reasoning (full LLM text) and code (for PR only).
    """
    code_context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    prompt = f"""
You are a senior software engineer.

A GitHub issue has been reported.

Issue:
{issue}

Relevant Code:
{code_context}

Task:
1. Understand the issue.
2. Identify the bug or problem.
3. Suggest a fix.
4. Show the corrected code snippet.

Provide full reasoning and the fixed code.
"""
    response = llm.invoke(prompt)
    full_text = response.content

    code_blocks = re.findall(r"```(?:python)?\n(.*?)```", full_text, re.DOTALL)
    code = "\n\n".join(code_blocks).strip()

    reasoning = full_text.strip()

    return {"reasoning": reasoning, "code": code}
