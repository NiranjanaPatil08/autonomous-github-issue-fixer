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

            # Step-by-step reasoning display
            st.subheader("Step-by-Step Reasoning")
            for step in report.get("steps", []):
                with st.expander(step["title"]):
                    st.write(step["description"])
                    if step.get("details"):
                        st.json(step["details"])

            # Final code fix display
            if report.get("final_fix"):
                st.subheader("Final Reviewed Fix")
                st.code(report["final_fix"], language="python")

            # Create PR and show link
            if report.get("final_fix") and report.get("pull_request_file"):
                from src.agents.pr_agent import create_pull_request

                pr_url = create_pull_request(
                    repo_url,
                    fix_code=report["final_fix"],
                    file_path=report["pull_request_file"],
                    reasoning_steps=report.get("steps")
                )

                st.subheader("Pull Request")
                st.markdown(f"[View PR]({pr_url})")

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
    else:
        st.warning("Please enter repository URL and issue number.")
