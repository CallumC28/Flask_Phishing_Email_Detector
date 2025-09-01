# Phishing Email Detector

A web app to detect phishing emails using a fine-tuned BERT model (Hugging Face Transformers).  
It provides both a clean web interface (Flask UI) and JSON endpoints (FastAPI) so users and developers can easily test email content.

---

## Features
- **Simple web UI** for pasting/scanning email text.
- **FastAPI JSON API** for programmatic access.
- **Heuristic fallback** when no trained model is available.
- **Locally run** with Uvicorn.
- **Trained model support** — just drop your Hugging Face `saved_model/` folder in place.

---

## Project Structure
```bash
phishing-detector/
│
├── api/ # Server code (FastAPI + Flask)
│ ├── index.py # Entrypoint with API + UI routes
│ ├── saved_model/ # Fine-tuned model (Hugging face) made from another repo of mine (Phishing-Email-Detector-In-Progress)
│ │ ├── config.json
│ │ ├── model.safetensors 
│ │ ├── tokenizer.json
│ │ └── vocab.txt
│ ├── templates/
│ │ └── index.html # Web UI template
│ └── styles/
│ └── style.css # UI styling
│ └── favicon.ico # letter logo
└── README.md # This file
```

---
