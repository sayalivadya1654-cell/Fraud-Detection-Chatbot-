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

# ===== NEW: DB imports =====
from fraud_detection import init_db, save_user, save_transaction

# ===== NEW: Email alert import =====
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

/* Language selector style */
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

# ---------------- FRAUD DETECTION LOGIC ----------------
def chatbot_reply(user_query, inputs, category):
    if category == "upi":
        if ("fraud" in inputs.get("upi_id", "").lower() or
            "fraud" in inputs.get("sender", "").lower() or
            "fraud" in inputs.get("receiver", "").lower() or
            inputs.get("amount", 0) > 50000):
            return "⚠ Fraud Detected in UPI Transaction.", False
        return "✅ UPI Transaction is Safe.", True
    elif category == "credit card":
        if inputs.get("card_number", "").startswith("0000") or len(inputs.get("cvv", "")) != 3:
            return "⚠ Credit Card Fraud Detected.", False
        return "✅ Credit Card Transaction is Safe.", True
    elif category == "url":
        if any(s in inputs.get("url", "").lower() for s in ["bit.ly", "scam", "fraud", "phish"]):
            return "⚠ Fraudulent URL Detected.", False
        return "✅ URL is Safe to Visit.", True
    return "❓ Unable to verify transaction.", None

def store_on_blockchain(txn_id_text, status):
    try:
        fake_tx_hash = "0x" + "".join(random.choices("0123456789abcdef", k=64))
        fake_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return fake_tx_hash, fake_timestamp, "Success"
    except Exception as e:
        return None, None, f"Blockchain Error: {e}"

# ---------------- VALIDATION ----------------
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
    lang_code = st.session_state.lang_code
    st.title("💬 " + translate("Multilingual Fraud Detection Chatbot", lang_code))

    if st.session_state.step == 0:
        speak(translate(f"Welcome {st.session_state.get('user_name', '')}!", lang_code), lang_code)
        time.sleep(0.5)
        speak(translate("Please choose the fraud type to check.", lang_code), lang_code)
        st.session_state.step = 1

    category = st.radio(translate("Choose Transaction Type", lang_code),
                        ["upi", "credit card", "url"], horizontal=True, key="category")
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
        elif category == "credit card":
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
                elif category == "credit card":
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
            elif category == "credit card":
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
                    response, is_safe = chatbot_reply(st.session_state.query, st.session_state.stored_inputs, category)
                    translated = translate(response, lang_code)
                    speak(translated, lang_code)

                    if is_safe:
                        st.markdown(f"<div class='safe-box'>{translated}</div>", unsafe_allow_html=True)
                    elif is_safe is False:
                        st.markdown(f"<div class='danger-box'>🚨 {translated}</div>", unsafe_allow_html=True)
                    else:
                        st.info(translated)

                    status_str = "Safe" if is_safe is True else ("Fraud" if is_safe is False else "Unknown")
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

                    # ===== Persist transaction in DB =====
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
                                card_number=si.get("card_number") if category=="credit card" else None,
                                url=si.get("url") if category=="url" else None
                            )
                    except Exception as e:
                        st.error(f"Failed to store transaction: {e}")

                    # ===== Send email alert with full details =====
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

# ---------------- MAIN ----------------
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if not st.session_state.logged_in:
        login_page()
    else:
        chatbot_interface()

if __name__ == "__main__":
    main()
