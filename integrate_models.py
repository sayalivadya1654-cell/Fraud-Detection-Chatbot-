import joblib
import os
import pandas as pd

# ----------- Model paths -------------
credit_model_path = r"D:\Projects\all_fraud_detection\model\credit_fraud_model.pkl"
upi_model_path = r"D:\Projects\all_fraud_detection\model\upi_fraud_model.pkl"
url_model_path = r"D:\Projects\all_fraud_detection\model\url_fraud_rf_gui_model.pkl"

def load_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")
    return joblib.load(model_path)

try:
    # Load models
    credit_model = load_model(credit_model_path)
    upi_model = load_model(upi_model_path)
    url_model = load_model(url_model_path)

    print("All models loaded successfully!\n")

    # Print expected features to debug
    print("Credit model expects:", list(credit_model.feature_names_in_))
    print("UPI model expects:", list(upi_model.feature_names_in_))
    print("URL model expects:", list(url_model.feature_names_in_))

    # Dummy inputs (you must update these based on the above feature names)
    credit_input = pd.DataFrame([[2000, 1, 0, 0, 1, 1, 0, 1, 0]], columns=credit_model.feature_names_in_)
    upi_input = pd.DataFrame([[1, 0, 1, 0, 5000, 2]], columns=upi_model.feature_names_in_)
    url_input = pd.DataFrame([[0.6, 1, 2]], columns=url_model.feature_names_in_)

    # Predictions
    credit_pred = credit_model.predict(credit_input)
    upi_pred = upi_model.predict(upi_input)
    url_pred = url_model.predict(url_input)

    # Results
    print("Credit Fraud Prediction:", "FRAUD" if credit_pred[0] == 1 else "SAFE")
    print("UPI Fraud Prediction   :", "FRAUD" if upi_pred[0] == 1 else "SAFE")
    print("URL Scam Prediction    :", "SCAM" if url_pred[0] == 1 else "SAFE")

except Exception as e:
    print("Error while loading or predicting:", str(e))
