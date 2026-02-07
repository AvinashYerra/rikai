from google.generativeai import GenerativeModel

model = GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.2,
        "response_mime_type": "application/json"
    }
)
