import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ----------------- EMAIL DETAILS -----------------
SENDER_EMAIL = "sayalivadya1654@gmail.com"   # Your Gmail address
APP_PASSWORD = "rtho hvkq hcqc szab"         # 16-char Google App Password

# ----------------- SEND EMAIL FUNCTION -----------------
def send_alert(receiver_email, status="fraud", ml_result=None, txn_hash=None, txn_timestamp=None):
    """
    Send alert email to a specific user with full transaction details.
    receiver_email: email entered at login
    status: 'fraud' or 'safe'
    ml_result: result from ML prediction (string)
    txn_hash: transaction hash (string)
    txn_timestamp: transaction timestamp (string)
    """
    subject = "Fraud Detection Alert 🚨" if status.lower() == "fraud" else "Transaction Safe ✅"

    # Prepare transaction details for email body
    details = ""
    if ml_result:
        details += f"ML Prediction Result: {ml_result}\n"
    if txn_hash:
        details += f"Transaction Hash: {txn_hash}\n"
    if txn_timestamp:
        details += f"Timestamp: {txn_timestamp}\n"
    details += f"Status: {status}\n"

    if status.lower() == "fraud":
        body = f"""
Hello User,

⚠️ ALERT: A fraudulent transaction has been detected in your account.

Here are the transaction details:
{details}

Please check your recent activities immediately.

Regards,
Sayali's Fraud Detection System
"""
    else:
        body = f"""
Hello User,

✅ Good news! Your last transaction was verified as SAFE.

Here are the transaction details:
{details}

Regards,
Sayali's Fraud Detection System
"""

    # Create email
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent successfully to {receiver_email} ({status})")
    except Exception as e:
        print(f"❌ Error sending email to {receiver_email}: {e}")


# ----------------- USAGE AFTER LOGIN -----------------
if __name__ == "__main__":
    # Example: replace this with email from login page
    login_email = input("Enter your email after login: ").strip()
    
    # Example transaction details
    predicted_status = "fraud"         # ML prediction
    ml_result = "Fraudulent Transaction"
    txn_hash = "0xabc123def456..."
    txn_timestamp = "2025-08-15 11:30:00"

    # Send alert email
    send_alert(login_email, status=predicted_status, ml_result=ml_result, txn_hash=txn_hash, txn_timestamp=txn_timestamp)
