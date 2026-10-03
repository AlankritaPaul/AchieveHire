#!/usr/bin/env bash
# AchieveHire — Launch Server Script
# Starts the Streamlit application on port 8501.

PORT=${PORT:-8501}

echo "Starting AchieveHire on port ${PORT}..."
python3 -m streamlit run app.py --server.port "${PORT}" --server.headless true
