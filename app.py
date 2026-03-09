import streamlit as st
from src.main import solve_github_issue
from src.tools.github_issue_fetcher import fetch_github_issue

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

            if "message" in report:
                st.info(report["message"])
            else:
                st.subheader("Issue Classification")
                st.write(report.get("classification"))

                st.subheader("Repository Path")
                st.write(report.get("repo_path"))

                st.subheader("Relevant Files")
                st.write(report.get("relevant_files"))

                st.subheader("Loaded Files")
                st.write(report.get("loaded_files"))

                st.subheader("Number of Code Chunks")
                st.write(report.get("num_chunks"))

                st.subheader("Research Keywords")
                st.write(report.get("research_keywords"))

                st.subheader("Generated Fix")
                st.code(report.get("generated_fix"), language="python")

                st.subheader("Reviewed Fix")
                st.code(report.get("reviewed_fix"), language="python")

                st.subheader("Pull Request URL")
                st.markdown(f"[View PR]({report.get('pull_request_url')})")

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")

    else:
        st.warning("Please enter repository URL and issue number.")
