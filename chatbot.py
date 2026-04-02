import os
import joblib
import pandas as pd
from symptom_extractor import update_symptoms
from responses import generate_response

# Safety checks
required_files = [
    "model/condition_model.pkl",
    "model/severity_model.pkl",
    "model/feature_columns.pkl"
]

for f in required_files:
    if not os.path.exists(f):
        raise RuntimeError(f"❌ Missing file: {f}. Run train_model.py first.")

# Load models and feature schema
condition_model = joblib.load("model/condition_model.pkl")
severity_model = joblib.load("model/severity_model.pkl")
feature_columns = joblib.load("model/feature_columns.pkl")

print("\n🩺 Gastroenterology First-Aid Chatbot")
print("Describe your symptoms freely.")
print("Type 'reset' to clear symptoms or 'exit' to quit.\n")

# Persistent symptom memory
symptoms = {
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

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Chatbot: Take care and consult a doctor if symptoms persist 👋")
        break

    if user_input.lower() == "reset":
        for k in symptoms:
            symptoms[k] = 0 if k != "pain_duration_days" else 3
        print("Chatbot: Symptom history cleared.\n")
        continue

    # Update symptom memory
    symptoms = update_symptoms(symptoms, user_input)

    # Build input DataFrame
    X_input = pd.DataFrame([symptoms])

    # Apply same encoding as training
    X_input = pd.get_dummies(X_input)

    # 🔥 ALIGN FEATURES EXACTLY
    X_input = X_input.reindex(columns=feature_columns, fill_value=0)

    # Predict
    condition = condition_model.predict(X_input)[0]
    severity = severity_model.predict(X_input)[0]

    print("\nChatbot:")
    print(generate_response(condition, severity))
