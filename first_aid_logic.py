def first_aid_response(condition, severity):
    advice = []

    if severity == "SEVERE":
        advice.append("⚠ Seek immediate medical attention.")
        advice.append("Do not self-medicate.")
    elif severity == "MODERATE":
        advice.append("Consult a gastroenterologist soon.")
        advice.append("Light diet and hydration recommended.")
    else:
        advice.append("Monitor symptoms and make lifestyle adjustments.")

    condition_tips = {
        "GERD_LIKE": [
            "Avoid spicy and acidic foods",
            "Eat smaller meals",
            "Do not lie down after eating"
        ],
        "IBS_LIKE": [
            "Increase fiber gradually",
            "Manage stress",
            "Avoid trigger foods"
        ],
        "IBD_LIKE": [
            "Monitor stool changes carefully",
            "Seek specialist care"
        ],
        "PEPTIC_ULCER_LIKE": [
            "Avoid alcohol",
            "Avoid NSAIDs"
        ],
        "LOW_RISK": [
            "Maintain a balanced diet",
            "Stay hydrated"
        ]
    }

    advice.extend(condition_tips.get(condition, []))
    return advice
