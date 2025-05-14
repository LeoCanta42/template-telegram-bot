import sqlite3
from typing import List, Tuple

DB_PATH = "todo.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            is_done INTEGER DEFAULT 0
        )
        """)

def add_todo(message: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO todos (message) VALUES (?)", (message,))

def list_todos() -> List[sqlite3.Row]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row  # enables dict-style access
        return conn.execute("SELECT id, message, is_done FROM todos").fetchall()

def complete_todo(todo_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE todos SET is_done = 1 WHERE id = ?", (todo_id,))
