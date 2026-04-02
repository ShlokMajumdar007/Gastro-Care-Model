import joblib
import numpy as np
from first_aid_logic import first_aid_response

condition_model = joblib.load("condition_model.pkl")
severity_model = joblib.load("severity_model.pkl")

sample = np.array([[1,1,0,0,1,0,0,0,0,0,7]])

condition = condition_model.predict(sample)[0]
severity = severity_model.predict(sample)[0]

print("Probable condition:", condition)
print("Severity:", severity)

print("\nFirst-aid guidance:")
for tip in first_aid_response(condition, severity):
    print("-", tip)
