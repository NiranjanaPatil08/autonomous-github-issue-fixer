from src.llm import llm
import re

def generate_fix(issue, retrieved_docs):
    """
    Generate a code fix using the issue description
    and relevant code retrieved from the repository.

    Returns a dict:
    {
        "reasoning": <full LLM text including explanation>,
        "code": <Python code snippet>
    }
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

Provide a clear explanation and the fixed code.
"""

    response = llm.invoke(prompt)
    full_text = response.content

    # Extract Python code blocks
    code_blocks = re.findall(r"```(?:python)?\n(.*?)```", full_text, re.DOTALL)
    code = "\n\n".join(code_blocks).strip()

    # Full reasoning = everything including text outside code blocks
    reasoning = full_text.strip()

    return {
        "reasoning": reasoning,
        "code": code
    }
