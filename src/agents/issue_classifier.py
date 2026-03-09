from src.llm import llm


def classify_issue(issue_text):

    prompt = f"""
You are a software engineer.

Determine if this GitHub issue is a **bug that requires a code fix**.

Issue:
{issue_text}

Answer ONLY with one word:

BUG
or
NOT_BUG
"""

    response = llm.invoke(prompt)

    return response.content.strip()
