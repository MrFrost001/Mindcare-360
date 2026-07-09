import sqlite3
import json
import os
from groq import Groq
from datetime import datetime, timedelta

DB_PATH = "chat_memory.db"


def _fetch_all_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        try:
            moods = conn.execute(
                "SELECT mood, note, timestamp FROM mood_logs ORDER BY id DESC LIMIT 30"
            ).fetchall()
        except Exception:
            moods = []
        try:
            journals = conn.execute(
                "SELECT analysis, timestamp FROM journal_entries ORDER BY id DESC LIMIT 20"
            ).fetchall()
        except Exception:
            journals = []
        try:
            msgs = conn.execute(
                "SELECT role, content, timestamp FROM messages ORDER BY id DESC LIMIT 50"
            ).fetchall()
        except Exception:
            msgs = []
        conn.close()
        return moods, journals, msgs
    except Exception:
        return [], [], []


def get_insights() -> dict:
    moods, journals, msgs = _fetch_all_data()

    if not moods and not journals and not msgs:
        return {
            "insights": [],
            "correlation_score": None,
            "ai_summary": "Start logging your mood and journaling to unlock personalized insights.",
            "streaks": {"mood_log_streak": 0, "journal_streak": 0},
        }

    # Compute streaks
    mood_streak = _compute_streak([m[2] for m in moods])
    journal_streak = _compute_streak([j[1] for j in journals])

    # Rule-based insights
    insights = []
    
    mood_values = [m[0] for m in moods]
    if mood_values:
        avg = sum(mood_values) / len(mood_values)
        if avg < 5:
            insights.append({
                "type": "warning",
                "icon": "📉",
                "title": "Mood Below Baseline",
                "text": f"Your average mood over the last {len(mood_values)} logs is {avg:.1f}/10. Consider a breathing exercise or journaling session.",
            })
        elif avg >= 7:
            insights.append({
                "type": "positive",
                "icon": "🌟",
                "title": "Strong Emotional Health",
                "text": f"Your average mood is {avg:.1f}/10 — you're thriving! Keep the habits that are working.",
            })

    journal_emotions = []
    for j in journals:
        try:
            a = json.loads(j[0]) if j[0] else {}
            journal_emotions.append(a.get("emotion", "unknown"))
        except Exception:
            pass

    if journal_emotions.count("anxiety") >= 3:
        insights.append({
            "type": "warning",
            "icon": "😰",
            "title": "Recurring Anxiety Pattern",
            "text": "Anxiety appears frequently in your journal entries. Box breathing and daily 5-minute mindfulness may help.",
        })

    if journal_streak >= 3:
        insights.append({
            "type": "positive",
            "icon": "🔥",
            "title": f"{journal_streak}-Day Journal Streak",
            "text": "Consistent journaling is a proven predictor of improved emotional regulation. Keep it up!",
        })

    if mood_streak >= 5:
        insights.append({
            "type": "positive",
            "icon": "💪",
            "title": f"{mood_streak}-Day Mood Logging Streak",
            "text": "Daily mood logging builds self-awareness over time. You're building a powerful habit.",
        })

    user_msgs = [m[1] for m in msgs if m[0] == "user"]
    if len(user_msgs) >= 10:
        insights.append({
            "type": "neutral",
            "icon": "💬",
            "title": "Active Engagement",
            "text": f"You've had {len(user_msgs)} chat interactions. Regular check-ins with MindCare correlate with better emotional resilience.",
        })

    # AI narrative summary
    ai_summary = _generate_ai_summary(mood_values, journal_emotions, len(user_msgs))

    return {
        "insights": insights[:5],
        "ai_summary": ai_summary,
        "streaks": {
            "mood_log_streak": mood_streak,
            "journal_streak": journal_streak,
            "total_chat_messages": len(user_msgs),
        },
        "emotion_breakdown": _emotion_counts(journal_emotions),
    }


def _compute_streak(timestamps: list) -> int:
    if not timestamps:
        return 0
    try:
        dates = sorted(set(t[:10] for t in timestamps if t), reverse=True)
        streak = 0
        today = datetime.now().date()
        for i, d in enumerate(dates):
            dt = datetime.strptime(d, "%Y-%m-%d").date()
            expected = today - timedelta(days=i)
            if dt == expected:
                streak += 1
            else:
                break
        return streak
    except Exception:
        return 0


def _emotion_counts(emotions: list) -> dict:
    counts = {}
    for e in emotions:
        counts[e] = counts.get(e, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def _generate_ai_summary(moods: list, emotions: list, chat_count: int) -> str:
    if not moods and not emotions:
        return "Begin your wellness journey by logging your first mood or writing a journal entry."
    
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        context = f"Mood scores: {moods[:10]}, Journal emotions: {emotions[:10]}, Chat count: {chat_count}"
        prompt = f"""Based on this mental wellness data: {context}
Write a 2-sentence personalized insight summary. Be warm, specific, and data-driven.
Don't start with 'Based on' or 'I'. Make it feel like a caring therapist's observation."""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.6,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Your consistent engagement with MindCare 360 reflects a genuine commitment to your wellbeing."
