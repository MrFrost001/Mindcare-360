import sqlite3
import os
from groq import Groq

DB_PATH = "chat_memory.db"

SYSTEM_PROMPT = """You are MindCare 360 — an empathetic AI mental wellness companion.

Your approach:
- Use CBT-inspired techniques: help users identify and reframe negative thought patterns
- Practice active listening — always acknowledge feelings before offering advice
- Ask thoughtful follow-up questions to encourage self-reflection
- Suggest practical coping strategies (deep breathing, journaling, mindful movement)
- Celebrate small wins, normalize setbacks
- Be concise: 2-4 sentences usually enough, unless user needs more
- Be warm, human, and never robotic or generic

Boundaries:
- Never diagnose or prescribe — always recommend professional help for serious concerns
- If user expresses self-harm thoughts, gently but firmly direct to crisis resources (iCall: 9152987821)

You have emotional memory — reference past conversations naturally to show continuity of care."""


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            role      TEXT NOT NULL,
            content   TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def get_history(limit: int = 20) -> list[dict]:
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in reversed(rows)]


def save_message(role: str, content: str):
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
    conn.commit()
    conn.close()


def clear_history():
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM messages")
    conn.commit()
    conn.close()


def chat(user_message: str) -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Add it to your .env file.")
    client = Groq(api_key=api_key)
    history = get_history(limit=12)
    save_message("user", user_message)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=512,
        temperature=0.85,
    )
    reply = response.choices[0].message.content
    save_message("assistant", reply)
    return reply
