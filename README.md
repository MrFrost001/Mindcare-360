
# 🧠 MindCare 360 — AI-Powered Mental Wellness Web Application

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg">
  <img src="https://img.shields.io/badge/SQLite-Database-green.svg">
  <img src="https://img.shields.io/badge/Groq-AI-orange.svg">
  <img src="https://img.shields.io/badge/Web-Application-red.svg">
</p>

<p align="center">
AI-powered mental wellness platform for emotional support, mood tracking, intelligent journaling, and lifestyle analysis.
</p>

---

# 📌 Project Overview

MindCare 360 is an AI-powered mental wellness web application designed to provide emotional support, self-awareness tools, and lifestyle insights using Artificial Intelligence.

The platform combines:

✅ AI-powered conversations  
✅ Emotion analysis  
✅ Mood tracking  
✅ Smart journaling  
✅ Lifestyle prediction  
✅ Personalized wellness suggestions  

The goal is to help users better understand their emotional well-being while receiving supportive and personalized guidance.

---

# 🎯 Objectives of the Project

The primary objectives of MindCare 360 are:

- Help users monitor emotional health
- Provide an AI companion for supportive conversations
- Track mood trends over time
- Analyze emotions from text
- Offer personalized wellness recommendations
- Encourage healthy lifestyle habits

---

# 🚀 Features

## 🤖 AI Wellness Chatbot

An intelligent AI companion capable of supportive conversations.

### Features

- Context-aware responses
- Conversation memory
- Personalized interaction
- CBT-inspired guidance
- Emotional understanding

---

## 📖 Smart Journal System

Users can write and save daily journal entries.

### AI-generated insights:

- Emotional insights
- Key themes
- Reflection analysis
- Thought reframing suggestions
- Emotional intensity measurement

---

## 📈 Mood Tracking System

Allows users to monitor emotional patterns over time.

### Features

- Mood rating scale
- Mood history
- Trend visualization
- Emotional statistics

---

## 🏃 Lifestyle Predictor

Analyzes user lifestyle habits based on:

- Sleep duration
- Stress level
- Physical activity
- BMI
- Diet quality
- Smoking habits
- Alcohol consumption
- Screen time

### Provides

- Risk score
- Risk category
- Health recommendations
- Personalized advice

---


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



# ⚙️ How the Project Works

## Step 1: User opens the application

Users access the web application through the browser interface.

↓

## Step 2: User selects a feature

Available modules:

- 🤖 Chatbot
- 📈 Mood Tracker
- 📖 Journal
- 😊 Emotion Detection
- 🏃 Lifestyle Prediction

↓

## Step 3: User enters information

Examples:

- Messages
- Mood values
- Journal text
- Health-related details

↓

## Step 4: Backend processing

### Chatbot Module

```text
Receive message
        ↓
Load previous history
        ↓
Send context to AI
        ↓
Generate response
        ↓
Save conversation
```

### Journal Module

```text
Receive journal entry
        ↓
Perform emotion analysis
        ↓
Generate insights
        ↓
Store results
```

### Lifestyle Predictor

```text
Receive health data
        ↓
Calculate risk score
        ↓
Generate recommendations
```

↓

## Step 5: Store information

SQLite database stores:

- Chat history
- Journal entries
- Mood logs

↓

## Step 6: Display results

Users receive:

- AI responses
- Emotional insights
- Mood statistics
- Health recommendations
---


# 🛠 Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Backend development |
| SQLite | Database management |
| Groq API | AI integration |
| LLaMA 3.3 70B | Natural Language Processing |
| Machine Learning | Lifestyle prediction |
| JSON | Structured data handling |
| HTML/CSS | Frontend design |

---


>>>>>>> 924fe6276ee3003add3a45e637dd5a04175a7622
