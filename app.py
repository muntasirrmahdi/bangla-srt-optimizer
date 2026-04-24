import streamlit as st
import pysrt
import os
import time
from dotenv import load_dotenv
from core.ai import get_ai_model, get_ai_corrected_text
from core.processor import load_rules, apply_hardcoded_fixes, validate_srt

load_dotenv()

RULES_PATH = os.path.join(os.path.dirname(__file__), "config", "rules.json")
BATCH_SIZE = 20

st.set_page_config(page_title="Bangla SRT Optimizer", layout="wide")

st.title("Bangla SRT Optimizer")
st.markdown(
    "Professional AI-powered tool to optimize Bengali subtitle files. Corrects spelling, pronunciation, and contextual errors while maintaining 100% timestamp integrity."
)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    batch_size = st.slider("Batch Size", min_value=5, max_value=50, value=BATCH_SIZE)
    st.info("Larger batches are faster but might lose AI context.")
    
    st.divider()
    api_key_input = st.text_input("Gemini API Key (Optional if in .env)", type="password")

# Initialize Model
if api_key_input:
    os.environ["GEMINI_API_KEY"] = api_key_input

model = get_ai_model()
if not model:
    st.error("⚠️ GEMINI_API_KEY not found. Please provide it in the sidebar or .env file.")
    st.stop()

uploaded_file = st.file_uploader("Upload your SRT file", type="srt")

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    subs = pysrt.from_string(content)
    
    is_valid, msg = validate_srt(subs)
    if not is_valid:
        st.error(msg)
        st.stop()

    st.success(f"Successfully loaded {len(subs)} subtitle blocks.")

    if st.button("Process & Optimize Subtitles"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Load rules
        rules = load_rules(RULES_PATH)
        
        corrected_subs = []
        total_batches = (len(subs) + batch_size - 1) // batch_size

        for i in range(0, len(subs), batch_size):
            current_batch_num = i // batch_size + 1
            status_text.text(f"Processing batch {current_batch_num}/{total_batches}...")
            
            batch = subs[i : i + batch_size]
            text_segments = [s.text for s in batch]

            try:
                # 1. AI Contextual Correction
                ai_corrected = get_ai_corrected_text(text_segments, model)

                # 2. Final Hardcoded Polish (Overrides AI hallucinations)
                final_segments = [
                    apply_hardcoded_fixes(s_text, rules)
                    for s_text in ai_corrected
                ]

                for j, s_obj in enumerate(batch):
                    if j < len(final_segments):
                        s_obj.text = final_segments[j]

                corrected_subs.extend(batch)
                time.sleep(2)
            except Exception as e:
                st.error(f"Error in batch {current_batch_num}: {e}")
                # Fallback to original for this batch
                corrected_subs.extend(batch)

            progress = min(1.0, (i + batch_size) / len(subs))
            progress_bar.progress(progress)

        status_text.text("Optimization complete!")
        
        new_filename = f"optimized_{uploaded_file.name}"
        srt_content = "\n".join([str(sub) for sub in corrected_subs])

        st.divider()
        st.success("🎉 Processed successfully! Click below to download.")
        st.download_button(
            label="📥 Download Optimized SRT",
            data=srt_content,
            file_name=new_filename,
            mime="text/plain",
        )

        st.subheader("👀 Preview (First 5 Blocks)")
        for i in range(min(5, len(corrected_subs))):
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"Original {i+1}")
                st.text(subs[i].text)
            with col2:
                st.caption(f"Optimized {i+1}")
                st.text(corrected_subs[i].text)
