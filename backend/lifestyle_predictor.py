import os
import pickle
import numpy as np

MODEL_PATH = "models/lifestyle_model.pkl"
ENCODER_PATH = "models/label_encoders.pkl"

_model = None
_encoders = None


def _load():
    global _model, _encoders
    if _model is None and os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, "rb") as f:
                _model = pickle.load(f)
        except Exception as e:
            print(f"[lifestyle_predictor] Could not load ML model: {e}. Using rule-based only.")
            _model = None
    if _encoders is None and os.path.exists(ENCODER_PATH):
        try:
            with open(ENCODER_PATH, "rb") as f:
                _encoders = pickle.load(f)
        except Exception as e:
            print(f"[lifestyle_predictor] Could not load encoders: {e}.")
            _encoders = None


def predict(data: dict) -> dict:
    _load()

    score = 0
    factors = []

    if data.get("bmi", 22) > 30:
        score += 25
        factors.append("High BMI indicates obesity risk")
    elif data.get("bmi", 22) > 25:
        score += 12
        factors.append("Slightly elevated BMI")

    if data.get("sleep_hours", 7) < 6:
        score += 20
        factors.append("Insufficient sleep — linked to metabolic disorders")
    elif data.get("sleep_hours", 7) > 9:
        score += 8
        factors.append("Excessive sleep may indicate underlying issues")

    if data.get("stress_level", 5) >= 7:
        score += 20
        factors.append("High stress increases cardiovascular risk")

    if data.get("physical_activity_days", 3) < 2:
        score += 20
        factors.append("Low physical activity — major lifestyle risk factor")

    if data.get("smoking", 0) == 1:
        score += 20
        factors.append("Smoking significantly raises disease risk")

    if data.get("alcohol_consumption", 0) > 3:
        score += 15
        factors.append("High alcohol consumption")

    if data.get("screen_time_hours", 6) > 8:
        score += 10
        factors.append("Excessive screen time linked to sedentary lifestyle")

    if data.get("diet_quality", 7) < 5:
        score += 15
        factors.append("Poor diet quality — key risk modifier")

    score = min(score, 100)

    if score < 25:
        risk = "Low"; color = "green"
        advice = "You're maintaining great lifestyle habits! Keep it up."
    elif score < 50:
        risk = "Moderate"; color = "yellow"
        advice = "Some areas need attention — focus on sleep, diet, and stress."
    elif score < 75:
        risk = "High"; color = "orange"
        advice = "Significant lifestyle risks detected. Consider consulting a healthcare professional."
    else:
        risk = "Very High"; color = "red"
        advice = "Multiple high-risk factors present. Please consult a doctor soon."

    recommendations = []
    if data.get("sleep_hours", 7) < 7:
        recommendations.append("Aim for 7–8 hours of quality sleep nightly")
    if data.get("physical_activity_days", 3) < 4:
        recommendations.append("Add 2–3 more days of 30-min moderate exercise per week")
    if data.get("stress_level", 5) >= 6:
        recommendations.append("Practice daily mindfulness or deep breathing (5–10 min)")
    if data.get("diet_quality", 7) < 7:
        recommendations.append("Increase fruits, vegetables, and reduce processed foods")
    if data.get("screen_time_hours", 6) > 6:
        recommendations.append("Take 20-20-20 screen breaks (every 20 min, look 20ft away for 20s)")
    if not recommendations:
        recommendations.append("Maintain your current healthy lifestyle habits")

    ml_result = None
    if _model is not None:
        try:
            features = _prepare_features(data)
            ml_pred = _model.predict([features])[0]
            proba = _model.predict_proba([features])[0] if hasattr(_model, "predict_proba") else None
            ml_result = {
                "prediction": str(ml_pred),
                "confidence": float(max(proba)) if proba is not None else None,
            }
        except Exception as e:
            ml_result = {"error": str(e)}

    return {
        "risk_level": risk,
        "risk_score": score,
        "risk_color": color,
        "key_factors": factors,
        "recommendations": recommendations,
        "advice": advice,
        "ml_result": ml_result,
    }


def _prepare_features(data: dict) -> list:
    return [
        data.get("age", 25),
        1 if str(data.get("gender", "male")).lower() == "male" else 0,
        data.get("bmi", 22),
        data.get("sleep_hours", 7),
        data.get("physical_activity_days", 3),
        data.get("stress_level", 5),
        data.get("diet_quality", 7),
        data.get("smoking", 0),
        data.get("alcohol_consumption", 0),
        data.get("screen_time_hours", 6),
    ]
