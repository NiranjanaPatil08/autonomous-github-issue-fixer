import streamlit as st
from src.main import solve_github_issue
from src.tools.github_issue_fetcher import fetch_github_issue


st.title("AI GitHub Issue Solver")

repo_url = st.text_input("GitHub Repository URL")

issue_number = st.text_input("GitHub Issue Number")

if st.button("Solve Issue"):

    if repo_url and issue_number:

        with st.spinner("Fetching issue from GitHub..."):

            issue_text = fetch_github_issue(repo_url, issue_number)

        st.subheader("Fetched Issue")
        st.write(issue_text)

        with st.spinner("Analyzing repository and generating fix..."):

            result = solve_github_issue(repo_url, issue_text)

        st.subheader("AI Suggested Fix")
        st.write(result)

    else:
        st.warning("Please enter repository URL and issue number.")
