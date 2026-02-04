# fraud_dashboard.py
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ----------------- DATABASE CONNECTION -----------------
def fetch_transactions():
    conn = sqlite3.connect("database/fraud_chatbot.db")
    c = conn.cursor()
    c.execute("""
        SELECT 
            t.id, t.timestamp, t.category, t.status,
            u.name, u.email, u.phone, t.amount
        FROM transactions t
        JOIN users u ON t.user_id = u.id
    """)
    data = c.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=[
        "Txn ID", "Timestamp", "Category", "Status",
        "User Name", "Email", "Phone", "Amount"
    ])

# ----------------- DASHBOARD -----------------
st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

# Custom CSS for better interface
st.markdown("""
    <style>
        .main {background-color: #f9f9f9;}
        .block-container {padding-top: 2rem; padding-bottom: 2rem;}
        h1 {color: #2c3e50; text-align: center;}
        h2, h3 {color: #34495e;}
        .stDataFrame {border-radius: 10px; overflow: hidden;}
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Fraud Detection Visualization Dashboard")
st.markdown("### 🔍 Monitor Fraud vs Safe Transactions in Real-Time")

df = fetch_transactions()

if df.empty:
    st.warning("⚠️ No transaction data available yet.")
else:
    # --- Raw Data ---
    st.markdown("## 📋 Transactions Data")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # --- Fraud vs Safe Distribution ---
    st.markdown("## 📈 Fraud vs Safe Transactions")
    fraud_counts = df["Status"].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🥧 Pie Chart")
        fig1, ax1 = plt.subplots()
        colors = ["#2ecc71", "#e74c3c", "#f1c40f"]
        ax1.pie(fraud_counts, labels=fraud_counts.index, autopct="%1.1f%%",
                startangle=90, colors=colors[:len(fraud_counts)])
        ax1.axis("equal")
        st.pyplot(fig1)

    with col2:
        st.markdown("### 📊 Bar Chart")
        fig2, ax2 = plt.subplots()

        # ✅ Fixed color mapping
        color_map = {
            "Safe": "#2ecc71",     # Green
            "Fraud": "#e74c3c",    # Red
            "Unknown": "#f1c40f"   # Yellow
        }
        bar_colors = [color_map.get(status, "#95a5a6") for status in fraud_counts.index]

        fraud_counts.plot(kind="bar", ax=ax2, color=bar_colors)
        ax2.set_ylabel("Count")
        ax2.set_xlabel("Status")
        st.pyplot(fig2)

    st.markdown("---")

    # --- Fraud over time ---
    st.markdown("## 📅 Fraud Cases Over Time")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    fraud_over_time = df.groupby(df["Timestamp"].dt.date)["Status"].apply(
        lambda x: (x == "Fraud").sum()
    )

    fig3, ax3 = plt.subplots()
    fraud_over_time.plot(kind="line", marker="o", ax=ax3, color="red")
    ax3.set_ylabel("Fraud Count")
    ax3.set_xlabel("Date")
    st.pyplot(fig3)

    st.markdown("---")

    # --- Users involved in fraud vs safe ---
    st.markdown("## 👥 Users with Fraud vs Safe Transactions")
    user_stats = df.groupby(["User Name", "Status"]).size().unstack(fill_value=0)

    st.dataframe(user_stats, use_container_width=True)

    fig4, ax4 = plt.subplots(figsize=(8,4))

    # ✅ Apply same fixed colors for stacked user chart
    user_colors = [color_map.get(col, "#95a5a6") for col in user_stats.columns]

    user_stats.plot(kind="bar", stacked=True, ax=ax4, color=user_colors)
    ax4.set_ylabel("Transactions")
    st.pyplot(fig4)

    st.markdown("---")

    # --- Transaction Amount Distribution ---
    st.markdown("## 💰 Transaction Amount Distribution (Fraud vs Safe)")

    colA1, colA2 = st.columns(2)

    with colA1:
        st.markdown("### 📦 Boxplot")
        fig5, ax5 = plt.subplots(figsize=(6,4))
        df.boxplot(column="Amount", by="Status", ax=ax5,
                   grid=False, patch_artist=True,
                   boxprops=dict(facecolor="lightblue", color="blue"),
                   medianprops=dict(color="red"))
        ax5.set_title("Amount Distribution by Status")
        ax5.set_ylabel("Transaction Amount")
        plt.suptitle("")  # remove default title
        st.pyplot(fig5)

    with colA2:
        st.markdown("### 📊 Histogram")
        fig6, ax6 = plt.subplots(figsize=(6,4))
        for status, color in color_map.items():
            subset = df[df["Status"] == status]
            ax6.hist(subset["Amount"], bins=10, alpha=0.6, label=status, color=color)
        ax6.set_title("Amount Histogram by Status")
        ax6.set_xlabel("Transaction Amount")
        ax6.set_ylabel("Frequency")
        ax6.legend()
        st.pyplot(fig6)

    st.markdown("---")

    # --- Total Summary ---
    st.markdown("## 📌 Summary")
    total_txns = len(df)
    fraud_txns = (df["Status"] == "Fraud").sum()
    safe_txns = (df["Status"] == "Safe").sum()
    unknown_txns = (df["Status"] == "Unknown").sum()

    colB1, colB2, colB3, colB4 = st.columns(4)
    colB1.metric("✅ Safe Transactions", safe_txns)
    colB2.metric("⚠️ Fraud Transactions", fraud_txns)
    colB3.metric("❓ Unknown Transactions", unknown_txns)
    colB4.metric("📊 Total Transactions", total_txns)
