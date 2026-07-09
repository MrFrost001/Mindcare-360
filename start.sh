#!/bin/bash
echo "============================================"
echo "  MindCare 360 v3.0 - Starting Server"
echo "============================================"

# Create venv if missing
if [ ! -d "env" ]; then
    echo "[1/2] Creating virtual environment..."
    python3 -m venv env
fi

source env/bin/activate

# Install if needed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "[2/2] Installing packages..."
    pip install -r requirements.txt --quiet
fi

# Create .env if missing
if [ ! -f ".env" ]; then
    echo "GROQ_API_KEY=paste_your_groq_key_here" > .env
    echo ""
    echo "*** Created .env — open it and add your Groq API key from https://console.groq.com ***"
    echo ""
fi

echo "Server starting at http://localhost:8000"
echo "Press Ctrl+C to stop."
echo ""
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
