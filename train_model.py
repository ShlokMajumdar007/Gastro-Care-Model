import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error

# ============================
# 📁 Paths
# ============================
TRAIN_PATH = "data/data-train.csv"
VAL_PATH = "data/data-val.csv"
TEST_PATH = "data/data-test.csv"

os.makedirs("model", exist_ok=True)

# ============================
# 📥 Load Data
# ============================
train_df = pd.read_csv(TRAIN_PATH)
val_df = pd.read_csv(VAL_PATH)
test_df = pd.read_csv(TEST_PATH)

# Combine train + val
train_df = pd.concat([train_df, val_df], axis=0).reset_index(drop=True)

# ============================
# 🎯 Separate Features & Labels
# ============================
X_train = train_df.drop(["condition", "severity"], axis=1)
y_cond_train = train_df["condition"]
y_sev_train = train_df["severity"]

X_test = test_df.drop(["condition", "severity"], axis=1)
y_cond_test = test_df["condition"]
y_sev_test = test_df["severity"]

# ============================
# 🔄 Encoding
# ============================
X_train = pd.get_dummies(X_train)
X_test = pd.get_dummies(X_test)

# Align columns
X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

# Save schema
joblib.dump(X_train.columns.tolist(), "model/feature_columns.pkl")

# ============================
# 🔴 Severity → Numeric
# ============================
severity_map = {
    "MILD": 20,
    "MODERATE": 50,
    "SEVERE": 90
}

y_sev_train_num = y_sev_train.map(severity_map)
y_sev_test_num = y_sev_test.map(severity_map)

# ============================
# 🔵 CONDITION MODEL (IMPROVED)
# ============================
condition_model = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    min_samples_split=5,
    random_state=42
)

condition_model.fit(X_train, y_cond_train)

cond_preds = condition_model.predict(X_test)
cond_acc = accuracy_score(y_cond_test, cond_preds)

# ============================
# 🟣 SEVERITY MODEL (STABLE)
# ============================
severity_model = GradientBoostingRegressor(
    n_estimators=150,
    learning_rate=0.1,
    random_state=42
)

severity_model.fit(X_train, y_sev_train_num)

sev_preds = severity_model.predict(X_test)

mse = mean_squared_error(y_sev_test_num, sev_preds)
mae = mean_absolute_error(y_sev_test_num, sev_preds)

# ============================
# 💾 Save Models
# ============================
joblib.dump(condition_model, "model/condition_model.pkl")
joblib.dump(severity_model, "model/severity_model.pkl")

# ============================
# 📊 Output
# ============================
print("\n📊 FINAL MODEL PERFORMANCE")
print(f"✅ Condition Accuracy : {cond_acc:.2f}")
print(f"✅ Severity MSE       : {mse:.2f}")
print(f"✅ Severity MAE       : {mae:.2f}")
print("✅ Models saved successfully")