from fastapi import FastAPI, Query
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="Hybrid Gastro Medical API")

# ==============================
# ✅ Load Models Safely
# ==============================
required_files = [
    "model/condition_model.pkl",
    "model/severity_model.pkl",
    "model/feature_columns.pkl"
]

for f in required_files:
    if not os.path.exists(f):
        raise RuntimeError(f"❌ Missing file: {f}. Run train_model.py first.")

condition_model = joblib.load("model/condition_model.pkl")
severity_model = joblib.load("model/severity_model.pkl")
feature_columns = joblib.load("model/feature_columns.pkl")

# ==============================
# 🧠 Input Schema
# ==============================
class InputData(BaseModel):
    abdominal_pain: int
    bloating: int
    diarrhea: int
    constipation: int
    acid_reflux: int
    nausea: int
    vomiting: int
    weight_loss: int
    blood_in_stool: int
    fever: int
    pain_duration_days: int

# ==============================
# 🔁 Severity Mapping
# ==============================
def severity_label(score):
    if score < 30:
        return "MILD"
    elif score < 70:
        return "MODERATE"
    else:
        return "SEVERE"

# ==============================
# 🏠 Home Route
# ==============================
@app.get("/")
def home():
    return {
        "message": "✅ Hybrid Medical API Running",
        "docs": "/docs"
    }

# ==============================
# 🤖 Prediction Logic
# ==============================
def run_prediction(data_dict):
    df = pd.DataFrame([data_dict])
    df = pd.get_dummies(df)

    # Align with training schema
    df = df.reindex(columns=feature_columns, fill_value=0)

    condition = condition_model.predict(df)[0]
    severity_score = severity_model.predict(df)[0]
    severity = severity_label(severity_score)

    return condition, severity_score, severity

# ==============================
# 📩 POST Endpoint
# ==============================
@app.post("/predict")
def predict_post(data: InputData):
    condition, severity_score, severity = run_prediction(data.dict())

    return {
        "condition": condition,
        "severity_score": round(float(severity_score), 2),
        "severity": severity
    }

# ==============================
# 🌐 GET Endpoint
# ==============================
@app.get("/predict")
def predict_get(
    abdominal_pain: int = Query(...),
    bloating: int = Query(...),
    diarrhea: int = Query(...),
    constipation: int = Query(...),
    acid_reflux: int = Query(...),
    nausea: int = Query(...),
    vomiting: int = Query(...),
    weight_loss: int = Query(...),
    blood_in_stool: int = Query(...),
    fever: int = Query(...),
    pain_duration_days: int = Query(...)
):
    data_dict = {
        "abdominal_pain": abdominal_pain,
        "bloating": bloating,
        "diarrhea": diarrhea,
        "constipation": constipation,
        "acid_reflux": acid_reflux,
        "nausea": nausea,
        "vomiting": vomiting,
        "weight_loss": weight_loss,
        "blood_in_stool": blood_in_stool,
        "fever": fever,
        "pain_duration_days": pain_duration_days
    }

    condition, severity_score, severity = run_prediction(data_dict)

    return {
        "condition": condition,
        "severity_score": round(float(severity_score), 2),
        "severity": severity
    }