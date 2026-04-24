from google import genai
from google.genai import types
from google.genai.errors import APIError
import os
import re
import time
import streamlit as st

def get_ai_model():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    
    try:
        client = genai.Client(api_key=key)
        return client
    except Exception as e:
        st.error(f"Failed to initialize Gemini Client: {e}")
        return None

def get_ai_corrected_text(segments: list[str], client, max_retries=3) -> list[str]:
    """Sends text segments to Gemini for AI-driven correction with retry logic."""
    original_text = "\n".join([f"SEG_{j + 1}: {s}" for j, s in enumerate(segments)])

    prompt = f"""
    You are an expert Bengali podcast editor. Your task is to accurately correct the following script segments.
    
    Correction Rules:
    - Provide exactly one corrected line for each input line.
    - The output format MUST be 'SEG_number: corrected text'.
    - Correct spelling and pronunciation errors (e.g., উট -> উড, তিতা দি -> ইত্যাদি, মাঠায় -> মাথায়).
    - Do not skip or merge any lines. There must be exactly {len(segments)} lines in the output.

    Input Segments:
    {original_text}
    """

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            
            lines = response.text.strip().split("\n")

            corrected_dict = {}
            for line in lines:
                match = re.match(r"SEG_(\d+):\s*(.*)", line.strip())
                if match:
                    idx = int(match.group(1)) - 1
                    corrected_dict[idx] = match.group(2)

            # Reconstruct list based on original order
            result = []
            for i in range(len(segments)):
                result.append(corrected_dict.get(i, segments[i]))
            
            return result
        except APIError as e:
            if "429" in str(e) or attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise e
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)  # Exponential backoff
            
    return segments
