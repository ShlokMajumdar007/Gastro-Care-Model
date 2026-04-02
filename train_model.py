import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Ensure model directory exists
os.makedirs("model", exist_ok=True)

# Load dataset
data = pd.read_csv("data/data-train.csv")

# Separate features and labels
X = data.drop(["condition", "severity"], axis=1)
y_condition = data["condition"]
y_severity = data["severity"]

# One-hot encode categorical features
X = pd.get_dummies(X)

# 🔥 SAVE FEATURE SCHEMA (CRITICAL)
joblib.dump(X.columns.tolist(), "model/feature_columns.pkl")

# Train-test split
X_train, X_test, y_cond_train, y_cond_test = train_test_split(
    X, y_condition, test_size=0.2, random_state=42
)

_, _, y_sev_train, y_sev_test = train_test_split(
    X, y_severity, test_size=0.2, random_state=42
)

# Models
condition_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
severity_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

# Train models
condition_model.fit(X_train, y_cond_train)
severity_model.fit(X_train, y_sev_train)

# Accuracy
cond_acc = accuracy_score(y_cond_test, condition_model.predict(X_test))
sev_acc = accuracy_score(y_sev_test, severity_model.predict(X_test))

print(f"✅ Condition Model Accuracy : {cond_acc:.2f}")
print(f"✅ Severity Model Accuracy  : {sev_acc:.2f}")

# Save models
joblib.dump(condition_model, "model/condition_model.pkl")
joblib.dump(severity_model, "model/severity_model.pkl")

print("✅ Models + feature schema saved successfully")

