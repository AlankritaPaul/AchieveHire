#!/usr/bin/env bash
# AchieveHire — Environment Setup Script
# Installs platform dependencies and validates system audio/speech libraries.

set -e

echo "=========================================="
echo "   AchieveHire Platform Setup Script"
echo "=========================================="

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is required but not found in PATH."
    exit 1
fi

echo "[1/3] Creating virtual environment (.venv)..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

echo "[2/3] Activating virtual environment..."
source .venv/bin/activate

echo "[3/3] Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup completed successfully."
echo "Launch AchieveHire via: ./scripts/run_app.sh"
