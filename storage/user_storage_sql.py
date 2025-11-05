import os
from sqlalchemy import create_engine, text

DB_PATH = os.path.join("data", "movies.db")
DB_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DB_URL, echo=False)

# Tabelle für Nutzer anlegen (falls nicht vorhanden)
with engine.connect() as connection:
    connection.execute(text("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL
    )
    """))
    connection.commit()

def list_users():
    """Liefert Liste der Nutzer (id, username)."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, username FROM users"))
        return result.fetchall()

def create_user(username):
    """Legt neuen Nutzer an und liefert seine ID."""
    with engine.connect() as connection:
        try:
            result = connection.execute(text(
                "INSERT INTO users (username) VALUES (:username)"
            ), {"username": username})
            connection.commit()
            return result.lastrowid
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
