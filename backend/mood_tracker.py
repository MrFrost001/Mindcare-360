import sqlite3
from datetime import datetime

DB_PATH = "chat_memory.db"

MOOD_EMOJIS = {
    1: "😔", 2: "😕", 3: "😐", 4: "🙂", 5: "😊",
    6: "😄", 7: "😁", 8: "🤩", 9: "🥰", 10: "🌟"
}


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mood_logs (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            mood      INTEGER NOT NULL,
            note      TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def log_mood(mood: int, note: str = "") -> dict:
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO mood_logs (mood, note) VALUES (?, ?)", (mood, note))
    conn.commit()
    conn.close()
    return {"status": "logged", "mood": mood, "emoji": MOOD_EMOJIS.get(mood, "😐")}


def get_history(days: int = 14) -> list[dict]:
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        """SELECT mood, note, timestamp FROM mood_logs
           WHERE timestamp >= datetime('now', ?) ORDER BY timestamp ASC""",
        (f"-{days} days",),
    ).fetchall()
    conn.close()
    return [
        {"mood": r[0], "emoji": MOOD_EMOJIS.get(r[0], "😐"), "note": r[1], "timestamp": r[2]}
        for r in rows
    ]


def get_stats() -> dict:
    _init_db()
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT mood FROM mood_logs ORDER BY id DESC LIMIT 30").fetchall()
    conn.close()
    if not rows:
        return {"average": 0, "total_logs": 0, "trend": "no data"}
    moods = [r[0] for r in rows]
    avg = round(sum(moods) / len(moods), 1)
    recent_avg = round(sum(moods[:7]) / len(moods[:7]), 1) if len(moods) >= 7 else avg
    older_avg  = round(sum(moods[7:]) / len(moods[7:]), 1) if len(moods) > 7 else avg
    trend = "improving" if recent_avg > older_avg else ("declining" if recent_avg < older_avg else "stable")
    return {
        "average": avg,
        "total_logs": len(moods),
        "trend": trend,
        "emoji": MOOD_EMOJIS.get(round(avg), "😐"),
    }
