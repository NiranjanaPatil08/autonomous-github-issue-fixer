from src.llm import llm

def review_fix(issue, proposed_code):
    """
    Review the generated fix and improve it if needed.

    Returns:
    {
        "reasoning": <LLM review explanation>,
        "code": <final Python code>
    }
    """
    prompt = f"""
You are a senior software engineer reviewing a proposed code fix.

GitHub Issue:
{issue}

Proposed Fix:
{proposed_code}

Tasks:
1. Verify correctness.
2. Identify mistakes or edge cases.
3. Improve the solution if needed.
4. Provide only the final corrected Python code.

Return your explanation and final code.
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
        code = proposed_code  # fallback

    return {"reasoning": reasoning, "code": code}
