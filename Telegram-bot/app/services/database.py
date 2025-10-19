import sqlite3
from config import DATABASE_URL

conn = sqlite3.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT
)
''')
conn.commit()


def add_user(user_id: int, username: str) -> None:
    """Add a new user to the database."""
    cursor.execute("INSERT INTO users (id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()


def get_user(user_id: int) -> tuple:
    """Retrieve a user from the database."""
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()