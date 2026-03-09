import streamlit as st
from src.main import solve_github_issue
from src.tools.github_issue_fetcher import fetch_github_issue

st.set_page_config(page_title="Autonomous GitHub Issue Fixer", page_icon="🤖")
st.title("🤖 Autonomous GitHub Issue Fixer")
st.write(
    "An AI multi-agent system that analyzes GitHub issues, finds relevant code and "
    "generates fixes."
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

            # Split output into lines to preserve formatting
            lines = llm_output.splitlines()

            formatted_output = ""
            in_code_block = False

            for line in lines:
                # Detect code lines (simple heuristic)
                if line.strip().startswith("def ") or line.strip().startswith("class ") or line.strip().startswith("import ") or line.strip().endswith(":"):
                    if not in_code_block:
                        formatted_output += "```python\n"
                        in_code_block = True
                    formatted_output += line + "\n"
                else:
                    if in_code_block:
                        formatted_output += "```\n"
                        in_code_block = False
                    formatted_output += line + "\n"

            # Close any unclosed code block
            if in_code_block:
                formatted_output += "```\n"

            st.markdown(formatted_output, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")

    else:
        st.warning("Please enter repository URL and issue number.")
