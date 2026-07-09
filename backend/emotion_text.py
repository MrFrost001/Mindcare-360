import os
import json
from groq import Groq

EMOTIONS = ["joy", "sadness", "anger", "fear", "anxiety", "neutral", "disgust", "surprise"]

PROMPT = """Analyze the emotional tone of the following message and return a JSON object with:
- "primary_emotion": one of {emotions}
- "confidence": float 0-1
- "valence": "positive" | "neutral" | "negative"
- "brief_insight": one short sentence about the emotional state

Return ONLY valid JSON, no markdown, no explanation.

Message: {{message}}""".format(emotions=EMOTIONS)


def analyze(text: str) -> dict:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": PROMPT.replace("{{message}}", text)}
        ],
        max_tokens=150,
        temperature=0.3,
    )
    raw = response.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except Exception:
        return {
            "primary_emotion": "neutral",
            "confidence": 0.5,
            "valence": "neutral",
            "brief_insight": "Could not analyze emotion.",
        }
