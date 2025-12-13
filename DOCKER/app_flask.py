from flask import Flask, request, jsonify
import joblib
import numpy as np
from pathlib import Path
from database import get_connection, get_history, save_prediction, create_table

# Initialize Flask app
app = Flask(__name__)

# Load model and vectorizer
BASE_DIR = Path(__file__).resolve().parent
classifier = joblib.load(BASE_DIR / "sentimental_model.pkl")
vectorizer = joblib.load(BASE_DIR / "vectorizer.pkl")

sentiment_labels = {0: "Negative", 1: "Neutral", 2: "Positive"}


# -------------------------------
# Startup Hook: Create DB Table
# -------------------------------
@app.before_first_request
def startup():
    create_table()
    print("Database Ready!")


# -------------------------------
# Root Endpoint
# -------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Sentiment Analysis API is running",
        "version": "1.0",
        "endpoints": {
            "POST /predict": "Get sentiment prediction",
            "GET /history": "View last predictions"
        }
    })


# -------------------------------
# Predict Endpoint
# -------------------------------
@app.route("/predict", methods=["POST"])
def predict_sentiment():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' in request"}), 400

        text = data["text"]

        # 1. Vectorize input
        text_vec = vectorizer.transform([text])

        # 2. Predict
        prediction = classifier.predict(text_vec)[0]

        # 3. Confidence Score
        probabilities = classifier.predict_proba(text_vec)
        confidence = float(np.max(probabilities))

        # 4. Convert Prediction to Label
        sentiment = sentiment_labels[prediction]

        # 5. Save to DB
        save_prediction(text, prediction, round(confidence, 2))

        return jsonify({
            "text": text,
            "sentiment": sentiment,
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "text": text,
            "sentiment": "Error",
            "confidence": 0.0
        }), 500


# -------------------------------
# History Endpoint
# -------------------------------
@app.route("/history", methods=["GET"])
def view_history():
    limit = int(request.args.get("limit", 10))
    rows = get_history(limit)

    formatted = [
        {
            "id": r[0],
            "text": r[1],
            "sentiment": r[2],
            "confidence": r[3],
            "timestamp": r[4]
        }
        for r in rows
    ]

    return jsonify({
        "total": len(rows),
        "predictions": formatted
    })


# Run App
if __name__ == "__main__":
    app.run(debug=True)
