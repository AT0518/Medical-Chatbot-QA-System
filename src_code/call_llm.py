import os

from src_code.env import load_project_env

load_project_env()

from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set.")

client = genai.Client(api_key=GEMINI_API_KEY)
    
def ask_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text

    