# 🧠 MindCare 360 — AI-Powered Mental Wellness Web Application

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg">
  <img src="https://img.shields.io/badge/SQLite-Database-green.svg">
  <img src="https://img.shields.io/badge/Groq-AI-orange.svg">
  <img src="https://img.shields.io/badge/Web-Application-red.svg">
</p>

---

# 📌 Project Overview

MindCare 360 is an AI-powered mental wellness web application designed to provide users with emotional support, self-awareness tools, and lifestyle insights through intelligent analysis.

The system combines Artificial Intelligence, emotional analysis, mood tracking, journaling, chatbot interaction, and lifestyle prediction into a single platform.

The objective of the project is to help users understand their emotional state, monitor mental well-being, and receive personalized guidance in an accessible and user-friendly environment.

---

# 🎯 Objectives of the Project

The main objectives of MindCare 360 are:

* Help users monitor emotional health
* Provide an AI companion for supportive conversations
* Track mood trends over time
* Analyze emotions from text
* Offer personalized wellness suggestions
* Encourage healthy lifestyle habits

---

# 🚀 Features

## 🤖 AI Wellness Chatbot

The chatbot acts as an intelligent companion capable of engaging in supportive conversations.

Features:

* Context-aware responses
* Conversation memory
* Personalized interaction
* CBT-inspired guidance
* Emotional understanding

---

## 📖 Smart Journal System

Users can write daily journal entries.

The AI analyzes entries and generates:

* Emotional insights
* Key themes
* Reflection analysis
* Thought reframing suggestions
* Emotional intensity

---

## 📈 Mood Tracking System

Allows users to log daily mood values.

Features:

* Mood rating scale
* Mood history
* Mood trends
* Emotional statistics

---

## 🏃 Lifestyle Predictor

Evaluates user lifestyle habits based on:

* Sleep duration
* Stress level
* Physical activity
* BMI
* Diet quality
* Smoking habits
* Alcohol consumption
* Screen time

Provides:

* Risk score
* Risk category
* Health recommendations
* Personalized advice

---

# ⚙️ How the Project Works

### Step 1: User opens the web application

The user accesses the application through a browser interface.

---

### Step 2: User selects a feature

Available features:

* Chatbot
* Mood Tracker
* Journal
* Emotion Detection
* Lifestyle Prediction

---

### Step 3: User enters data

Examples:

* Messages
* Mood values
* Journal text
* Health details

---

### Step 4: Backend processing

Depending on the selected module:

**Chatbot**

* Receives message
* Loads previous history
* Sends context to AI
* Generates response
* Saves conversation

**Journal**

* Receives journal entry
* Performs emotional analysis
* Generates insights
* Saves data

**Lifestyle Predictor**

* Evaluates user habits
* Calculates risk score
* Generates recommendations

---

### Step 5: Store information

SQLite database stores:

* Chat history
* Journal entries
* Mood logs

---

### Step 6: Display output

Users receive:

* AI responses
* Emotional insights
* Mood statistics
* Health recommendations

---

# 💾 Database Structure

### Messages Table

Stores chatbot conversation history.

Fields:

* id
* role
* content
* timestamp

---

### Journal Entries Table

Stores journal content and analysis.

Fields:

* id
* content
* analysis
* timestamp

---

# 🛠 Technologies Used

| Technology                  | Purpose                     |
| --------------------------- | --------------------------- |
| Python                      | Backend development         |
| SQLite                      | Database management         |
| Groq API                    | AI integration              |
| LLaMA 3.3 70B               | Natural language processing |
| Machine Learning            | Lifestyle prediction        |
| JSON                        | Structured data handling    |
| HTML/CSS/Frontend Framework | User interface              |

---




---

# ⭐ If you found this project useful, please give it a star.
