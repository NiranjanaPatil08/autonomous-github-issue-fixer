from src.llm import llm


def review_fix(issue, proposed_fix):
    """
    Review the generated fix and improve it if needed.
    """

    prompt = f"""
You are a senior software engineer reviewing a proposed code fix.

GitHub Issue:
{issue}

Proposed Fix:
{proposed_fix}

Tasks:
1. Check if the fix actually solves the issue.
2. Identify mistakes or missing edge cases.
3. Improve the solution if needed.
4. Provide the final corrected fix.

Return the final improved solution.
"""

    response = llm.invoke(prompt)

    return response.content
