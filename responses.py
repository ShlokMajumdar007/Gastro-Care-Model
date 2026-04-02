def generate_response(condition, severity):
    # FULL disease names (what you asked for)
    disease_full_names = {
        "GERD_LIKE": "Gastroesophageal Reflux Disease (GERD)",
        "IBS_LIKE": "Irritable Bowel Syndrome (IBS)",
        "IBD_LIKE": "Inflammatory Bowel Disease (IBD)",
        "PEPTIC_ULCER_LIKE": "Peptic Ulcer Disease",
        "LOW_RISK": "No specific gastrointestinal disease identified"
    }

    response = []

    # Safety disclaimer
    response.append(
        "⚠ This is a first-level medical assessment, not a confirmed diagnosis."
    )

    # FULL disease name output
    disease_name = disease_full_names.get(
        condition, "Gastrointestinal condition"
    )
    response.append(
        f"🩺 Probable condition identified: {disease_name}."
    )

    # Severity explanation
    if severity == "SEVERE":
        response.append(
            "The symptoms suggest a potentially serious condition."
        )
        response.append(
            "Immediate medical consultation is strongly recommended."
        )
    elif severity == "MODERATE":
        response.append(
            "The symptoms indicate a moderate condition."
        )
        response.append(
            "Consulting a gastroenterologist soon is advised."
        )
    else:
        response.append(
            "The symptoms appear mild at this stage."
        )
        response.append(
            "Lifestyle and dietary changes may help."
        )

    # First-aid style guidance
    advice = {
        "GERD_LIKE": [
            "Avoid spicy, oily, and acidic foods",
            "Eat smaller and frequent meals",
            "Do not lie down immediately after eating"
        ],
        "IBS_LIKE": [
            "Manage stress levels",
            "Avoid trigger foods",
            "Maintain a regular diet"
        ],
        "IBD_LIKE": [
            "Monitor symptoms closely",
            "Do not delay professional medical care"
        ],
        "PEPTIC_ULCER_LIKE": [
            "Avoid alcohol and smoking",
            "Avoid painkillers unless prescribed"
        ],
        "LOW_RISK": [
            "Maintain a balanced diet",
            "Stay hydrated"
        ]
    }

    for tip in advice.get(condition, []):
        response.append(f"• {tip}")

    response.append(
        "If symptoms persist or worsen, please consult a qualified healthcare professional."
    )

    return "\n".join(response)
