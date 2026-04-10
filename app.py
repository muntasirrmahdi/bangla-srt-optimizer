import streamlit as st
import pysrt
import google.generativeai as genai
import os
import re
import json

# Security: Load API Key from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Missing GEMINI_API_KEY environment variable. Please set it and restart.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3-flash-preview")

st.set_page_config(layout="wide")

st.title("Bangla SRT Optimizer")
st.markdown(
    "Upload your podcast subtitle file. AI will automatically correct spelling, pronunciation, and contextual errors while strictly maintaining timestamps."
)

uploaded_file = st.file_uploader("Upload your SRT file here", type="srt")

# Load fixes from config file (Your 'Special Sauce')
RULES_PATH = os.path.join(os.path.dirname(__file__), "config", "rules.json")
if os.path.exists(RULES_PATH):
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        SPECIFIC_BENGALI_FIXES = json.load(f)
else:
    SPECIFIC_BENGALI_FIXES = []

SPECIFIC_BENGALI_FIXES.sort(key=lambda x: len(x[0]), reverse=True)


def apply_hardcoded_fixes(text: str) -> str:
    for wrong, correct in SPECIFIC_BENGALI_FIXES:
        text = text.replace(wrong, correct)

    text = re.sub(r"  +", " ", text)
    text = re.sub(r" [,।]", lambda m: m.group(0).strip(), text)
    return text.strip()


def get_ai_corrected_text(segments: list[str]) -> list[str]:
    original_text = "\n".join([f"SEG_{j + 1}: {s}" for j, s in enumerate(segments)])

    prompt = f"""
    You are an expert Bengali podcast editor. Your task is to accurately correct the following script segments.
    
    Correction Rules:
    - Provide exactly one corrected line for each input line.
    - The output format MUST be 'SEG_number: corrected text'.
    - Correct spelling and pronunciation errors (e.g., উট -> উড, তিতা দি -> ইত্যাদি, মাঠায় -> মাথায়)।
    - Do not skip or merge any lines. There must be exactly {len(segments)} lines in the output.

    Input Segments:
    {original_text}
    """

    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split("\n")

        corrected_dict = {}
        for line in lines:
            match = re.match(r"SEG_(\d+):\s*(.*)", line.strip())
            if match:
                idx = int(match.group(1)) - 1
                corrected_dict[idx] = match.group(2)

        result = []
        for i in range(len(segments)):
            result.append(corrected_dict.get(i, segments[i]))

        if len(corrected_dict) != len(segments):
            st.warning(
                f"Received {len(corrected_dict)} out of {len(segments)} lines from AI. Missing lines were kept unchanged."
            )

        return result
    except Exception as e:
        st.error(f"Error fetching corrected text from AI: {e}")
        return segments


if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    subs = pysrt.from_string(content)

    st.write(f"Total subtitle blocks: {len(subs)}")

    if st.button("Process and Correct Subtitles"):
        progress_bar = st.progress(0)
        batch_size = 20
        corrected_subs = []
        for i in range(0, len(subs), batch_size):
            batch = subs[i : i + batch_size]
            text_segments = [s.text for s in batch]

            ai_contextual_corrected_segments = get_ai_corrected_text(text_segments)

            final_validated_segments = [
                apply_hardcoded_fixes(s_text)
                for s_text in ai_contextual_corrected_segments
            ]

            for j, s_obj in enumerate(batch):
                if j < len(final_validated_segments):
                    s_obj.text = final_validated_segments[j]

            corrected_subs.extend(batch)
            progress = min(1.0, (i + batch_size) / len(subs))
            progress_bar.progress(progress)

        new_filename = "optimized_" + uploaded_file.name
        temp_filepath = os.path.join("/tmp", new_filename)

        for idx, s_obj in enumerate(corrected_subs):
            s_obj.index = idx + 1

        pysrt.SubRipFile(corrected_subs).save(temp_filepath, encoding="utf-8")

        st.success("Correction complete! Download the file using the button below.")
        with open(temp_filepath, "rb") as file:
            st.download_button(
                label="Download Optimized SRT",
                data=file,
                file_name=new_filename,
                mime="text/plain",
            )

        st.subheader("Corrected Subtitle Samples:")
        sample_count = 5
        for i in range(min(sample_count, len(corrected_subs))):
            st.write(f"**Original {subs[i].index}:** {subs[i].text}")
            st.write(
                f"**Corrected {corrected_subs[i].index}:** {corrected_subs[i].text}"
            )
            st.write("---")
