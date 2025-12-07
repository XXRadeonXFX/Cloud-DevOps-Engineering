from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from typing import Optional
from pathlib import Path
from database import get_connection ,get_history ,save_predictions ,create_table

# APP Initialization
app = FastAPI(title="Sentiment ANalysis API", version="1.0" )

@app.on_event("startup")
def startup():
    create_table()
    print("Database Ready!")

# Get the directory where this app.py file is located
BASE_DIR = Path(__file__).resolve().parent

# Loading Trained Model
classifier = joblib.load(BASE_DIR / 'sentimental_model.pkl')
vectorizer = joblib.load(BASE_DIR / 'vectorizer.pkl')


sentiment_labels = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}

class PredictionRequest(BaseModel):
    text: str
    user_id: Optional[str] = None

class PredictionResponse(BaseModel):
    text: str
    sentiment: str 
    confidence: float

@app.get("/")
def root():
    return {"message" : "Sentiment Analysis API is running",
            "version" : "1.0" ,
            "endpoints": {"POST/predict": "Get sentiment Prediction" }}

@app.post("/predict" ,response_model= PredictionResponse )
def predict_sentiment(request: PredictionRequest):
    try:
        #1. Vectorized input
        text_vectorized = vectorizer.transform([request.text])

        #2 Predict Sentiment
        prediction = classifier.predict(text_vectorized)[0]

        #3 Get Confidence Score
        probabilities = classifier.predict_proba(text_vectorized)
        confidence = float(np.max( probabilities ))

        #4 Map Prediction to label
        sentiment = sentiment_labels[prediction] 
        save_predictions(request.text, sentiment , round(confidence,2))

        return PredictionResponse(
            text=request.text,
            sentiment=sentiment,
            confidence=round(confidence,2)
        )
    except Exception as e:
        print(f"Error during prediction: {str(e)}")  # Log the actual error
        import traceback
        traceback.print_exc()
        return PredictionResponse(
            text=request.text,
            sentiment="Error",
            confidence=0.0
        )



@app.get("/history")
def view_history(limit: int = 10):
    rows = get_history(limit)
    return {
        "total" : len(rows),
        "predictions": rows
    }







