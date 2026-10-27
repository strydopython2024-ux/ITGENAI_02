from pathlib import Path
import sqlite3
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[4]
DB_PATH = ROOT / "CODE" / "DATA_BASE" / "database" / "business.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )''')

def create_user(name, email, password_hash, created_at):
    with get_connection() as conn:
        cur=conn.execute("INSERT INTO users(name,email,password,created_at) VALUES(?,?,?,?)", (name,email,password_hash,created_at))
        return cur.lastrowid

def get_user(email):
    with get_connection() as conn:
        row=conn.execute("SELECT * FROM users WHERE lower(email)=lower(?)", (email,)).fetchone()
        return dict(row) if row else None
