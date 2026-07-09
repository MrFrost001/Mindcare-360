import os
import tempfile
from groq import Groq
from gtts import gTTS
from backend.chatbot import chat


def transcribe(audio_bytes: bytes, filename: str = "audio.webm") -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(filename)[1] or ".webm", delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name
    try:
        with open(tmp_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=(filename, f, "audio/webm"),
                response_format="text",
            )
        return result.strip() if isinstance(result, str) else result.text.strip()
    finally:
        os.unlink(tmp_path)


def synthesize(text: str, lang: str = "en") -> bytes:
    tts = gTTS(text=text, lang=lang, slow=False)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        tmp_path = f.name
    try:
        tts.save(tmp_path)
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        os.unlink(tmp_path)


def voice_chat(audio_bytes: bytes, filename: str = "audio.webm") -> dict:
    transcript = transcribe(audio_bytes, filename)
    if not transcript:
        return {"error": "Could not transcribe audio", "transcript": "", "reply": "", "audio": None}
    reply = chat(transcript)
    audio = synthesize(reply)
    return {"transcript": transcript, "reply": reply, "audio": audio}
