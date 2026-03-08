# 🛡 Fraud Detection Chatbot with Machine Learning, Explainable AI & Blockchain

## 📌 Project Overview

Fraud Detection Chatbot is an **AI-powered system designed to detect fraudulent financial transactions and assist users through an interactive chatbot interface**. The system combines **Machine Learning, Explainable AI (XAI), Blockchain logging, Natural Language Processing, and voice interaction** to provide a secure and intelligent fraud detection platform.

The chatbot analyzes transaction data using trained machine learning models and determines whether a transaction is **fraudulent or legitimate**. To enhance transparency and security, verified transactions are recorded using **blockchain smart contracts**, ensuring that records are **tamper-proof and traceable**.

To increase transparency of machine learning decisions, the system also integrates **Explainable AI using SHAP**, which helps understand how features contribute to fraud predictions.

The system includes **voice-enabled chatbot interaction, visualization dashboards, model comparison experiments, and an admin monitoring panel** to track transactions and system activity.

This project demonstrates how **Artificial Intelligence, Explainable AI, Blockchain technology, and conversational interfaces** can be integrated to build **secure and intelligent digital financial systems**.

---

# 🛠 Tech Stack

## Frontend

* HTML
* CSS
* JavaScript
* Chatbot UI Interface

## Backend

* Python
* Flask Web Framework

## Machine Learning

* Scikit-learn
* Random Forest
* XGBoost
* LightGBM
* Logistic Regression

## Explainable AI

* SHAP (SHapley Additive Explanations)

## Blockchain

* Solidity Smart Contracts
* Fraud transaction logging
* Risk score storage

## Database

* SQLite

## Data Processing

* Pandas
* NumPy

## Visualization

* Matplotlib
* Seaborn

## Additional Tools

* Streamlit Dashboard
* Email Alert System
* Voice Interaction

---

# ✨ Features

* AI-based **fraud detection using multiple machine learning models**
* **Explainable AI (XAI)** using SHAP for model transparency
* **Blockchain-based transaction logging**
* **Smart contracts for fraud verification and risk scoring**
* Interactive **chatbot interface**
* **Voice-enabled chatbot responses**
* **Admin monitoring dashboard**
* **Transaction visualization dashboard**
* **Credit Card, UPI, and URL fraud detection modules**
* **Model comparison experiments**
* Fraud alert notifications via **email**
* Secure **SQLite database storage**
* **Streamlit analytics interface**

---

# 🧠 Machine Learning Models

The system integrates several machine learning algorithms to detect fraudulent activity across different transaction types.

Implemented models include:

* Random Forest
* XGBoost
* LightGBM
* Logistic Regression

Fraud detection modules:

* **Credit Card Fraud Detection**
* **UPI Fraud Detection**
* **URL Fraud Detection**

Model training and evaluation experiments are available inside the **notebook/** directory.

---

# 🔍 Explainable AI (XAI)

To improve trust and transparency in fraud detection models, the system uses **SHAP (SHapley Additive Explanations)**.

SHAP helps:

* Interpret machine learning predictions
* Identify important features influencing fraud detection
* Provide explainable decision support for financial systems

Implementation files are located in:

```
XAI/SHAP/
```

---

# ⛓ Blockchain Integration

The project integrates **Ethereum-style smart contracts** to securely log fraud detection results.

Implemented contracts:

* **FraudDetection.sol** – Logs fraud detection events
* **RiskScore.sol** – Stores and updates risk scores

Blockchain utilities include:

* Smart contract deployment scripts
* Contract testing scripts
* Risk score update utilities

Blockchain components are located in:

```
blockchain/contracts/
blockchain/scripts/
blockchain/artifacts/
```

This ensures:

* **Tamper-proof transaction records**
* **Transparent fraud verification**
* **Secure decentralized logging**

---

# 📊 Model Experimentation

Extensive experiments were conducted to compare machine learning models for fraud detection.

Available notebooks:

* Credit Card Fraud Model Comparison
* UPI Fraud Model Comparison
* URL Fraud Model Comparison

Location:

```
notebook/
```

These notebooks evaluate:

* Model accuracy
* Precision and recall
* Fraud detection performance
* Feature importance analysis

---

# 🚀 Getting Started

Follow the steps below to run the project locally.

---

# ⚙ Prerequisites

Ensure the following software is installed on your system:

* Python 3.8 or higher
* pip (Python package manager)
* Git

Verify Python installation:

```bash
python --version
```

---

# 📥 Installation

Clone the repository:

```bash
git clone https://github.com/sayalivadya1654-cell/Fraud-Detection-Chatbot-.git
```

Navigate to the project directory:

```bash
cd Fraud-Detection-Chatbot-
```

Install required dependencies:

```bash
pip install -r requirements.txt
```

---

# ⚙ Configuration

Ensure the following components are configured correctly:

Machine learning models stored in:

```
models/
```

Database files:

* fraud_detection.db
* fraud_chatbot.db
* users.db

Transaction datasets:

* transactions.csv
* upi_verification_log.csv

Email configuration for fraud alerts inside:

```
send_email.py
```

---

# ▶ Running the Application

Start the main chatbot application:

```bash
python app.py
```

Run the admin dashboard:

```bash
python admin_dashboard.py
```

Start visualization dashboard:

```bash
python visualization_dashboard.py
```

Once the server starts, open your browser and visit:

```
http://localhost:5000
```

This launches the **Fraud Detection Chatbot interface**.

---

# 📂 Project Structure

```
Fraud-Detection-Chatbot
│
├── XAI/
│   └── SHAP/                   # Explainable AI utilities
│
├── blockchain/
│   ├── contracts/              # Smart contracts
│   ├── scripts/                # Deployment & testing scripts
│   └── artifacts/              # Contract ABI and addresses
│
├── database/                   # SQLite databases
│
├── model/                      # ML model training scripts
├── models/                     # Saved machine learning models
│
├── notebook/                   # Jupyter notebooks for experimentation
│
├── streamlit/                  # Streamlit analytics components
│
├── app.py                      # Main chatbot application
├── admin_dashboard.py          # Admin monitoring dashboard
├── visualization_dashboard.py  # Transaction visualization dashboard
│
├── send_email.py               # Email alert system
│
└── README.md                   # Project documentation
```

---

# 🤖 Fraud Detection Pipeline

The fraud detection system follows this workflow:

**1️⃣ User Interaction**

User interacts with the chatbot via text or voice.

**2️⃣ Transaction Input**

Transaction information is collected.

**3️⃣ Data Processing**

Transaction data is cleaned and prepared.

**4️⃣ Machine Learning Prediction**

ML models analyze the transaction and predict:

* Fraudulent transaction
* Legitimate transaction

**5️⃣ Explainable AI**

SHAP explains the model decision and highlights important features.

**6️⃣ Blockchain Logging**

Transactions are recorded on the blockchain ledger.

**7️⃣ Alerts & Reporting**

If fraud is detected:

* Email alerts are sent
* Admin dashboard logs the event
* Visualization dashboard updates analytics

---

# 📊 Use Cases

This system can be applied in:

* Digital payment platforms
* Banking fraud detection
* Online transaction monitoring
* FinTech security systems

---

# ⭐ Project Highlights

This project demonstrates integration of:

* Artificial Intelligence
* Explainable AI (XAI)
* Blockchain Technology
* Chatbot Interfaces
* Fraud Detection Systems

The platform provides a **secure, transparent, and intelligent fraud detection solution for modern financial systems**.

---

# 🤝 Contributing

Contributions are welcome.

Steps:

1. Fork the repository

2. Create a new branch

```bash
git checkout -b feature-new-improvement
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push the branch

```bash
git push origin feature-new-improvement
```

5. Create a Pull Request.

---

# 📜 License

This project is licensed under the **MIT License**.

---

⭐ If you find this project useful, consider **starring the repository**.
