import random
import pandas as pd

def generate_sample():
    symptoms = {
        "abdominal_pain": random.randint(0, 1),
        "bloating": random.randint(0, 1),
        "diarrhea": random.randint(0, 1),
        "constipation": random.randint(0, 1),
        "acid_reflux": random.randint(0, 1),
        "nausea": random.randint(0, 1),
        "vomiting": random.randint(0, 1),
        "weight_loss": random.randint(0, 1),
        "blood_in_stool": random.randint(0, 1),
        "fever": random.randint(0, 1),
        "pain_duration_days": random.randint(1, 60)
    }

    if symptoms["blood_in_stool"] or symptoms["weight_loss"]:
        condition, severity = "IBD_LIKE", "SEVERE"
    elif symptoms["acid_reflux"]:
        condition, severity = "GERD_LIKE", "MILD"
    elif symptoms["diarrhea"] and symptoms["bloating"]:
        condition, severity = "IBS_LIKE", "MODERATE"
    elif symptoms["vomiting"] and symptoms["abdominal_pain"]:
        condition, severity = "PEPTIC_ULCER_LIKE", "MODERATE"
    else:
        condition, severity = "LOW_RISK", "MILD"

    return list(symptoms.values()) + [condition, severity]

columns = [
    "abdominal_pain","bloating","diarrhea","constipation","acid_reflux",
    "nausea","vomiting","weight_loss","blood_in_stool","fever",
    "pain_duration_days","condition","severity"
]

data = [generate_sample() for _ in range(1200)]
df = pd.DataFrame(data, columns=columns)
df.to_csv("data/gastro_dataset.csv", index=False)

print("✅ Dataset generated")
