from src.llm import llm


def generate_fix(issue, retrieved_docs):
    """
    Generate a code fix using the issue description
    and relevant code retrieved from the repository.
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
5. Explain the changes made and why they are required
6. List changes made and which files were targeted

Provide a clear explanation and the fixed code.
"""

    response = llm.invoke(prompt)

    return response.content
