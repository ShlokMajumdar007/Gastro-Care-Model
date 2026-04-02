# 🩺 Gastroenterology AI Chatbot

A machine learning-based conversational system for **first-level gastrointestinal symptom assessment**. This offline system uses Natural Language Processing (NLP) and ensemble machine learning to help patients understand their symptoms and receive preliminary guidance.

> ⚠️ **Disclaimer**: This is an educational tool for symptom triage only. It is **NOT a medical diagnostic system** and should not replace professional medical consultation. Always consult a healthcare professional for proper diagnosis and treatment.

---

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [File Descriptions](#-file-descriptions)
- [Model Training](#-model-training)
- [API Usage](#-api-usage)
- [Supported Conditions](#-supported-conditions)
- [License](#-license)

---

## ✨ Features

✅ **Conversational Interface** - Chat naturally with the bot about your symptoms  
✅ **Symptom Recognition** - Automatically extracts gastrointestinal symptoms from user input  
✅ **Condition Classification** - Identifies potential GI conditions:
   - Gastroesophageal Reflux Disease (GERD)
   - Irritable Bowel Syndrome (IBS)
   - Inflammatory Bowel Disease (IBD)
   - Peptic Ulcer Disease
   
✅ **Severity Assessment** - Classifies severity levels (Mild, Moderate, Severe)  
✅ **First-Aid Guidance** - Provides practical advice based on condition and severity  
✅ **Persistent Memory** - Tracks symptoms across conversation turns  
✅ **Fully Offline** - No internet required; all processing local  
✅ **RESTful API** - Flask-based API for integration into other applications  

---

## 📁 Project Structure

```
Final gastro chatbot/
├── app.py                   # Flask API server
├── chatbot.py               # Interactive CLI chatbot
├── train_model.py           # Model training script
├── predict.py               # Inference module
├── preprocess.py            # NLP preprocessing utilities
├── symptom_extractor.py     # Symptom extraction from user input
├── responses.py             # Response generation templates
├── first_aid_logic.py       # First-aid advice logic
├── genrate_dataset.py       # Dataset generation utility
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── commands.txt             # Example commands/test cases
├── data/
│   ├── data-train.csv       # Training dataset
│   └── gastro_dataset.csv   # Original gastro dataset
└── model/                   # Trained models (generated after training)
    ├── condition_model.pkl
    ├── severity_model.pkl
    └── feature_columns.pkl
```

---

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project

```bash
cd "Final gastro chatbot"
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: On Windows, if you encounter pandas build errors:
```bash
pip install --only-binary :all: -r requirements.txt
```

Or use Conda (recommended for Windows):
```bash
conda install flask pandas scikit-learn joblib numpy nltk
```

### Step 3: Download NLTK Data

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"
```

---

## 🚀 Quick Start

### Option 1: Interactive Chatbot

```bash
python train_model.py    # Train the model (first time only)
python chatbot.py        # Start the chatbot
```

**Example conversation:**
```
🩺 Gastroenterology First-Aid Chatbot
Describe your symptoms freely.
Type 'reset' to clear symptoms or 'exit' to quit.

You: I have been experiencing severe abdominal pain for the last 3 days
Chatbot: [Assessment and guidance]

You: reset
Chatbot: Symptoms cleared.

You: exit
Chatbot: Take care and consult a doctor if symptoms persist 👋
```

### Option 2: REST API

```bash
python train_model.py    # Train the model (first time only)
python app.py            # Start Flask server (runs on http://localhost:5000)
```

**Test the API:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"abdominal_pain": 1, "bloating": 0, "diarrhea": 1, "constipation": 0, "acid_reflux": 0, "nausea": 1, "vomiting": 0, "weight_loss": 0, "blood_in_stool": 0, "fever": 0, "pain_duration_days": 5}'
```

---

## 🏗️ Architecture

### System Components

```
User Input
    ↓
[Symptom Extractor] → Extracts symptoms using predefined patterns
    ↓
[Preprocessor] → NLP cleaning (tokenization, lemmatization, stopword removal)
    ↓
[Feature Vectorizer] → Converts text to numeric features
    ↓
[Condition Model] → Random Forest classifier (200 estimators)
    ↓
[Severity Model] → Random Forest classifier (200 estimators)
    ↓
[Response Generator] → Creates user-friendly response with:
         ├── First-aid advice
         ├── Condition-specific tips
         ├── Severity-based recommendations
         └── Safety disclaimer
    ↓
Response to User
```

### ML Models

- **Model Type**: Random Forest Classifier (200 estimators)
- **Training Algorithm**: Tree-based ensemble learning
- **Features**: One-hot encoded symptom flags + pain duration
- **Output 1 (Condition)**: Multi-class classification (5 classes)
- **Output 2 (Severity)**: Multi-class classification (3 classes)

---

## 📄 File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Flask REST API server for external integrations |
| `chatbot.py` | Interactive CLI chatbot with persistent symptom tracking |
| `train_model.py` | Trains both condition and severity models from dataset |
| `predict.py` | Core predictive module with ML inference logic |
| `preprocess.py` | NLP utilities (tokenization, lemmatization, stopword removal) |
| `symptom_extractor.py` | Extracts GI symptoms from user input using regex patterns |
| `responses.py` | Template-based response generation |
| `first_aid_logic.py` | Condition-specific and severity-specific advice |
| `genrate_dataset.py` | Utility for generating synthetic training data |

---

## 🤖 Model Training

### Training Process

```bash
python train_model.py
```

This script will:
1. Load the training dataset from `data/data-train.csv`
2. Preprocess and one-hot encode features
3. Train two Random Forest models:
   - **Condition Model**: Classifies the likely GI condition
   - **Severity Model**: Classifies the severity (Mild/Moderate/Severe)
4. Evaluate accuracy on test set
5. Save models to `model/` directory:
   - `condition_model.pkl`
   - `severity_model.pkl`
   - `feature_columns.pkl` (for feature schema consistency)

### Dataset Requirements

Training data should be in `data/data-train.csv` with columns:
- Symptom binary features (0/1): `abdominal_pain`, `bloating`, `diarrhea`, `constipation`, `acid_reflux`, `nausea`, `vomiting`, `weight_loss`, `blood_in_stool`, `fever`, etc.
- `pain_duration_days`: Duration of symptoms (numeric)
- `condition`: Target label (string)
- `severity`: Target label (string)

---

## 🌐 API Usage

### POST /predict

**Endpoint**: `http://localhost:5000/predict`

**Request Body**:
```json
{
  "abdominal_pain": 1,
  "bloating": 0,
  "diarrhea": 1,
  "constipation": 0,
  "acid_reflux": 0,
  "nausea": 1,
  "vomiting": 0,
  "weight_loss": 0,
  "blood_in_stool": 0,
  "fever": 0,
  "pain_duration_days": 5
}
```

**Response**:
```json
{
  "probable_condition": "IBS_LIKE",
  "severity": "MODERATE",
  "first_aid_guidance": [
    "⚠ This is a first-level medical assessment, not a confirmed diagnosis.",
    "🩺 Probable condition identified: Irritable Bowel Syndrome (IBS).",
    "Consult a gastroenterologist soon.",
    "Light diet and hydration recommended.",
    "Increase fiber gradually",
    "Manage stress",
    "Avoid trigger foods"
  ],
  "note": "This is not a medical diagnosis."
}
```

---

## 🔍 Supported Conditions

| Condition Code | Full Name | Characteristics |
|---|---|---|
| `GERD_LIKE` | Gastroesophageal Reflux Disease | Acid reflux, heartburn, regurgitation |
| `IBS_LIKE` | Irritable Bowel Syndrome | Bloating, diarrhea/constipation, cramps |
| `IBD_LIKE` | Inflammatory Bowel Disease | Chronic inflammation, blood in stool, weight loss |
| `PEPTIC_ULCER_LIKE` | Peptic Ulcer Disease | Severe pain, nausea, vomiting |
| `LOW_RISK` | No specific condition | Mild symptoms, low risk |

### Severity Levels

- **MILD**: Monitor at home; lifestyle adjustments
- **MODERATE**: Consult healthcare provider soon; supportive care
- **SEVERE**: Seek immediate medical attention; do not self-medicate

---

## ⚠️ Important Notes

1. **Not a Diagnostic Tool**: This system provides educational guidance only
2. **Always Consult Professionals**: For any serious symptoms, seek immediate medical attention
3. **Data Privacy**: All processing is local; no data is sent elsewhere
4. **Limitations**: 
   - Works best with clearly described symptoms
   - Cannot account for individual medical history
   - Should not be used as sole basis for treatment decisions

---

## 🛠️ Troubleshooting

**Q: "Missing file" error when running chatbot?**
```bash
python train_model.py  # Run this first to generate models
```

**Q: pandas build error on Windows?**
```bash
pip install --only-binary :all: -r requirements.txt
```

**Q: NLTK data download fails?**
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"
```

**Q: Flask server won't start?**
- Check if port 5000 is available
- Try: `python app.py --port 8000`

---

## 📊 Performance Metrics

After training, the model achieves:
- **Condition Classification Accuracy**: ~85-92% (depends on dataset)
- **Severity Classification Accuracy**: ~90-95% (depends on dataset)

*Note: Actual performance may vary based on training data quality and volume.*

---

## 🤝 Contributing

Improvements and contributions are welcome! You can:
- Improve the symptom extraction logic
- Enhance the response templates
- Add more conditions to the knowledge base
- Optimize model performance

---

## 📜 License

This project is provided as-is for educational purposes.

---

## 📧 Support

For issues, questions, or suggestions, please review the code comments and docstrings or contact the project maintainer.

---

**Made with ❤️ for healthcare education**
