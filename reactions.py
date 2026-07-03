import sqlite3
import random

db = sqlite3.connect("messages.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    emoji TEXT,
    UNIQUE(message, emoji)
)
""")
db.commit()


def save_reaction(message, emoji):
    try:
        cursor.execute(
            "INSERT INTO reactions(message, emoji) VALUES(?, ?)",
            (message, str(emoji))
        )
        db.commit()
    except sqlite3.IntegrityError:
        pass


def get_reaction(message):
    cursor.execute(
        "SELECT emoji FROM reactions WHERE LOWER(message)=LOWER(?) ORDER BY RANDOM() LIMIT 1",
        (message,)
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    return None