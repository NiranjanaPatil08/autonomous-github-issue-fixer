from .config import GROQ_API_KEY
from .llm import llm

# Check that API key is loaded
print("GROQ_API_KEY:", GROQ_API_KEY)

# Test the LLM
response = llm.invoke("Explain what Retrieval Augmented Generation (RAG) is in 3 simple sentences.")
print("LLM Response:\n", response)
