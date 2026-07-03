import sqlite3

db = sqlite3.connect("messages.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS conversations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    reply TEXT,
    UNIQUE(message, reply)
)
""")
db.commit()


def save_pair(message, reply):
    message = message.strip()
    reply = reply.strip()

    if len(message) < 3 or len(reply) < 3:
        return

    if message == reply:
        return

    try:
        cursor.execute(
            "INSERT INTO conversations(message, reply) VALUES(?, ?)",
            (message, reply)
        )
        db.commit()
    except sqlite3.IntegrityError:
        pass


def get_all_pairs():
    cursor.execute("SELECT message, reply FROM conversations")
    return cursor.fetchall()


def total_pairs():
    cursor.execute("SELECT COUNT(*) FROM conversations")
    return cursor.fetchone()[0]