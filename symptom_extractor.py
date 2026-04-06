import re

def update_symptoms(existing, text):
    text = text.lower()

    # Normalize text
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text)

    # ============================
    # 🧠 Symptom keyword mapping
    # ============================
    symptom_keywords = {
        "abdominal_pain": [
            "abdominal pain", "stomach pain", "belly pain",
            "pain in abdomen", "pain in stomach", "cramps"
        ],
        "bloating": [
            "bloating", "bloated", "gas", "gassy", "fullness"
        ],
        "diarrhea": [
            "diarrhea", "loose motion", "loose stool",
            "watery stool", "frequent stools"
        ],
        "constipation": [
            "constipation", "hard stool", "difficulty passing stool"
        ],
        "acid_reflux": [
            "acid reflux", "heartburn", "burning chest",
            "acidic", "sour taste"
        ],
        "nausea": [
            "nausea", "queasy", "feeling sick"
        ],
        "vomiting": [
            "vomiting", "vomit", "threw up", "puking"
        ],
        "weight_loss": [
            "weight loss", "losing weight", "lost weight"
        ],
        "blood_in_stool": [
            "blood in stool", "bloody stool", "blood in poop",
            "red stool", "black stool"
        ],
        "fever": [
            "fever", "high temperature", "feverish"
        ]
    }

    # ============================
    # ✅ Detect symptoms
    # ============================
    for symptom, keywords in symptom_keywords.items():
        for keyword in keywords:
            if keyword in text:
                existing[symptom] = 1
                break

    # ============================
    # ⏱ Duration extraction
    # ============================
    day_match = re.search(r"(\d+)\s*day", text)
    week_match = re.search(r"(\d+)\s*week", text)
    month_match = re.search(r"(\d+)\s*month", text)

    if day_match:
        existing["pain_duration_days"] = int(day_match.group(1))
    elif week_match:
        existing["pain_duration_days"] = int(week_match.group(1)) * 7
    elif month_match:
        existing["pain_duration_days"] = int(month_match.group(1)) * 30

    # ============================
    # 🔥 Intensity detection (NEW)
    # ============================
    if any(word in text for word in ["severe", "very bad", "extreme"]):
        existing["pain_duration_days"] += 5

    if any(word in text for word in ["mild", "slight"]):
        existing["pain_duration_days"] = max(1, existing["pain_duration_days"] - 2)

    return existing