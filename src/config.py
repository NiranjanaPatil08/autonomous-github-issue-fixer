import streamlit as st
import os

# Use Streamlit Secrets first, fallback to local environment (for dev)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. "
        "Add it to Streamlit secrets or your local environment."
    )

# Optional: print to confirm (only for local dev, remove for production)
if os.getenv("STREAMLIT_SERVER") is None:
    print("GROQ_API_KEY loaded successfully.")
