from src.llm import llm

def generate_fix(issue, retrieved_docs):
    """
    Generate a code fix using the issue description
    and relevant code retrieved from the repository.

    Returns:
    {
        "reasoning": <full LLM reasoning>,
        "code": <Python code snippet>
    }
    """
    code_context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    prompt = f"""
You are a senior software engineer.

GitHub Issue:
{issue}

Relevant Code:
{code_context}

Task:
1. Understand the issue.
2. Identify the bug or problem.
3. Suggest a fix.
4. Provide a full explanation in English followed by the corrected Python code.

Return your full reasoning and Python code.
"""
    response = llm.invoke(prompt)
    full_text = response.content

    # Split reasoning vs code (keep reasoning intact)
    code_start = full_text.find("```")
    if code_start != -1:
        reasoning = full_text[:code_start].strip()
        code = full_text[code_start:].strip("```").strip()
    else:
        reasoning = full_text
        code = ""

    return {"reasoning": reasoning, "code": code}
