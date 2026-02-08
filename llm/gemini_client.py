import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel
import google.generativeai as genai

load_dotenv()  # <-- loads .env

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.2,
        "response_mime_type": "application/json"
    }
)
