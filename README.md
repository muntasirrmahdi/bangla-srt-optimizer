# Bangla SRT Optimizer

An AI-powered tool to optimize and correct Bengali subtitle (SRT) files while maintaining 100% timestamp accuracy.

## Features
- **Contextual AI Correction**: Uses Google Gemini to fix spelling, phonetic errors, and grammatical flow.
- **1:1 Timestamp Mapping**: Uses a proprietary segment tagging system to ensure zero timestamp drift.
- **Custom Rule Support**: Hardcoded replacement rules for consistent terminology (e.g., industry-specific terms).

## Setup
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set your Gemini API Key: `export GEMINI_API_KEY='your_api_key_here'`
6. Run the app: `streamlit run app.py`

## Configuration
Add your specific replacement rules to `config/rules.json` in the following format:
\`\`\`json
[
    ["wrong_word", "correct_word"],
    ["phonetic_error", "actual_meaning"]
]
\`\`\`
