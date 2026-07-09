import os
import json
from groq import Groq

PATTERNS = {
    "box": {
        "name": "Box Breathing",
        "phases": [
            {"label": "Inhale", "duration": 4, "color": "#14b8a6"},
            {"label": "Hold", "duration": 4, "color": "#8b5cf6"},
            {"label": "Exhale", "duration": 4, "color": "#3b82f6"},
            {"label": "Hold", "duration": 4, "color": "#f59e0b"},
        ],
        "cycles": 4,
        "best_for": "stress, focus, anxiety",
        "description": "Equal count for all four phases. Used by Navy SEALs for stress control.",
    },
    "478": {
        "name": "4-7-8 Breathing",
        "phases": [
            {"label": "Inhale", "duration": 4, "color": "#14b8a6"},
            {"label": "Hold", "duration": 7, "color": "#8b5cf6"},
            {"label": "Exhale", "duration": 8, "color": "#3b82f6"},
        ],
        "cycles": 4,
        "best_for": "sleep, deep anxiety, racing thoughts",
        "description": "Extended exhale activates parasympathetic response. Ideal before sleep.",
    },
    "coherent": {
        "name": "Coherent Breathing",
        "phases": [
            {"label": "Inhale", "duration": 5, "color": "#14b8a6"},
            {"label": "Exhale", "duration": 5, "color": "#3b82f6"},
        ],
        "cycles": 6,
        "best_for": "general calm, heart rate variability, mindfulness",
        "description": "5 breaths per minute. Maximizes heart rate variability and calm.",
    },
    "physiological_sigh": {
        "name": "Physiological Sigh",
        "phases": [
            {"label": "Inhale", "duration": 2, "color": "#14b8a6"},
            {"label": "Inhale again (double)", "duration": 1, "color": "#10b981"},
            {"label": "Long Exhale", "duration": 6, "color": "#3b82f6"},
        ],
        "cycles": 3,
        "best_for": "immediate panic, acute stress, overwhelm",
        "description": "Discovered by Stanford neuroscience. Fastest known way to reduce stress.",
    },
}


def get_session(pattern_type: str = "box", current_emotion: str = "neutral") -> dict:
    # Auto-select best pattern if not specified or if 'auto'
    if pattern_type == "auto" or pattern_type not in PATTERNS:
        emotion_map = {
            "anxiety": "478",
            "fear": "physiological_sigh",
            "anger": "box",
            "sadness": "coherent",
            "joy": "coherent",
            "neutral": "box",
            "disgust": "box",
            "surprise": "physiological_sigh",
        }
        pattern_type = emotion_map.get(current_emotion, "box")

    pattern = PATTERNS[pattern_type]

    # Generate AI tip
    tip = _generate_tip(pattern["name"], current_emotion)

    return {
        "pattern_type": pattern_type,
        "pattern": pattern,
        "ai_tip": tip,
        "total_duration_seconds": sum(p["duration"] for p in pattern["phases"]) * pattern["cycles"],
    }


def _generate_tip(pattern_name: str, emotion: str) -> str:
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        prompt = f"""The user is about to do a {pattern_name} breathing exercise. Their current emotional state is: {emotion}.
Write one short, warm, encouraging tip (2 sentences max) to help them get the most from this session.
Be specific to both the technique and their emotion. No generic advice."""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return f"Find a comfortable position and focus on each phase of {pattern_name}. Your breath is your most powerful tool for calm."


def list_patterns() -> dict:
    return {k: {"name": v["name"], "best_for": v["best_for"], "description": v["description"]} for k, v in PATTERNS.items()}
