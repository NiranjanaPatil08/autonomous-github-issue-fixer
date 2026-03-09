from src.llm import llm
import re

def review_fix(issue, proposed_fix):
    """
    Review the generated fix and improve it if needed.

    Returns a dict:
    {
        "reasoning": <reviewer explanation in English>,
        "code": <final reviewed Python code>
    }
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

Return a clear explanation and the final corrected code.
"""

    response = llm.invoke(prompt)
    full_text = response.content

    # Extract Python code blocks
    code_blocks = re.findall(r"```(?:python)?\n(.*?)```", full_text, re.DOTALL)
    code = "\n\n".join(code_blocks).strip()

    # Remove code blocks to get reasoning
    reasoning = re.sub(r"```(?:python)?\n.*?```", "", full_text, flags=re.DOTALL).strip()

    return {
        "reasoning": reasoning,
        "code": code
    }
