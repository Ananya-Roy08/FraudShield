
import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "creditcard.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "fraud_model.joblib")

# Load dataset
print("Loading dataset...")
data = pd.read_csv(DATA_PATH)

print("Dataset shape:", data.shape)
print("Class distribution:")
print(data["Class"].value_counts())

# Separate features and target
X = data.drop("Class", axis=1)
y = data["Class"]

# Split dataset while preserving fraud/legitimate proportions
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train Random Forest model
print("\nTraining Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))

print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))

print("ROC-AUC Score:")
print(roc_auc_score(y_test, probabilities))

# Save trained model
joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully at:", MODEL_PATH)

