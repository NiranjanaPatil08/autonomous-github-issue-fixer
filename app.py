import streamlit as st
from src.main import solve_github_issue
from src.tools.github_issue_fetcher import fetch_github_issue

# --- Page config ---
st.set_page_config(
    page_title="Autonomous GitHub Issue Fixer",
    page_icon="🤖",
    layout="centered",
)

# --- Custom CSS ---
st.markdown("""
<style>
/* Page background */
body {
    background-color: #f8f9fa;
}

/* Card container for content */
.card {
    background-color: #ffffff;
    padding: 20px 25px;
    border-radius: 12px;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.08);
    margin-bottom: 20px;
}

/* Section titles */
h1, h2, h3, h4 {
    font-family: 'Segoe UI', sans-serif;
}

/* Code block styling */
.stMarkdown code {
    background-color: #f1f3f6;
    color: #0b0b0b;
    padding: 2px 4px;
    border-radius: 4px;
    font-family: 'Fira Code', monospace;
}

/* Text area for long outputs */
.stTextArea textarea {
    font-family: 'Fira Code', monospace;
}

/* Buttons */
.stButton>button {
    background-color: #4B6CF7;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 8px 16px;
}

.stButton>button:hover {
    background-color: #3A50D0;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="card"><h1>🤖 Autonomous GitHub Issue Fixer</h1></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="card">'
    'An AI multi-agent system that analyzes GitHub issues, finds relevant code, '
    'generates fixes, and displays reasoning exactly as provided by the model.'
    '</div>',
    unsafe_allow_html=True
)

# --- Inputs ---
repo_url = st.text_input("GitHub Repository URL")
issue_number = st.text_input("GitHub Issue Number")

# --- Solve button ---
if st.button("Solve Issue"):
    if repo_url and issue_number:
        try:
            with st.spinner("Fetching issue from GitHub..."):
                issue_text = fetch_github_issue(repo_url, issue_number)

            st.markdown(f'<div class="card"><h3>Fetched Issue</h3><p>{issue_text}</p></div>', unsafe_allow_html=True)

            with st.spinner("Analyzing repository and generating fix..."):
                llm_output = solve_github_issue(repo_url, issue_text)

            st.markdown('<div class="card"><h3>AI Reasoning + Fix</h3></div>', unsafe_allow_html=True)

            # Safely handle backticks in LLM output
            safe_output = llm_output.replace("```", "´´´")

            # Display full reasoning with preserved formatting
            st.markdown(f'<div class="card">{safe_output}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
    else:
        st.warning("Please enter repository URL and issue number.")
