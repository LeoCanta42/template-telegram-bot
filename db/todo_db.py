import sqlite3
from typing import List, Optional

DB_PATH = "todo.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            message_id TEXT NOT NULL,
            is_done INTEGER DEFAULT 0
        )
        """)

def add_todo(message: str, message_id: int = None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO todos (message,message_id) VALUES (?,?)", (message,message_id,))
        todo_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        return todo_id

def list_todos() -> List[sqlite3.Row]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row  # enables dict-style access
        return conn.execute("SELECT id, message, is_done FROM todos").fetchall()

def complete_todo(todo_id: int) -> Optional[int]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT message_id FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        if row:
            topic_msg_id = row[0]
            conn.execute("UPDATE todos SET is_done = 1 WHERE id = ?", (todo_id,))
            return topic_msg_id
    return None

