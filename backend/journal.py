import sqlite3
import json
import os
from groq import Groq

DB_PATH = "chat_memory.db"


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            content    TEXT NOT NULL,
            analysis   TEXT,
            timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def analyze_and_save(entry_text: str) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""Analyze this personal journal entry and return ONLY a valid JSON object with these fields:
- "emotion": primary emotion detected (joy/sadness/anger/anxiety/fear/neutral/hope/gratitude)
- "valence": "positive" | "neutral" | "negative"
- "keywords": list of 3-5 key themes/words
- "insight": 2-3 sentence empathetic reflection on what the person wrote
- "cbt_reframe": one helpful CBT-style thought reframe if emotion is negative, else an affirmation
- "intensity": emotion intensity 1-10

Journal entry: {entry_text}

Return ONLY the JSON object, no markdown."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.5,
    )
    raw = response.choices[0].message.content.strip()
    try:
        analysis = json.loads(raw)
    except Exception:
        analysis = {
            "emotion": "neutral", "valence": "neutral",
            "keywords": [], "insight": raw,
            "cbt_reframe": "", "intensity": 5
        }

    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO journal_entries (content, analysis) VALUES (?, ?)",
        (entry_text, json.dumps(analysis))
    )
    conn.commit()
    conn.close()

    return {"entry": entry_text, "analysis": analysis}


def get_entries(limit: int = 20) -> list[dict]:
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, content, analysis, timestamp FROM journal_entries ORDER BY id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    result = []
    for r in rows:
        try:
            analysis = json.loads(r[2]) if r[2] else {}
        except Exception:
            analysis = {}
        result.append({"id": r[0], "content": r[1], "analysis": analysis, "timestamp": r[3]})
    return result
