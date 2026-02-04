# create_dummy_models.py

import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
import os

os.makedirs("models", exist_ok=True)

# Create dummy dataset and model for UPI
X, y = make_classification(n_samples=100, n_features=5, random_state=42)
model_upi = LogisticRegression().fit(X, y)
with open("models/upi_model.pkl", "wb") as f:
    pickle.dump(model_upi, f)

# Create dummy model for Credit Card
model_credit = LogisticRegression().fit(X, y)
with open("models/credit_model.pkl", "wb") as f:
    pickle.dump(model_credit, f)

# Create dummy model for URL
model_url = LogisticRegression().fit(X, y)
with open("models/url_model.pkl", "wb") as f:
    pickle.dump(model_url, f)

print("✅ Dummy models created and saved to 'models/' folder.")
