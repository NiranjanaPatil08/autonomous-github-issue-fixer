from src.llm import llm
import re
import json


def find_relevant_files(issue, repo_file_list):

    files_text = "\n".join(repo_file_list[:200])

    prompt = f"""
You are a senior software engineer.

Given a GitHub issue and a list of repository files,
identify the files most likely related to the issue.

Return ONLY a Python list of file paths.

Issue:
{issue}

Repository files:
{files_text}

Example output:
["requests/cookies.py", "requests/sessions.py"]
"""

    response = llm.invoke(prompt)

    text = response.content

    # Extract list from model output
    match = re.search(r"\[.*?\]", text, re.DOTALL)

    if match:
        try:
            files = json.loads(match.group())
            return files
        except:
            pass

    return []
