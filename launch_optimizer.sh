#!/bin/bash
# Load key from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

cd "/home/moon/Projects/Bangla_SRT_Optimizer"
nohup /home/moon/Projects/Bangla_SRT_Optimizer/venv/bin/streamlit run app.py --browser.gatherUsageStats false > streamlit.log 2>&1 &
