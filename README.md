# 🛡 Fraud Detection Chatbot with Machine Learning & Blockchain

## 📌 Project Overview

Fraud Detection Chatbot is an **AI-powered system designed to detect fraudulent financial transactions and assist users through an interactive chatbot interface**. The system combines **Machine Learning, Blockchain logging, Natural Language Processing, and voice interaction** to provide a secure and intelligent fraud detection platform.

The chatbot analyzes transaction data using trained machine learning models and determines whether a transaction is **fraudulent or legitimate**. To enhance transparency and security, verified transactions are recorded using **blockchain logging**, ensuring that records are **tamper-proof and traceable**.

The system also includes **voice-enabled chatbot interaction, a visualization dashboard, and an admin monitoring panel** to track transactions and system activity.

This project demonstrates how **Artificial Intelligence, Blockchain technology, and conversational interfaces** can be integrated to build **secure digital financial systems**.

---

# 🛠 Tech Stack

## Frontend

* HTML
* CSS
* JavaScript
* Chatbot UI interface

## Backend

* Python
* Flask Web Framework

## Machine Learning

* Scikit-learn
* Fraud Detection Classification Models

## Blockchain

* Custom blockchain implementation for secure transaction logging

## Database

* SQLite

## Data Processing

* Pandas
* NumPy

## Visualization

* Matplotlib
* Seaborn

## Additional Features

* Email alerts
* Voice-based chatbot interaction
* Admin dashboard

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

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

# ⚙ Configuration

Ensure the following components are properly configured:

• Machine learning models stored inside the **models/** directory
• Database files such as:

* fraud_detection.db
* fraud_chatbot.db
* users.db

• Transaction datasets:

* transactions.csv
* upi_verification_log.csv

• Email configuration for fraud alert notifications inside:

```python
send_email.py
```

---

# ▶ Running the Application

Start the main application:

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

This will launch the **Fraud Detection Chatbot interface**.

---

# ✨ Features

* AI-based **fraud detection using machine learning**
* Interactive **chatbot interface**
* **Voice-enabled chatbot responses**
* **Blockchain transaction logging**
* Secure transaction record storage
* **Admin monitoring dashboard**
* Fraud alert notifications via email
* Transaction visualization dashboard
* Secure SQLite database storage

---

# 📂 Project Structure

```
Fraud-Detection-Chatbot
│
├── blockchain/                 # Blockchain implementation for transaction logging
├── chatbot/                    # Chatbot conversation logic
├── database/                   # Database utilities and operations
├── model/                      # ML model training scripts
├── models/                     # Saved machine learning models
├── notebook/                   # Jupyter notebooks for experimentation
├── utils/                      # Helper functions and utilities
│
├── app.py                      # Main chatbot application
├── fraud_detection.py          # Fraud detection logic
├── integrate_models.py         # Integrates ML models with chatbot
├── admin_dashboard.py          # Admin monitoring dashboard
├── visualization_dashboard.py  # Transaction visualization dashboard
│
├── send_email.py               # Email alert system
├── create_dummy_models.py      # Script to generate sample models
│
├── transactions.csv            # Transaction dataset
├── upi_verification_log.csv    # UPI verification logs
│
├── fraud_chatbot.db            # Chatbot database
├── fraud_detection.db          # Fraud detection database
├── users.db                    # User authentication database
│
└── README.md                   # Project documentation
```

---

# 🤖 Fraud Detection Pipeline

The fraud detection system follows this workflow:

1️⃣ **User Interaction**

The user interacts with the chatbot via text or voice input.

2️⃣ **Transaction Input**

Transaction details are collected from the user.

3️⃣ **Data Processing**

The system preprocesses transaction data for analysis.

4️⃣ **Machine Learning Prediction**

The trained fraud detection model analyzes the transaction and predicts:

* Fraudulent transaction
* Legitimate transaction

5️⃣ **Blockchain Logging**

Transaction records are stored on a blockchain ledger to ensure **tamper-proof security**.

6️⃣ **Alerts and Reporting**

If fraud is detected:

* Email alerts are sent
* Admin dashboard logs the event
* Visualization dashboard updates the analytics

---

# 📊 Use Cases

This system can be applied in:

* Digital payment platforms
* Banking fraud detection
* Online transaction monitoring
* FinTech security systems

---

# 🤝 Contributing

Contributions are welcome!

To contribute:

1. Fork the repository
2. Create a new feature branch

```bash
git checkout -b feature-new-improvement
```

3. Commit your changes

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
