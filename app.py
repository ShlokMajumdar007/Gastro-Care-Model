from flask import Flask, request, jsonify
import joblib
import numpy as np
from first_aid_logic import first_aid_response

app = Flask(__name__)

condition_model = joblib.load("condition_model.pkl")
severity_model = joblib.load("severity_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = np.array([list(data.values())])

    condition = condition_model.predict(features)[0]
    severity = severity_model.predict(features)[0]
    advice = first_aid_response(condition, severity)

    return jsonify({
        "probable_condition": condition,
        "severity": severity,
        "first_aid_guidance": advice,
        "note": "This is not a medical diagnosis."
    })

if __name__ == "__main__":
    app.run(debug=True)
