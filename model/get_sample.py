
import os
import json
import pandas as pd

from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "creditcard.csv")

data = pd.read_csv(DATA_PATH)

# Recreate the same stratified test split used during training
_, test_data = train_test_split(
    data,
    test_size=0.2,
    random_state=42,
    stratify=data["Class"]
)

# Select one real fraudulent transaction from the test set
sample = test_data[test_data["Class"] == 1].iloc[0]

payload = sample.drop("Class").to_dict()

print("Expected class: FRAUD (1)")
print("\nCopy this JSON into Swagger:")
print(json.dumps(payload, indent=2))
