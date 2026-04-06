import joblib
import pandas as pd
from first_aid_logic import first_aid_response

condition_model = joblib.load("model/condition_model.pkl")
severity_model = joblib.load("model/severity_model.pkl")
feature_columns = joblib.load("model/feature_columns.pkl")

sample = {
    "abdominal_pain": 1,
    "bloating": 1,
    "diarrhea": 0,
    "constipation": 0,
    "acid_reflux": 1,
    "nausea": 0,
    "vomiting": 0,
    "weight_loss": 0,
    "blood_in_stool": 0,
    "fever": 0,
    "pain_duration_days": 5
}

df = pd.DataFrame([sample])
df = pd.get_dummies(df)
df = df.reindex(columns=feature_columns, fill_value=0)

condition = condition_model.predict(df)[0]
severity_score = severity_model.predict(df)[0]

# Convert score → label
if severity_score < 30:
    severity = "MILD"
elif severity_score < 70:
    severity = "MODERATE"
else:
    severity = "SEVERE"

print("Condition:", condition)
print("Severity Score:", severity_score)
print("Severity:", severity)

print("\nAdvice:")
for tip in first_aid_response(condition, severity):
    print("-", tip)