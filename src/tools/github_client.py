import os
from dotenv import load_dotenv
from github import Github

# Load .env
load_dotenv()
GITHUB_PAT = os.getenv("GITHUB_PAT")

if not GITHUB_PAT:
    raise ValueError("GITHUB_PAT not found in .env")

# Initialize GitHub client
github_client = Github(GITHUB_PAT)
