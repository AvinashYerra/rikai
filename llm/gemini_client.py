from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Check for both possible API key names for flexibility
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-3-flash-preview"