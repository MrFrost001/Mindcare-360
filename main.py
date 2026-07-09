import os
import base64
import logging
from pathlib import Path

from dotenv import load_dotenv
# Load .env from the directory where main.py lives
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("mindcare360")

_key = os.getenv("GROQ_API_KEY", "")
if not _key:
    logger.error("❌  GROQ_API_KEY not set! Add it to your .env file.")
else:
    logger.info(f"✅  GROQ_API_KEY loaded → {_key[:8]}...")

from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend import chatbot, emotion_text, lifestyle_predictor, mood_tracker, voice_chat, journal
from backend import wellness_report, breathing, insights

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(title="MindCare 360", version="3.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path("static")
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ── Frontend ───────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = STATIC_DIR / "index.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text())
    return HTMLResponse("<h1>MindCare 360</h1><p>static/index.html not found</p>")


# ── Models ─────────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str

class MoodRequest(BaseModel):
    mood: int
    note: str = ""

class EmotionRequest(BaseModel):
    text: str

class LifestyleRequest(BaseModel):
    age: int = 25
    gender: str = "male"
    bmi: float = 22.0
    sleep_hours: float = 7.0
    physical_activity_days: int = 3
    stress_level: int = 5
    diet_quality: int = 7
    smoking: int = 0
    alcohol_consumption: int = 0
    screen_time_hours: float = 6.0

class JournalRequest(BaseModel):
    entry: str

class BreathingRequest(BaseModel):
    pattern: str = "auto"
    emotion: str = "neutral"


# ── Chat ───────────────────────────────────────────────────────────────────────
@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    try:
        reply = chatbot.chat(req.message)
        emotion = emotion_text.analyze(req.message)
        return {"reply": reply, "emotion": emotion}
    except Exception as e:
        logger.error(f"Chat error: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")


@app.get("/api/chat/history")
async def api_chat_history():
    return chatbot.get_history(limit=50)


@app.delete("/api/chat/history")
async def api_clear_history():
    chatbot.clear_history()
    return {"status": "cleared"}


# ── Voice ──────────────────────────────────────────────────────────────────────
@app.post("/api/voice/chat")
async def api_voice_chat(audio: UploadFile = File(...)):
    try:
        audio_bytes = await audio.read()
        result = voice_chat.voice_chat(audio_bytes, filename=audio.filename or "audio.webm")
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return {
            "transcript": result["transcript"],
            "reply": result["reply"],
            "audio_b64": base64.b64encode(result["audio"]).decode(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/voice/transcribe")
async def api_transcribe(audio: UploadFile = File(...)):
    try:
        audio_bytes = await audio.read()
        text = voice_chat.transcribe(audio_bytes, filename=audio.filename or "audio.webm")
        return {"transcript": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Emotion ────────────────────────────────────────────────────────────────────
@app.post("/api/emotion/analyze")
async def api_emotion(req: EmotionRequest):
    try:
        return emotion_text.analyze(req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Lifestyle ──────────────────────────────────────────────────────────────────
@app.post("/api/lifestyle/predict")
async def api_lifestyle(req: LifestyleRequest):
    try:
        return lifestyle_predictor.predict(req.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Mood ───────────────────────────────────────────────────────────────────────
@app.post("/api/mood/log")
async def api_mood_log(req: MoodRequest):
    if not 1 <= req.mood <= 10:
        raise HTTPException(status_code=400, detail="Mood must be 1–10")
    return mood_tracker.log_mood(req.mood, req.note)


@app.get("/api/mood/history")
async def api_mood_history(days: int = 14):
    return mood_tracker.get_history(days)


@app.get("/api/mood/stats")
async def api_mood_stats():
    return mood_tracker.get_stats()


# ── Journal ───────────────────────────────────────────────────────────────────
@app.post("/api/journal/analyze")
async def api_journal_analyze(req: JournalRequest):
    if len(req.entry.strip()) < 10:
        raise HTTPException(status_code=400, detail="Entry too short")
    try:
        return journal.analyze_and_save(req.entry)
    except Exception as e:
        logger.error(f"Journal error: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")


@app.get("/api/journal/entries")
async def api_journal_entries(limit: int = 20):
    return journal.get_entries(limit)


# ── Dashboard ──────────────────────────────────────────────────────────────────
@app.get("/api/dashboard")
async def api_dashboard():
    stats = mood_tracker.get_stats()
    history = mood_tracker.get_history(days=7)
    chat_hist = chatbot.get_history(limit=100)
    return {
        "mood_stats": stats,
        "mood_week": history,
        "total_messages": len(chat_hist),
        "user_messages": sum(1 for m in chat_hist if m["role"] == "user"),
    }


# ── Wellness Report (NEW) ──────────────────────────────────────────────────────
@app.get("/api/wellness/report")
async def api_wellness_report():
    try:
        return wellness_report.generate_report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Breathing (NEW) ───────────────────────────────────────────────────────────
@app.get("/api/breathing/patterns")
async def api_breathing_patterns():
    return breathing.list_patterns()


@app.get("/api/breathing/session")
async def api_breathing_session(
    pattern: str = Query(default="box"),
    emotion: str = Query(default="neutral"),
):
    try:
        return breathing.get_session(pattern, emotion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Insights (NEW) ────────────────────────────────────────────────────────────
@app.get("/api/insights")
async def api_insights():
    try:
        return insights.get_insights()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
