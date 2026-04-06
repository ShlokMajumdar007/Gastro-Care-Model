import os
import joblib
import pandas as pd
from symptom_extractor import update_symptoms
from responses import generate_response

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
# 🧠 Initial Symptom State
# ==============================
def reset_symptoms():
    return {
        "abdominal_pain": 0,
        "bloating": 0,
        "diarrhea": 0,
        "constipation": 0,
        "acid_reflux": 0,
        "nausea": 0,
        "vomiting": 0,
        "weight_loss": 0,
        "blood_in_stool": 0,
        "fever": 0,
        "pain_duration_days": 3
    }

symptoms = reset_symptoms()

print("\n🩺 Gastro AI Chatbot (Hybrid ML)")
print("Describe your symptoms naturally.")
print("Commands: reset | status | exit\n")

# ==============================
# 🔁 Chat Loop
# ==============================
while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Chatbot: Take care! 👋")
        break

    if user_input.lower() == "reset":
        symptoms = reset_symptoms()
        print("Chatbot: 🔄 Symptoms reset.\n")
        continue

    if user_input.lower() == "status":
        print("\n📊 Current Symptoms:")
        for k, v in symptoms.items():
            print(f"{k}: {v}")
        print()
        continue

    # ==============================
    # 🧠 Update Symptoms (NLP)
    # ==============================
    symptoms = update_symptoms(symptoms, user_input)

    # ==============================
    # 📊 Convert to DataFrame
    # ==============================
    df = pd.DataFrame([symptoms])
    df = pd.get_dummies(df)
    df = df.reindex(columns=feature_columns, fill_value=0)

    # ==============================
    # 🤖 Predictions
    # ==============================
    condition = condition_model.predict(df)[0]
    severity_score = severity_model.predict(df)[0]
    severity = severity_label(severity_score)

    # ==============================
    # 💬 Response Generation
    # ==============================
    response = generate_response(condition, severity, symptoms)

    # ==============================
    # 🧾 Output
    # ==============================
    print("\nChatbot:")
    print(response)

    print(f"\n📈 Severity Score: {round(float(severity_score),2)} ({severity})")

    # ==============================
    # 🧠 Smart follow-up (NEW 🔥)
    # ==============================
    if severity == "SEVERE":
        print("⚠ I strongly recommend seeking medical help immediately.\n")

    elif severity == "MODERATE":
        print("👉 Monitor symptoms closely. Want diet tips? (yes/no)\n")

    elif severity == "MILD":
        print("👉 This looks manageable. Stay hydrated 👍\n")