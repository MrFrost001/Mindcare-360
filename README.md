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

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Objectives](#-objectives-of-the-project)
- [Features](#-features)
- [Project Workflow](#-how-the-project-works)
- [Database Structure](#-database-structure)
- [Technologies Used](#-technologies-used)
- [Future Improvements](#-future-improvements)

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

# 💾 Database Structure

## Messages Table

Stores chatbot conversations.

| Field | Type |
|---------|------|
| id | Integer |
| role | Text |
| content | Text |
| timestamp | DateTime |

---

## Journal Entries Table

Stores journal data and analysis.

| Field | Type |
|---------|------|
| id | Integer |
| content | Text |
| analysis | Text |
| timestamp | DateTime |

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

# 🔮 Future Improvements

Planned enhancements:

- User authentication system
- Real-time emotion detection
- Voice-based chatbot interaction
- Mood visualization dashboards
- Cloud deployment
- Mobile application support

---

# 👨‍💻 Author

**Utkarsh Maurya**  
AI & Machine Learning Engineer | Python Developer

📧 Email: maurya124421@gmail.com  
📍 Varanasi, Uttar Pradesh, India  

---

<p align="center">
⭐ If you found this project useful, consider giving it a star.
</p>
