# symptom_extractor.py
# Refined symptom extraction with better NLP coverage
# Offline, rule-based, explainable

import re

def update_symptoms(existing, text):
    text = text.lower()

    # Normalize common phrases
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text)

    # Expanded symptom keyword mapping
    symptom_keywords = {
        "abdominal_pain": [
            "abdominal pain", "stomach pain", "belly pain",
            "pain in abdomen", "pain in stomach", "upper stomach pain",
            "lower abdominal pain"
        ],
        "bloating": [
            "bloating", "gas", "gassy", "fullness",
            "bloated", "feeling full"
        ],
        "diarrhea": [
            "diarrhea", "loose motion", "loose stool",
            "watery stool", "frequent stools"
        ],
        "constipation": [
            "constipation", "hard stool", "difficulty passing stool",
            "not able to pass stool"
        ],
        "acid_reflux": [
            "acid reflux", "heartburn", "acidic",
            "burning chest", "burning sensation",
            "sour taste", "acid coming up"
        ],
        "nausea": [
            "nausea", "feeling sick", "queasy"
        ],
        "vomiting": [
            "vomiting", "throw up", "vomited", "puking"
        ],
        "weight_loss": [
            "weight loss", "lost weight", "losing weight",
            "unintentional weight loss"
        ],
        "blood_in_stool": [
            "blood in stool", "bloody stool", "blood while passing stool",
            "blood in poop", "red stool", "black stool"
        ],
        "fever": [
            "fever", "high temperature", "temperature",
            "feeling feverish"
        ]
    }

    # Detect symptoms (once true, stays true)
    for symptom, keywords in symptom_keywords.items():
        for keyword in keywords:
            if keyword in text:
                existing[symptom] = 1
                break

    # -------- Duration extraction (robust) --------
    # Examples:
    # "for 5 days", "since 2 weeks", "last 10 days"
    day_match = re.search(r"(\d+)\s*day", text)
    week_match = re.search(r"(\d+)\s*week", text)
    month_match = re.search(r"(\d+)\s*month", text)

    if day_match:
        existing["pain_duration_days"] = int(day_match.group(1))
    elif week_match:
        existing["pain_duration_days"] = int(week_match.group(1)) * 7
    elif month_match:
        existing["pain_duration_days"] = int(month_match.group(1)) * 30

    return existing
