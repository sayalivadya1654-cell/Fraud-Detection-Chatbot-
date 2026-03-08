import streamlit as st  
from deep_translator import GoogleTranslator
from gtts import gTTS
from playsound import playsound
import os
import uuid
import time
import random
from datetime import datetime
import re
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
# ================== XAI SETUP ==================
import shap  # if not already imported

# Global SHAP variables
shap_explainers = {}    # will store explainer per category
shap_values_dict = {}   # will store SHAP values per category
# =================================================

# ================== XAI IMPORTS ==================
from XAI.SHAP.shap_utils import shap_global_explain
# =================================================

# ===== DB imports =====
from fraud_detection import init_db, save_user, save_transaction

# ===== Email alert import =====
from send_email import send_alert

# ---------------- STREAMLIT PAGE CONFIG ----------------
st.set_page_config(page_title="Fraud Chatbot", layout="wide")

# --- Theme and CSS ---
st.markdown("""<style>
.stApp { background: linear-gradient(135deg, #e0f2f1, #f1f8e9, #e3f2fd); font-family: 'Segoe UI', sans-serif; }
.stApp, .stApp * { color: #222222 !important; }
[data-testid="stSidebar"] { background: linear-gradient(135deg, #dcedc8, #bbdefb); color: #222222 !important; }
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 { color: #222222 !important; font-weight: 600; }
div.stButton > button { background: linear-gradient(135deg, #a5d6a7, #90caf9); color: #222222 !important; border: none; border-radius: 10px; padding: 0.6rem 1rem; font-size: 1rem; font-weight: 500; transition: all 0.3s ease; box-shadow: 0px 3px 6px rgba(0,0,0,0.1); }
div.stButton > button:hover { background: linear-gradient(135deg, #90caf9, #a5d6a7); transform: scale(1.05); }
input, select, textarea { background-color: #ffffff !important; border: 1px solid #b0bec5 !important; border-radius: 8px !important; color: #222222 !important; padding: 0.5rem 0.75rem !important; font-family: 'Segoe UI', sans-serif !important; }
.safe-box { background-color: #D4F4DD; padding: 1rem; border-radius: 10px; font-weight: 600; border-left: 6px solid #27AE60; color: #145214; }
.danger-box { background-color: #FFD6D6; padding: 1rem; border-radius: 10px; font-weight: 600; border-left: 6px solid #C0392B; color: #7A1A1A; }
.example-questions { background: linear-gradient(135deg, #EAF2F8, #D6EAF8); padding: 0.8rem; border-radius: 8px; font-size: 0.95rem; font-weight: 500; color: #222222; margin-bottom: 5px; box-shadow: 0px 2px 5px rgba(0,0,0,0.1); transition: all 0.3s ease; }
.example-questions:hover { background: linear-gradient(135deg, #D6EAF8, #AED6F1); transform: scale(1.02); }
.language-selectbox label { color: white !important; font-weight: 600 !important; }
.language-selectbox div[data-baseweb="select"] > div {
    background-color: black !important;
    color: white !important;
    border-radius: 8px !important;
    border: 1px solid #ffffff !important;
}
.language-selectbox div[data-baseweb="select"] * {
    color: white !important;
}
.language-selectbox [role="option"] {
    background-color: black !important;
    color: white !important;
}
</style>""", unsafe_allow_html=True)

# ===== Ensure DB exists =====
init_db()

# ---------------- LANGUAGE SETTINGS ----------------
language_map = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te"
}

def translate(text, lang_code):
    try:
        return GoogleTranslator(source='en', target=lang_code).translate(text)
    except:
        return text

def speak(text, lang_code="en"):
    if text:
        try:
            tts = gTTS(text=text, lang=lang_code)
            filename = f"temp_{uuid.uuid4().hex}.mp3"
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
        except Exception as e:
            print("Error in gTTS:", e)

# ---------------- NEW: ML MODEL INTEGRATION ----------------
# --- Load models ---
MODELS_FOLDER = r"D:\Projects\all_fraud_detection\models"

models = {}

model_files = {
    "upi": "upi_model.pkl",
    "credit": "credit_model.pkl",
    "url": "url_model.pkl"
}

for category, filename in model_files.items():
    try:
        filepath = f"{MODELS_FOLDER}\\{filename}"
        models[category] = joblib.load(filepath)
        print(f"✅ Loaded {category} model")

    except Exception as e:
        print(f"⚠ Failed to load {filename}: {e}")

# --- Compute SHAP AFTER all models loaded ---
shap_explainers = {}
shap_values_dict = {}

dataset_paths = {
    "upi": r"D:\Projects\all_fraud_detection\notebook\upi_combined_dataset.csv",
    "url": r"D:\Projects\all_fraud_detection\notebook\url_fraud_dataset.csv",
    "credit": r"D:\Projects\all_fraud_detection\notebook\credit_combined_dataset.csv"
}

for category_name, model_pipeline in models.items():

    if category_name == "credit":
        continue
    try:
        df_train = pd.read_csv(dataset_paths[category_name])
        df_train.columns = df_train.columns.str.strip().str.lower()

        # Feature engineering
        if category_name == "upi":

            df_train['amount'] = df_train['amount'].fillna(0).astype(float) if 'amount' in df_train else 0
            df_train['sender_len'] = df_train['sender'].fillna('').apply(len) if 'sender' in df_train else 0
            df_train['receiver_len'] = df_train['receiver'].fillna('').apply(len) if 'receiver' in df_train else 0

            df_train['date_numeric'] = pd.to_datetime(df_train['date'], errors='coerce').dt.day.fillna(0).astype(int) if 'date' in df_train else 0

            df_train['time_numeric'] = df_train['time'].fillna('00:00').apply(
                lambda x: int(x.split(':')[0])*60 + int(x.split(':')[1]) if ':' in x else 0
            ) if 'time' in df_train else 0

            feature_cols = ['amount','sender_len','receiver_len','date_numeric','time_numeric']

        elif category_name == "credit":
           df_train['card_length'] = df_train['card_number'].fillna('').apply(len) if 'card_number' in df_train else 0
           df_train['cvv'] = df_train['cvv'].fillna(0).astype(int) if 'cvv' in df_train else 0     

           feature_cols = ['card_length','cvv']

        elif category_name == "url":

            df_train['url_length'] = df_train['url'].fillna('').apply(len)
            df_train['dots_count'] = df_train['url'].fillna('').apply(lambda x: x.count('.'))
            df_train['has_https'] = df_train['url'].fillna('').apply(lambda x: int('https' in x))

            df_train['is_shortened'] = 0
            df_train['entropy_score'] = 0
            df_train['domain_age_months'] = 0
            df_train['blacklist_match'] = 0
            df_train['sender_known'] = 0
            df_train['source_channel'] = 0
            df_train['clicked'] = 0

            feature_cols = [
                "url_length",
                "dots_count",
                "has_https",
                "is_shortened",
                "entropy_score",
                "domain_age_months",
                "blacklist_match",
                "sender_known",
                "source_channel",
                "clicked"
            ]
        # Preprocessing
        preprocessor = list(model_pipeline.named_steps.values())[0]
        X_train = preprocessor.transform(df_train[feature_cols])

        if hasattr(X_train, "toarray"):
            X_train = X_train.toarray()

        X_train = X_train.astype(float)

        # Classifier
        classifier = list(model_pipeline.named_steps.values())[-1]

        explainer = shap.Explainer(classifier, X_train)

        shap_explainers[category_name] = explainer
        shap_values_dict[category_name] = explainer(X_train)

        print(f"✅ SHAP computed for {category_name}")

    except Exception as e:
        print(f"⚠ Failed to compute SHAP for {category_name}: {e}")
                                
def extract_features(inputs, category):

    if category == "upi":
        amount = float(inputs.get("amount", 0))
        sender_len = len(inputs.get("sender", "")) if inputs.get("sender") else 0
        receiver_len = len(inputs.get("receiver", "")) if inputs.get("receiver") else 0
        
        date_input = inputs.get("date")
        date_numeric = int(date_input.strftime("%d")) if date_input else 0
        
        time_input = inputs.get("time", "00:00")
        h, m = map(int, time_input.split(":")) if ":" in time_input else (0, 0)
        time_numeric = h*60 + m
        
        features = [amount, sender_len, receiver_len, date_numeric, time_numeric]
        feature_names = ["amount","sender_len","receiver_len","date_numeric","time_numeric"]
        return features, feature_names

    elif category == "credit":
        card_num = inputs.get("card_number", "")
        cvv = inputs.get("cvv", "")
        return [len(card_num), int(cvv) if cvv.isdigit() else 0], ["card_length","cvv"]

    elif category == "url":

        url = inputs.get("url", "")

        features = [
            len(url),
            url.count("."),
            int("https" in url),
            0,
            0,
            0,
            0,
            0,
            0,
            0
        ]

        feature_names = [
            "url_length",
            "dots_count",
            "has_https",
            "is_shortened",
            "entropy_score",
            "domain_age_months",
            "blacklist_match",
            "sender_known",
            "source_channel",
            "clicked"
        ]

        return features, feature_names

    return [], []
def chatbot_reply(user_query, inputs, category):

    # 🔹 Rule-based override for high amount
    if category == "upi" and inputs.get("amount", 0) > 50000:
        return "🚨 Amount too high! Potential fraud.", False, 95.0

    model = models.get(category)

    if model:
        try:
            features, _ = extract_features(inputs, category)

            # 🔥 IMPORTANT FIX: Create DataFrame with correct column names
            feature_names = model.named_steps['preprocessor'].transformers_[0][2]
            input_df = pd.DataFrame([features], columns=feature_names)

            # 🔹 Prediction
            pred = model.predict(input_df)[0] 

            # 🔹 Risk Score using probability
            if hasattr(model, "predict_proba"):
                prob = model.predict_proba(input_df)[0][1]
                risk_score = round(float(prob) * 100, 2)
            else:
                risk_score = 90.0 if pred == 1 else 10.0

            if pred == 1:
                return "⚠ Fraud Detected by Machine Learning Model.", False, risk_score
            else:
                return "✅ Transaction Safe according to Machine Learning Model.", True, risk_score

        except Exception as e:
            print(f"ML model error for {category}: {e}")
            return "❓ ML Error Occurred.", None, 50.0

    # 🔹 Fallback logic (no model found)
    if category == "upi":
        return "✅ UPI Transaction is Safe.", True, 10.0
    elif category == "credit":
        return "✅ Credit Card Transaction is Safe.", True, 10.0
    elif category == "url":
        return "✅ URL is Safe to Visit.", True, 10.0

    return "❓ Unable to verify transaction.", None, 50.0
# ---------------- COMMON FUNCTIONS ----------------
def store_on_blockchain(txn_id_text, status):
    try:
        fake_tx_hash = "0x" + "".join(random.choices("0123456789abcdef", k=64))
        fake_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return fake_tx_hash, fake_timestamp, "Success"
    except Exception as e:
        return None, None, f"Blockchain Error: {e}"

def is_valid_name(name):
    return bool(re.match(r'^[A-Za-z ]+$', name.strip()))

# ---------------- LOGIN PAGE ----------------
def login_page():
    st.title("🔐 User Login")
    st.markdown('<div class="language-selectbox">', unsafe_allow_html=True)
    selected_language = st.selectbox(
        "🌐 Select Bot Speaking Language",
        list(language_map.keys()),
        key="login_language",
        help="Choose the language the bot will speak in.",
        label_visibility="visible"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.lang_code = language_map[selected_language]
    st.session_state.selected_language_name = selected_language

    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")

    if st.button("Login"):
        if not name or not email or not phone:
            st.warning(translate("Please enter all fields.", st.session_state.lang_code))
        elif not is_valid_name(name):
            st.error(translate("Please enter a valid name using only alphabets and spaces.", st.session_state.lang_code))
        else:
            try:
                user_id = save_user(name, email, phone)
                st.session_state.user_id = user_id
            except Exception as e:
                st.error(f"DB error: {e}")
                return

            st.session_state.user_email = email
            st.session_state.logged_in = True
            st.session_state.user_name = name
            st.session_state.step = 0

# ---------------- CHATBOT INTERFACE ----------------
def chatbot_interface():
    global shap_explainers,shap_values_dict
    lang_code = st.session_state.lang_code
    st.title("💬 " + translate("Multilingual Fraud Detection Chatbot", lang_code))
    
    if st.session_state.step == 0:
        speak(translate(f"Welcome {st.session_state.get('user_name', '')}!", lang_code), lang_code)
        time.sleep(0.5)
        speak(translate("Please choose the fraud type to check.", lang_code), lang_code)
        st.session_state.step = 1

    category = st.radio(translate("Choose Transaction Type", lang_code),
                    ["upi", "credit", "url"], horizontal=True, key="category")
    if category and st.session_state.step == 1:
        speak(translate("Now, please enter all transaction details in the sidebar.", lang_code), lang_code)
        st.session_state.step = 2

    inputs = {}
    with st.sidebar:
        st.header("📋 " + translate("Transaction Details", lang_code))
        if category == "upi":
            inputs["upi_id"] = st.text_input(translate("UPI ID", lang_code))
            inputs["sender"] = st.text_input(translate("Sender Name", lang_code))
            inputs["receiver"] = st.text_input(translate("Receiver Name", lang_code))
            if inputs["sender"] and not is_valid_name(inputs["sender"]):
                st.error(translate("Sender name must contain only alphabets and spaces.", lang_code))
            if inputs["receiver"] and not is_valid_name(inputs["receiver"]):
                st.error(translate("Receiver name must contain only alphabets and spaces.", lang_code))
            inputs["amount"] = st.number_input(translate("Amount", lang_code), min_value=1.0)
            inputs["date"] = st.date_input(translate("Date", lang_code))
            inputs["time"] = st.text_input(translate("Time (HH:MM)", lang_code))
        elif category == "credit":
            inputs["card_number"] = st.text_input(translate("Card Number", lang_code))
            inputs["cvv"] = st.text_input(translate("CVV", lang_code))
        elif category == "url":
            inputs["url"] = st.text_input(translate("Enter URL", lang_code))

        if st.session_state.step == 2:
            if st.button(translate("Details Completed", lang_code)):
                details_filled = False
                if category == "upi":
                    details_filled = all([
                        inputs.get("upi_id"), inputs.get("sender"), inputs.get("receiver"),
                        inputs.get("amount") > 0, inputs.get("date"), inputs.get("time"),
                        is_valid_name(inputs.get("sender", "")), is_valid_name(inputs.get("receiver", ""))])
                elif category == "credit":
                    details_filled = all([inputs.get("card_number"), inputs.get("cvv")])
                elif category == "url":
                    details_filled = bool(inputs.get("url"))

                if details_filled:
                    speak(translate("Details recorded. Now type your question in the box below.", lang_code), lang_code)
                    st.session_state.stored_inputs = inputs.copy()
                    st.session_state.step = 3
                else:
                    st.warning(translate("Please fill in all details correctly.", lang_code))

    col1, col2 = st.columns([2, 1])

    with col2:
        if st.session_state.step < 4:
            st.markdown("### 💡 " + translate("Example Questions", lang_code))
            example_list = []
            if category == "upi":
                example_list = [
                    "Is this UPI transaction fraudulent?", "Check this UPI payment.", "Is this UPI ID safe?",
                    "Can I trust this sender in UPI?", "Detect fraud in this UPI transfer.", "Does this receiver look suspicious?",
                    "Verify this UPI amount."
                ]
            elif category == "credit":
                example_list = [
                    "Check this credit card transaction.", "Is this card number safe?", "Does this CVV look valid?",
                    "Is this a fraudulent card transaction?", "Verify this credit card payment.", "Is this card compromised?",
                    "Can I trust this card purchase?"
                ]
            elif category == "url":
                example_list = [
                    "Is this link safe to click?", "Check if this website is fraudulent.", "Can I trust this payment site?",
                    "Is this a phishing website?", "Detect fraud in this URL.", "Is this shortened link safe?",
                    "Check if this site is secure."
                ]
            selected_example = st.radio(
                "", [translate(q, lang_code) for q in example_list], index=0, key="selected_example"
            )
            st.session_state.prefilled_query = selected_example

    with col1:
        if st.session_state.step >= 3:
            user_query = st.text_input(
                translate("Type your question here...", lang_code),
                key="query",
                value=st.session_state.get("prefilled_query", "")
            )
            if user_query and st.session_state.step == 3:
                speak(translate("Now press the Predict button to get the prediction.", lang_code), lang_code)
                st.session_state.step = 4

        if st.session_state.step >= 4:
            if st.button(translate("Predict", lang_code)):
                if not st.session_state.query:
                    st.warning(translate("Please enter your question or command.", lang_code))
                else:
                    with st.spinner("🤖 " + translate("Bot is typing...", lang_code)):
                        time.sleep(1.5)

                                        # ---- ML Prediction ----
                    response, is_safe, risk_score = chatbot_reply(
                        st.session_state.query,
                        st.session_state.stored_inputs,
                        category
                    )

                    translated = translate(response, lang_code)
                    speak(translated, lang_code)

                    # Show Safe / Fraud Result
                    if is_safe:
                        st.markdown(f"<div class='safe-box'>{translated}</div>", unsafe_allow_html=True)
                    elif is_safe is False:
                        st.markdown(f"<div class='danger-box'>🚨 {translated}</div>", unsafe_allow_html=True)
                    else:
                        st.info(translated)

                    # 🔢 Risk Score directly below result
                    st.markdown(f"""
                    <div style='font-size:20px; font-weight:600; margin-top:10px;'>
                    🔢 Risk Score: {risk_score}%
</div>
""", unsafe_allow_html=True)
                    status_str = "Safe" if is_safe is True else ("Fraud" if is_safe is False else "Unknown")
                    status_str = f"{status_str} - Risk Score: {risk_score}%"
                    tx_hash, tx_time, tx_status = store_on_blockchain(st.session_state.query, status_str)
                    if tx_hash:
                        txn_html = (
                            f"<div style='font-family: monospace; font-size: 16px; color: black; "
                            f"padding: 8px; border-radius: 6px; "
                            f"overflow-x: auto; max-width: 100%; white-space: nowrap;'>"
                            f"<div><strong>Txn Hash:</strong></div>"
                            f"<div style='word-break: break-all;'>{tx_hash}</div>"
                            f"<div><strong>Timestamp:</strong> {tx_time}</div>"
                            f"<div><strong>Status:</strong> {tx_status}</div>"
                            f"</div>"
                        )
                        st.markdown(txn_html, unsafe_allow_html=True)

                    # ---- Persist transaction in DB ----
                    try:
                        if "user_id" in st.session_state:
                            si = st.session_state.stored_inputs
                            save_transaction(
                                user_id=st.session_state.user_id,
                                category=category,
                                query=st.session_state.query,
                                result=response,
                                status=status_str,
                                txn_hash=tx_hash or "",
                                timestamp=tx_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                upi_id=si.get("upi_id") if category=="upi" else None,
                                sender=si.get("sender") if category=="upi" else None,
                                receiver=si.get("receiver") if category=="upi" else None,
                                amount=float(si.get("amount",0)) if category=="upi" else None,
                                txn_date=str(si.get("date")) if category=="upi" else None,
                                txn_time=si.get("time") if category=="upi" else None,
                                card_number=si.get("card_number") if category=="credit" else None,
                                url=si.get("url") if category=="url" else None
                            )
                    except Exception as e:
                        st.error(f"Failed to store transaction: {e}")

                    # ---- Email Alert ----
                    try:
                        receiver_email = st.session_state.get("user_email", None)

                        if receiver_email:
                            email_status = "fraud" if is_safe is False else ("safe" if is_safe else "unknown")

                            send_alert(
                                receiver_email,
                                status=email_status,
                                ml_result=response,
                                txn_hash=tx_hash,
                                txn_timestamp=tx_time
                            )

                            st.success(f"✅ Alert sent successfully to {receiver_email}!")

                    except Exception as e:
                        st.warning(f"Could not send email alert: {e}")


                    # =========================
                    # SHAP Section (MOVE HERE)
                    # =========================
                    try:

                        st.info(f"Available SHAP explainers: {list(shap_explainers.keys())}")

                        if category in shap_explainers:

                            st.subheader("🔹 SHAP Explainability")

                            explainer = shap_explainers[category]

                            # Extract features
                            features_list, feature_names = extract_features(
                                st.session_state.stored_inputs, category
                            )

                            input_df = pd.DataFrame([features_list], columns=feature_names)

                            # Transform features
                            preprocessor = list(models[category].named_steps.values())[0]
                            X_input = preprocessor.transform(input_df)

                            if hasattr(X_input, "toarray"):
                                X_input = X_input.toarray()

                            X_input = X_input.astype(float)

                                # Local SHAP
                            local_shap = explainer(X_input)

                            local_shap_values = local_shap.values[0]

                            if len(local_shap_values.shape) > 1:
                                    local_shap_values = local_shap_values[:,1]

                            df_local = pd.DataFrame({
                                    "Feature": feature_names,
                                    "SHAP Value": local_shap_values
                                })

                            df_local["Abs Value"] = df_local["SHAP Value"].abs()

                            df_top = df_local.sort_values("Abs Value", ascending=False).head(5)

                            st.text("Top 5 Features Influencing Prediction:")

                            for _, row in df_top.iterrows():
                                    effect = "Increase Fraud Risk" if row["SHAP Value"] > 0 else "Decrease Fraud Risk"
                                    st.text(f"- {row['Feature']}: {effect} ({row['SHAP Value']:.3f})")

                            import matplotlib.pyplot as plt

                            fig, ax = plt.subplots(figsize=(10,6))
                            ax.barh(df_top["Feature"], df_top["Abs Value"])
                            ax.set_xlabel("SHAP Impact")
                            ax.set_title(f"Top 5 SHAP Features for {category}")

                            st.pyplot(fig)

                    except Exception as e:
                        st.warning(f"SHAP explanation failed: {e}")
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if not st.session_state.logged_in:
        login_page()
    else:
        chatbot_interface()

if __name__ == "__main__":
    main()
 