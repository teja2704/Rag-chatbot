import sqlite3
from datetime import datetime

DB_NAME = "rag_chatbot.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            query TEXT,
            response TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task_type TEXT,
            task_data TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_chat(user_id, query, response):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats (user_id, query, response, created_at) VALUES (?, ?, ?, ?)",
        (user_id, query, response, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()

def save_task(user_id, task_type, task_data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (user_id, task_type, task_data, created_at) VALUES (?, ?, ?, ?)",
        (user_id, task_type, str(task_data), datetime.now().isoformat())
    )

    conn.commit()
    conn.close()
