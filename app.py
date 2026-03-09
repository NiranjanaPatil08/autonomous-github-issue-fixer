import streamlit as st
from src.main import solve_github_issue
from src.tools.github_issue_fetcher import fetch_github_issue
from urllib.parse import quote_plus

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
                report = solve_github_issue(repo_url, issue_text)

            # Show full LLM reasoning exactly as it comes
            # Show full LLM reasoning as-is
            st.subheader("AI Reasoning")
            st.text_area("LLM Full Reasoning", report.get("final_fix", ""), height=400)

           

            # Prepare pull request link with only final corrected code
            # final_code = report.get("final_fix", "")
           

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")

    else:
        st.warning("Please enter repository URL and issue number.")
