# MindCare 360 v3.0 — AI Mental Wellness & Lifestyle Health Assistant

## Stack
- **Backend**: FastAPI + Groq (LLaMA 3.3-70B) + SQLite
- **Frontend**: Single-file HTML/CSS/JS — dark bioluminescent UI, Chart.js
- **New in v3**: Wellness Report, Breathing Engine (4 patterns), AI Insights, redesigned frontend

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 3. (Optional) Place your trained ML model
mkdir -p models
# Copy lifestyle_model.pkl and label_encoders.pkl into models/

# 4. Run
uvicorn main:app --reload --port 8000
```

Open `http://localhost:8000` in your browser.

## Project Structure
```
mindcare360/
├── main.py                  # FastAPI app + all routes
├── requirements.txt
├── .env.example
├── static/
│   └── index.html           # Full frontend SPA
├── backend/
│   ├── __init__.py
│   ├── chatbot.py           # CBT chatbot with SQLite memory
│   ├── emotion_text.py      # 8-class emotion classifier
│   ├── journal.py           # AI journal with CBT reframing
│   ├── lifestyle_predictor.py # Hybrid rule-based + ML risk scorer
│   ├── mood_tracker.py      # Mood logging + trend analysis
│   ├── voice_chat.py        # Whisper STT + gTTS pipeline
│   ├── wellness_report.py   # Weekly AI wellness report (NEW)
│   ├── breathing.py         # 4 breathing patterns + AI tips (NEW)
│   └── insights.py          # Cross-module AI insights (NEW)
└── models/                  # (optional) sklearn pickle files
    ├── lifestyle_model.pkl
    └── label_encoders.pkl
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Chat with wellness bot |
| GET | `/api/chat/history` | Get chat history |
| DELETE | `/api/chat/history` | Clear chat |
| POST | `/api/voice/chat` | Voice-to-voice chat |
| POST | `/api/emotion/analyze` | Analyze text emotion |
| POST | `/api/journal/analyze` | Save + analyze journal entry |
| GET | `/api/journal/entries` | Get past journal entries |
| POST | `/api/mood/log` | Log mood (1–10) |
| GET | `/api/mood/history` | Mood history (last N days) |
| GET | `/api/mood/stats` | Mood stats + trend |
| POST | `/api/lifestyle/predict` | Lifestyle risk prediction |
| GET | `/api/wellness/report` | Generate weekly AI report |
| GET | `/api/breathing/session` | Get breathing session + AI tip |
| GET | `/api/breathing/patterns` | List all breathing patterns |
| GET | `/api/insights` | Cross-module AI insights |
| GET | `/api/dashboard` | Dashboard summary |

## What's New in v3

### Backend
- **`wellness_report.py`** — Pulls mood + journal + chat data and generates a 6-section weekly wellness narrative via Groq
- **`breathing.py`** — 4 science-backed patterns (Box, 4-7-8, Coherent, Physiological Sigh) with per-pattern AI tip personalized to current emotion
- **`insights.py`** — Streak detection, cross-module correlation, rule-based + AI-generated insight cards

### Frontend
- Full dark bioluminescent redesign — navy/teal/amber palette, Sora + DM Sans fonts
- Animated sidebar with hover-expand labels
- Dashboard: live Chart.js sparklines, emotion donut chart, AI insight cards, streak badges
- Chat: emotion badge on every message, voice record button, typing indicator
- Journal: animated CBT reframe reveal card, intensity bar, keyword chips
- Mood: emoji arc selector + 14-day history chart with color-coded points
- Lifestyle: range sliders + animated SVG arc gauge
- Breathing modal: 4 patterns, animated expanding circle, phase labels, AI tip
