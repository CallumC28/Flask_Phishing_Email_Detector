# Phishing Email Detector

A web app to detect phishing emails using a fine-tuned BERT model (Hugging Face Transformers).  
It provides both a clean web interface (Flask UI) and JSON endpoints (FastAPI) so users and developers can easily test email content.

---

## Features
- **Simple web UI** for pasting/scanning email text.
- **FastAPI JSON API** for programmatic access.
- **Heuristic fallback** when no trained model is available.
- **Deployable to Vercel** (serverless) or run locally with Uvicorn.
- **Trained model support** — just drop your Hugging Face `saved_model/` folder in place.

---

## Project Structure
```bash
phishing-detector/
│
├── api/ # Server code (FastAPI + Flask)
│ ├── index.py # Entrypoint with API + UI routes
│ ├── saved_model/ # Fine-tuned model (Hugging Face format)
│ │ ├── config.json
│ │ ├── model.safetensors 
│ │ ├── tokenizer.json
│ │ └── vocab.txt
│ ├── templates/
│ │ └── index.html # Web UI template
│ └── styles/
│ └── style.css # UI styling
│
├── requirements.txt # Python dependencies
├── vercel.json # Vercel routing config
└── README.md # This file
```

---

## API Usage

**Health**
GET /api/health

**Response**
```bash
{
  "ok": true,
  "model_present": true,
  "engine": "hf_model"
}
```

---

**Predict**
```bash
POST /api/predict
Content-Type: application/json

{ "text": "The copy and pasted email." }
```

**Response**
```bash
{
  "phishing_probability": 0.92,
  "legitimate_probability": 0.08,
  "label": "phishing",
  "engine": "hf_model"
}
```