from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
from pydantic import BaseModel
from train import extract_features

app = FastAPI(title="M1 Phishing Link Detector API")

# --- Enable CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    # "*" permits requests from local files (file://), localhost, and 127.0.0.1
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Permits POST, GET, OPTIONS (preflight)
    allow_headers=["*"],  # Permits Content-Type, Authorization, etc.
)

# Load trained model
try:
    model = joblib.load("phishing_model.pkl")
except Exception as e:
    raise RuntimeError(
        "Could not load phishing_model.pkl. Run train.py first!"
    ) from e


class URLRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {"message": "Phishing Detector API is live and CORS enabled!"}


@app.post("/scan")
def scan(payload: URLRequest):
    raw_url = payload.url.strip()
    if not raw_url:
        raise HTTPException(status_code=400, detail="URL cannot be empty.")

    features = extract_features(raw_url)
    features_df = pd.DataFrame([features])

    prob = float(model.predict_proba(features_df)[0][1])

    return {
        "url": raw_url,
        "is_phishing": prob >= 0.60,
        "phishing_probability_pct": round(prob * 100, 2),
        "risk_level": "High"
        if prob >= 0.75
        else ("Medium" if prob >= 0.40 else "Safe"),
        "features": features,
    }