from src.llm import llm


def research_issue(issue):
    """
    Analyze the issue and extract important search keywords.
    """

    prompt = f"""
You are a software engineer analyzing a GitHub issue.

Issue:
{issue}

Extract important technical keywords that should be searched
in the repository to find relevant code.

Return them as a short list.
"""

    response = llm.invoke(prompt)

    return response.content
