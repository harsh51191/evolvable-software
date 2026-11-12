"""SQLite access. The table is created by hand from schema.sql."""
import sqlite3

import settings


def connect():
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def list_notes(category, limit):
    with connect() as conn:
        if category:
            return conn.execute("SELECT * FROM notes WHERE category = ? ORDER BY id DESC LIMIT ?",
                                (category, limit)).fetchall()
        return conn.execute("SELECT * FROM notes ORDER BY id DESC LIMIT ?", (limit,)).fetchall()


def search_notes(text, limit):
    like = f"%{text}%"
    with connect() as conn:
        return conn.execute("SELECT * FROM notes WHERE title LIKE ? OR body LIKE ? ORDER BY id DESC LIMIT ?",
                            (like, like, limit)).fetchall()


def get_note(note_id):
    with connect() as conn:
        return conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()


def add_note(title, category, body):
    with connect() as conn:
        conn.execute("INSERT INTO notes (title, category, body) VALUES (?, ?, ?)", (title, category, body))


def delete_note(note_id):
    with connect() as conn:
        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
