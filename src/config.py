from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env from project root
project_root = Path(__file__).resolve().parent.parent
dotenv_path = project_root / ".env"

if not dotenv_path.exists():
    raise FileNotFoundError(f".env file not found at {dotenv_path}")

load_dotenv(dotenv_path=dotenv_path)

# Get the API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# Optional: print to confirm
print("GROQ_API_KEY loaded successfully.")
