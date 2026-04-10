import google.generativeai as genai
import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Please set GEMINI_API_KEY environment variable")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

print("Available models:")
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)
