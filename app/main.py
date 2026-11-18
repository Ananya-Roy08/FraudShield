
import os
import joblib
import pandas as pd

from fastapi import FastAPI
from app.schemas import TransactionInput

app = FastAPI(
    title="FraudShield API",
    description="ML-Based Financial Transaction Fraud Detection System",
    version="1.0.0"
)

# Load the trained machine learning model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "fraud_model.joblib")

model = joblib.load(MODEL_PATH)


# Endpoint 1: Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "FraudShield",
        "version": "1.0.0",
        "model_loaded": True
    }


# Endpoint 2: Fraud prediction
@app.post("/predict")
def predict_transaction(transaction: TransactionInput):

    # Convert transaction into a DataFrame
    features = pd.DataFrame(
        [transaction.model_dump()],
        columns=model.feature_names_in_
    )

    # Predict transaction
    prediction = int(model.predict(features)[0])
    fraud_probability = float(model.predict_proba(features)[0][1])

    return {
        "prediction": prediction,
        "result": (
            "Fraudulent Transaction"
            if prediction == 1
            else "Legitimate Transaction"
        ),
        "fraud_probability": round(fraud_probability, 4)
    }


# Endpoint 3: Model information
@app.get("/model-info")
def model_info():
    return {
        "model_name": "FraudShield Random Forest",
        "algorithm": "Random Forest Classifier",
        "model_status": "Loaded successfully",
        "version": "1.0.0",
        "features": 30
    }
