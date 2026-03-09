import streamlit as st
from src.main import solve_github_issue
from src.tools.github_issue_fetcher import fetch_github_issue
import re

st.set_page_config(page_title="Autonomous GitHub Issue Fixer", page_icon="🤖")
st.title("🤖 Autonomous GitHub Issue Fixer")
st.write(
    "An AI multi-agent system that analyzes GitHub issues, finds relevant code, "
    "generates fixes, and automatically creates pull requests."
)

repo_url = st.text_input("GitHub Repository URL")
issue_number = st.text_input("GitHub Issue Number")

if st.button("Solve Issue"):
    if repo_url and issue_number:
        try:
            with st.spinner("Fetching issue from GitHub..."):
                issue_text = fetch_github_issue(repo_url, issue_number)

            st.subheader("Fetched Issue")
            st.write(issue_text)

            with st.spinner("Analyzing repository and generating fix..."):
                llm_output = solve_github_issue(repo_url, issue_text)

            st.subheader("AI Reasoning + Fix")

            # Preserve multi-line code blocks as-is
            # If LLM output has backticks, leave them. Otherwise, detect code and wrap manually.
            code_block_pattern = r"(```[\s\S]*?```)"
            parts = re.split(code_block_pattern, llm_output)

            for part in parts:
                if part.startswith("```"):
                    # Render code block properly
                    st.code(part.strip("```"), language="javascript")  # or "python" depending
                else:
                    # Render normal text
                    st.markdown(part)

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")

    else:
        st.warning("Please enter repository URL and issue number.")
