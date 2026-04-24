#!/bin/bash
# 1. Kill any existing instances so it doesn't crash on port conflict
pkill -f "streamlit run app.py"
sleep 1

cd "/home/moon/Projects/GithubProjects/Bangla_SRT_Optimizer"

# 2. Activate virtual environment
source venv/bin/activate

# 3. Load key from .env file explicitly
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# 4. Run streamlit in the background, headless
streamlit run app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false > /tmp/srt_optimizer.log 2>&1 &

# 5. Wait for the server to spin up
sleep 3

# 6. Force open Google Chrome to the exact port
google-chrome "http://localhost:8501" || xdg-open "http://localhost:8501"
