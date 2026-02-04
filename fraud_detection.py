import os
import sqlite3
from datetime import datetime

# Ensure database folder exists (same style as your old project)
DB_DIR = "database"
DB_PATH = os.path.join(DB_DIR, "fraud_chatbot.db")

def _connect():
    if not os.path.isdir(DB_DIR):
        os.makedirs(DB_DIR, exist_ok=True)
    # check_same_thread=False for Streamlit concurrency
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# ---------------- INIT ----------------
def init_db():
    conn = _connect()
    c = conn.cursor()

    # Users table (adds login_time; phone column present)
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        login_time TEXT
    )
    """)

    # Predictions/Transactions table (generic to support UPI / Card / URL)
    # NOTE: We DO NOT store CVV or full card number (security).
    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,           -- 'upi' | 'credit card' | 'url'
        query TEXT,              -- user question text
        result TEXT,             -- chatbot result text (e.g., "✅ ...", "⚠ ...")
        status TEXT,             -- "Safe" | "Fraud" | "Unknown"
        txn_hash TEXT,
        timestamp TEXT,

        -- UPI-specific
        upi_id TEXT,
        sender TEXT,
        receiver TEXT,
        amount REAL,
        txn_date TEXT,           -- store date as text (YYYY-MM-DD)
        txn_time TEXT,           -- HH:MM

        -- Card-specific
        card_bin6 TEXT,          -- first 6 (masked if you prefer)
        card_last4 TEXT,         -- last 4
        -- do NOT store CVV or full PAN!

        -- URL-specific
        url TEXT,

        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # Basic indices for faster admin filtering
    c.execute("CREATE INDEX IF NOT EXISTS idx_transactions_user ON transactions(user_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_transactions_time ON transactions(timestamp)")

    conn.commit()
    conn.close()

# ---------------- HELPERS ----------------
def _now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _mask_and_split_card(card_number: str):
    """
    Returns (bin6, last4) safely. If card number is short/invalid, returns None/None.
    """
    if not card_number:
        return None, None
    digits = "".join([c for c in card_number if c.isdigit()])
    if len(digits) < 10:
        # too short to reliably split; store as last4 only if possible
        return None, digits[-4:] if len(digits) >= 4 else None
    bin6 = digits[:6]
    last4 = digits[-4:]
    return bin6, last4

# ---------------- USERS ----------------
def save_user(name, email, phone):
    conn = _connect()
    c = conn.cursor()
    login_time = _now_str()
    c.execute("INSERT INTO users (name, email, phone, login_time) VALUES (?, ?, ?, ?)",
              (name, email, phone, login_time))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return user_id

def get_users():
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT id, name, email, phone, login_time FROM users ORDER BY login_time DESC")
    rows = c.fetchall()
    conn.close()
    return rows

# ---------------- TRANSACTIONS / PREDICTIONS ----------------
def save_transaction(
    user_id: int,
    category: str,
    query: str,
    result: str,
    status: str,
    txn_hash: str,
    timestamp: str,

    # Optional category-specific fields:
    upi_id: str = None,
    sender: str = None,
    receiver: str = None,
    amount: float = None,
    txn_date: str = None,
    txn_time: str = None,

    card_number: str = None,   # we'll split to (bin6, last4); DO NOT store CVV
    url: str = None
):
    card_bin6, card_last4 = _mask_and_split_card(card_number) if card_number else (None, None)

    conn = _connect()
    c = conn.cursor()
    c.execute("""
        INSERT INTO transactions (
            user_id, category, query, result, status, txn_hash, timestamp,
            upi_id, sender, receiver, amount, txn_date, txn_time,
            card_bin6, card_last4, url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, category, query, result, status, txn_hash, timestamp,
        upi_id, sender, receiver, amount, txn_date, txn_time,
        card_bin6, card_last4, url
    ))
    conn.commit()
    conn.close()

def get_transactions():
    conn = _connect()
    c = conn.cursor()
    c.execute("""
        SELECT
            t.id, t.timestamp, t.category, t.status, t.result,
            u.name, u.email, u.phone,
            t.query, t.txn_hash,
            t.upi_id, t.sender, t.receiver, t.amount, t.txn_date, t.txn_time,
            t.card_bin6, t.card_last4,
            t.url
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        ORDER BY t.timestamp DESC, t.id DESC
    """)
    rows = c.fetchall()
    conn.close()
    return rows
