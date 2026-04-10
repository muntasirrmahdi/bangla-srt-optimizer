# Bangla SRT Optimizer

An AI-powered professional tool to optimize and correct Bengali subtitle (SRT) files. Built with Python, Streamlit, and Google Gemini.

[![GitHub license](https://img.shields.io/github/license/muntasirrmahdi/bangla-srt-optimizer)](https://github.com/muntasirrmahdi/bangla-srt-optimizer/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/muntasirrmahdi/bangla-srt-optimizer)](https://github.com/muntasirrmahdi/bangla-srt-optimizer/stargazers)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

##  The Problem
Manual correction of Bengali podcast subtitles can take 3-4 hours per episode due to phonetic errors, spelling mistakes, and contextual nuances (e.g., "উট" vs "উড"). This tool reduces that work to minutes while ensuring 100% timestamp integrity.

##  Features
- **Contextual Intelligence**: Detects and fixes industry-specific terms (e.g., Furniture/Metal industry context).
- **1:1 Timestamp Mapping**: Proprietary segment tagging (`SEG_n`) prevents AI from merging lines, ensuring zero drift.
- **Hybrid Correction Engine**: Combines hardcoded linguistic rules with LLM reasoning for maximum accuracy.
- **Privacy-First**: Your proprietary correction rules can be kept locally while using the shared engine.

##  Quick Start

### 1. Setup Environment
```bash
git clone https://github.com/muntasirrmahdi/bangla-srt-optimizer.git
cd bangla-srt-optimizer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Secrets
Create a `.env` file from the template:
```bash
cp .env.example .env
```
Edit `.env` and add your `GEMINI_API_KEY` from [Google AI Studio](https://aistudio.google.com/).

### 3. Run the App
```bash
streamlit run app.py
```

##  Configuration
Customize the correction logic in `config/rules.json`:
```json
[
    ["wrong_word", "correct_word"],
    ["phonetic_mistake", "intended_meaning"]
]
```
*Note: A `rules_sample.json` is provided as a starting point.*

##  Contributing
Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

##  License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Built by [Muntasir Mahdi](https://learnwithmuntasir.com)
