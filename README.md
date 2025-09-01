# Phishing Email Detector – Flask Web App

A **simple web application** that helps you check if an email is **phishing or legitimate** using an AI model.  
This project was created for personal learning, but it can also be used as a handy tool to analyse suspicious emails.

You paste an email’s text into the app, and it will predict whether the email is **“phishing” or “legitimate”** along with confidence scores.  

---

## Features

- **Easy Web Interface** – Paste email text and click “Scan” to get results.  
- **AI-Powered Detection** – Uses a fine-tuned **BERT** model to classify emails.  
- **Probability Scores** – See how confident the model is (e.g., *92% phishing, 8% legitimate*).  
- **Fallback Mode** – If the model isn’t available, the app uses a simple keyword-based check.  
- **Private & Local** – Runs only on your computer; no data is sent online.  

---

## How It Works (Non-Technical)

1. **You paste email text** into the text box.  
2. The app uses an **AI model** (trained on phishing emails) to analyse it.  
3. It outputs:
   - **Phishing Probability** (e.g., 0.92 → 92%)  
   - **Legitimate Probability** (e.g., 0.08 → 8%)  
   - A clear **label**: ✅ Legitimate or 🛑 Phishing  
4. If no model is available, it falls back to **keyword checks** (like spotting “urgent”, “reset password”).  

---

## 📂 Project Structure

```bash
Flask_Phishing_Email_Detector/
├── api/ 
│   ├── index.py          # Main Flask/FastAPI app
│   ├── saved_model/      # <--- Place your trained model here
│   ├── templates/       
│   │   └── index.html    # Web interface
│   └── styles/ 
│       └── style.css     # Page styling
└── requirements.txt      # Python dependencies
```

---

## Get the Model

1. **Get the Model**  
   This app needs a trained model from my other repo:  
   👉 [Phishing-Email-Detector-In-Progress](https://github.com/CallumC28/Phishing-Email-Detector-In-Progress)

   Download the `saved_model` folder made from that project when you train it on a dataset.
   Copy it into this repo’s `api/` folder.  

   After this, you should have:

   ```bash
   api/saved_model/config.json
   api/saved_model/pytorch_model.bin (or .safetensors)
   api/saved_model/tokenizer.json
   ...
   ```

   *(If you skip this, the app will still work using simple keyword checks, but results will be less accurate.)*

2. **Install Requirements**  
   From inside the project folder, run:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the App**  
   Start the server with:

   ```bash
   python -m uvicorn api.index:app --reload
   ```

4. **Open in Browser**  
   Go to [http://localhost:8000](http://localhost:8000) and you’ll see the Phishing Email Detector.

---

## Using the App

- Paste an email’s text into the box.  
- Click **Scan**.  
- View results:  
  - ✅ **Legitimate** → email seems safe.  
  - 🛑 **Phishing** → email looks dangerous.  
  - Percentages show how confident the model is.  

**Example:**

```yaml
Phishing Probability: 92%
Legitimate Probability: 8%
Label: Phishing
Engine: hf_model
```

---

## 📸 Screenshots

*Here’s what it looks like in action:*  
*(Replace this placeholder with a real screenshot from your app)*

---

## 🛠️ API Endpoints

- **Health Check** → `GET /api/health`  
  Returns JSON with model status.

- **Predict** → `POST /api/predict`  
  Example request:

  ```json
  { "text": "Dear user, click here to reset your password" }
  ```

  Example response:

  ```json
  {
    "phishing_probability": 0.92,
    "legitimate_probability": 0.08,
    "label": "phishing",
    "engine": "hf_model"
  }
  ```

  ---