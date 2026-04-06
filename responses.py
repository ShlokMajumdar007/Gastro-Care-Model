def generate_response(condition, severity, symptoms):

    response = []

    # ⚠ Disclaimer
    response.append("⚠ This is a first-level medical assessment, not a confirmed diagnosis.")

    # 🧠 Smart condition correction (medical logic override)
    if symptoms["blood_in_stool"] == 1 or symptoms["weight_loss"] == 1:
        condition = "IBD_LIKE"
        severity = "SEVERE"

    elif symptoms["acid_reflux"] == 1:
        condition = "GERD_LIKE"

    elif symptoms["diarrhea"] == 1 and symptoms["bloating"] == 1:
        condition = "IBS_LIKE"

    elif symptoms["vomiting"] == 1 and symptoms["abdominal_pain"] == 1:
        condition = "PEPTIC_ULCER_LIKE"

    elif sum(symptoms.values()) <= 2:
        condition = "LOW_RISK"

    # 🩺 Condition names
    disease_full_names = {
        "GERD_LIKE": "Gastroesophageal Reflux Disease (GERD)",
        "IBS_LIKE": "Irritable Bowel Syndrome (IBS)",
        "IBD_LIKE": "Inflammatory Bowel Disease (IBD)",
        "PEPTIC_ULCER_LIKE": "Peptic Ulcer Disease",
        "LOW_RISK": "General Gastrointestinal Discomfort"
    }

    disease_name = disease_full_names.get(condition, "Gastrointestinal condition")

    response.append(f"🩺 Probable condition identified: {disease_name}.")

    # 🎯 Severity logic improvement
    if symptoms["blood_in_stool"] or symptoms["weight_loss"]:
        severity = "SEVERE"
    elif symptoms["vomiting"] and symptoms["diarrhea"]:
        severity = "MODERATE"

    # 🎯 Severity response
    if severity == "SEVERE":
        response.append("🔴 Symptoms indicate a potentially serious condition.")
        response.append("🚨 Seek immediate medical attention.")

    elif severity == "MODERATE":
        response.append("🟡 Symptoms are moderate.")
        response.append("⚠ Monitor closely and consult a doctor if needed.")

    else:
        response.append("🟢 Symptoms appear mild.")
        response.append("✔ Lifestyle and dietary changes may help.")

    # 💡 Intelligent advice
    if symptoms["diarrhea"] and symptoms["vomiting"]:
        response.append("💧 Risk of dehydration — increase fluid intake.")

    if symptoms["acid_reflux"]:
        response.append("🔥 Avoid spicy, oily, and acidic foods.")

    if symptoms["constipation"]:
        response.append("🥗 Increase fiber intake and hydration.")

    if symptoms["bloating"]:
        response.append("🌿 Avoid gas-producing foods.")

    if symptoms["fever"]:
        response.append("🌡 Monitor temperature regularly.")

    # 🏁 Final note
    response.append("👨‍⚕ If symptoms persist or worsen, consult a healthcare professional.")

    return "\n".join(response)