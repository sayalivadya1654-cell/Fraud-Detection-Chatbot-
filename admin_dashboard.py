import streamlit as st
import pandas as pd
from fraud_detection import init_db, get_users, get_transactions

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🛡️ Admin Dashboard - Fraud Detection System")

# Ensure DB exists
init_db()

tab_users, tab_txns = st.tabs(["👤 Users", "📈 Predictions / Transactions"])

with tab_users:
    st.subheader("Registered Users")
    users = get_users()
    if users:
        df_u = pd.DataFrame(users, columns=["ID", "Name", "Email", "Phone", "Login Time"])
        st.dataframe(df_u, use_container_width=True)
        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button("⬇️ Export Users (CSV)", df_u.to_csv(index=False), "users.csv", "text/csv")
        with col_b:
            st.write(f"Total Users: **{len(df_u)}**")
    else:
        st.info("No users found yet.")

with tab_txns:
    st.subheader("Prediction / Transaction Logs")
    txns = get_transactions()
    if txns:
        df_t = pd.DataFrame(txns, columns=[
            "ID", "Timestamp", "Category", "Status", "Result",
            "User Name", "Email", "Phone",
            "Query", "Txn Hash",
            "UPI ID", "Sender", "Receiver", "Amount", "Txn Date", "Txn Time",
            "Card BIN6", "Card Last4",
            "URL"
        ])

        # Quick filters
        c1, c2, c3 = st.columns([1,1,2])
        with c1:
            cat = st.selectbox("Filter by Category", ["All", "upi", "credit card", "url"])
        with c2:
            status = st.selectbox("Filter by Status", ["All", "Safe", "Fraud", "Unknown"])
        with c3:
            search = st.text_input("Search (name/email/phone/query/url/upi_id)")

        df_view = df_t.copy()
        if cat != "All":
            df_view = df_view[df_view["Category"] == cat]
        if status != "All":
            df_view = df_view[df_view["Status"] == status]
        if search:
            s = search.lower()
            df_view = df_view[
                df_view.apply(lambda r:
                    s in str(r["User Name"]).lower()
                    or s in str(r["Email"]).lower()
                    or s in str(r["Phone"]).lower()
                    or s in str(r["Query"]).lower()
                    or s in str(r["URL"]).lower()
                    or s in str(r["UPI ID"]).lower()
                , axis=1)
            ]

        st.dataframe(df_view, use_container_width=True, height=480)
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇️ Export Transactions (CSV)", df_view.to_csv(index=False), "transactions.csv", "text/csv")
        with col2:
            st.write(f"Rows: **{len(df_view)}**")
    else:
        st.info("No transactions recorded yet.")
