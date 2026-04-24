import google.generativeai as genai
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Please set GEMINI_API_KEY environment variable")
    exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

print("Available Models:")
for model in client.models.list():
    print(f"- {model.name}")
