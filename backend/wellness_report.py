import sqlite3
import json
import os
from groq import Groq

DB_PATH = "chat_memory.db"


def _get_mood_summary() -> dict:
    try:
        conn = sqlite3.connect(DB_PATH)
        try:
            rows = conn.execute(
                "SELECT mood, timestamp FROM mood_logs ORDER BY id DESC LIMIT 30"
            ).fetchall()
        except Exception:
            rows = []
        conn.close()
        if not rows:
            return {"count": 0, "average": None, "trend": "no data"}
        moods = [r[0] for r in rows]
        avg = round(sum(moods) / len(moods), 1)
        recent = moods[:7]
        older = moods[7:] if len(moods) > 7 else moods
        trend = "improving" if sum(recent)/len(recent) > sum(older)/len(older) else (
            "declining" if sum(recent)/len(recent) < sum(older)/len(older) else "stable"
        )
        return {"count": len(moods), "average": avg, "trend": trend, "scores": moods[:14]}
    except Exception:
        return {"count": 0, "average": None, "trend": "no data"}


def _get_journal_summary(limit: int = 10) -> list:
    try:
        conn = sqlite3.connect(DB_PATH)
        try:
            rows = conn.execute(
                "SELECT analysis, timestamp FROM journal_entries ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        except Exception:
            rows = []
        conn.close()
        emotions = []
        for r in rows:
            try:
                a = json.loads(r[0]) if r[0] else {}
                emotions.append({
                    "emotion": a.get("emotion", "unknown"),
                    "valence": a.get("valence", "neutral"),
                    "intensity": a.get("intensity", 5),
                })
            except Exception:
                pass
        return emotions
    except Exception:
        return []


def _get_chat_count() -> int:
    try:
        conn = sqlite3.connect(DB_PATH)
        try:
            row = conn.execute(
                "SELECT COUNT(*) FROM messages WHERE role='user' AND timestamp >= datetime('now', '-7 days')"
            ).fetchone()
        except Exception:
            row = None
        conn.close()
        return row[0] if row else 0
    except Exception:
        return 0


def generate_report() -> dict:
    mood = _get_mood_summary()
    journals = _get_journal_summary()
    chat_count = _get_chat_count()

    journal_emotions = [j["emotion"] for j in journals]
    negative_entries = sum(1 for j in journals if j["valence"] == "negative")
    positive_entries = sum(1 for j in journals if j["valence"] == "positive")

    context = f"""
Weekly Wellness Data Summary:
- Mood: {mood['count']} logs, average score {mood['average']}/10, trend: {mood['trend']}
- Mood scores (recent first): {mood.get('scores', [])}
- Journal: {len(journals)} entries analyzed. Emotions: {journal_emotions}
- Negative journal entries: {negative_entries}, Positive: {positive_entries}
- Chat interactions this week: {chat_count}
"""

    prompt = f"""You are MindCare 360's wellness analyst. Based on this user's week data, write a warm, personal, 
evidence-based weekly wellness report. Structure it as:

1. **Week Overview** (2-3 sentences: overall emotional health summary)
2. **Mood Patterns** (what the mood data tells us)
3. **Emotional Themes** (patterns from journal entries)
4. **Strengths This Week** (what went well, celebrate wins)
5. **Focus Area for Next Week** (one specific, actionable recommendation)
6. **Affirmation** (one powerful closing affirmation)

Data:
{context}

Write in second person ("You..."), warm and clinical but not robotic. Keep each section 2-3 sentences.
Return as plain text with the section headers using ** markdown."""

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7,
        )
        report_text = response.choices[0].message.content.strip()
    except Exception as e:
        report_text = f"Unable to generate report at this time. Please try again later.\n\nError: {str(e)}"

    return {
        "report": report_text,
        "stats": {
            "mood_average": mood["average"],
            "mood_trend": mood["trend"],
            "mood_logs": mood["count"],
            "journal_entries": len(journals),
            "chat_sessions": chat_count,
            "positive_days": positive_entries,
            "negative_days": negative_entries,
        }
    }
