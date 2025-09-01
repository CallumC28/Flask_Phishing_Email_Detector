from __future__ import annotations
import os
import json
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.wsgi import WSGIMiddleware

from flask import Flask, render_template, request as flask_request

# Config & paths
HERE = Path(__file__).parent
DEFAULT_MODEL_DIR = HERE / "saved_model"  # place your fine-tuned model here
MODEL_DIR = Path(os.getenv("MODEL_DIR", str(DEFAULT_MODEL_DIR)))

# Lazy model cache (warm in memory on first call)
_tokenizer = None
_model = None
_label_map = {0: "legitimate", 1: "phishing"}


def _load_model_if_available() -> bool:
    global _tokenizer, _model, _label_map
    if _model is not None:
        return True

    if MODEL_DIR.exists() and (MODEL_DIR / "config.json").exists():
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
        try:
            m = getattr(_model.config, "id2label", None)
            if m:
                # If labels are default (LABEL_0/1), coerce to human-friendly names
                vals = {v.upper() for v in m.values()}
                if vals == {"LABEL_0", "LABEL_1"}:
                    _label_map = {0: "legitimate", 1: "phishing"}
                else:
                    _label_map = m  # type: ignore
        except Exception:
            pass
        _model.eval()
        return True
    return False


def _predict_with_model(text: str) -> dict:
    """Return phishing probability & label using the HF model if present; fall back to heuristics."""
    if _load_model_if_available():
        import torch
        with torch.no_grad():
            enc = _tokenizer(text, return_tensors="pt", truncation=True, padding=True)  # type: ignore
            out = _model(**enc)  # type: ignore
            probs = out.logits.softmax(dim=1)[0].tolist()
            phishing_p = float(probs[1]) if len(probs) > 1 else 0.0
            legit_p = float(probs[0]) if len(probs) > 0 else (1.0 - phishing_p)
            max_idx = int(probs.index(max(probs))) if probs else 1
            label = _label_map.get(max_idx, "phishing" if phishing_p >= 0.5 else "legitimate")
            return {
                "phishing_probability": phishing_p,
                "legitimate_probability": legit_p,
                "label": label,
                "engine": "BERT_model"
            }

    #Heuristic fallback
    text_lower = text.lower()
    bad_signals = [
        "verify your account", "urgent", "password", "bank", "suspend",
        "reset", "confirm", "click here", "login now", "congratulations",
        "gift card", "bitcoin", "wire transfer", "invoice attached",
    ]
    score = sum(term in text_lower for term in bad_signals) / max(1, len(bad_signals))
    ph = round(min(0.95, 0.2 + score), 3)
    return {
        "phishing_probability": ph,
        "legitimate_probability": round(1 - ph, 3),
        "label": "phishing" if score >= 0.35 else "legitimate",
        "engine": "heuristic"
    }


# FastAPI app (JSON API)
app = FastAPI(title="Phishing Email Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    present = MODEL_DIR.exists() and (MODEL_DIR / "config.json").exists()
    model_name = None
    engine = "heuristic"
    try:
        if _load_model_if_available():
            engine = "BERT_model"
            model_name = getattr(getattr(_model, "config", None), "_name_or_path", None)
    except Exception:
        pass
    return {
        "ok": True,
        "model_present": present,
        "engine": engine,
        "model_name": model_name,
        "model_dir": str(MODEL_DIR),
        "files": sorted([p.name for p in MODEL_DIR.glob("*")]) if present else []
    }



@app.post("/api/predict")
async def predict(request: Request):
    try:
        body = await request.json()
        text = (body.get("text") or "").strip()
    except json.JSONDecodeError:
        text = ""

    if not text:
        return JSONResponse({"error": "Missing 'text' in request body."}, status_code=400)

    result = _predict_with_model(text)
    return JSONResponse(result)


# Flask app
flask_app = Flask(
    __name__,
    template_folder=str(HERE / "templates"),
    static_folder=str(HERE / "styles")
)


@flask_app.get("/")
def ui_home():
    return render_template("index.html")


@flask_app.post("/scan")
def ui_scan():
    text = (flask_request.form.get("text") or "").strip()
    if not text:
        return render_template("index.html", error="Please paste an email body first.")
    result = _predict_with_model(text)
    return render_template("index.html", result=result, prefill=text)


# Mount Flask UI at / (and keep JSON under /api/*)
app.mount("/", WSGIMiddleware(flask_app))

# Run locally: python -m uvicorn api.index:app --reload
