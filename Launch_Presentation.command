#!/bin/bash
# EstatePulse AI - Instant Presentation Launcher
echo "=========================================================="
echo " Starting EstatePulse AI Enterprise Platform..."
echo "=========================================================="
cd "$(dirname "$0")"

# Activate conda if available, or use system python
if command -v conda &> /dev/null; then
    eval "$(conda shell.bash hook 2>/dev/null)"
fi

# Run Streamlit
streamlit run app.py
