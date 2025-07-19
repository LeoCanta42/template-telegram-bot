import sqlite3
from pathlib import Path

DB_FILE = Path("money.db")
DB_FILE.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payer TEXT NOT NULL,
            payee TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()

def insert_transaction(payer: str, payee: str, amount: float, description: str = ""):
    with get_connection() as conn:
        conn.execute("""
        INSERT INTO transactions (payer, payee, amount, description)
        VALUES (?, ?, ?, ?);
        """, (payer, payee, amount, description))
        conn.commit()

def get_all_transactions():
    with get_connection() as conn:
        return conn.execute("SELECT payer, payee, amount, description FROM transactions").fetchall()
