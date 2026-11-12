"""Operator commands: deskctl.py migrate | backup [DIR] | add-user NAME ROLE"""
import datetime
import os
import secrets
import sqlite3
import sys

DB = os.environ.get("DESK_DB", "/data/desk.db")
MIGRATIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrations")


def migrate(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS applied_migrations (name TEXT PRIMARY KEY)")
    done = {row[0] for row in conn.execute("SELECT name FROM applied_migrations")}
    for name in sorted(os.listdir(MIGRATIONS)):
        if name.endswith(".sql") and name not in done:
            with open(os.path.join(MIGRATIONS, name), encoding="utf-8") as handle:
                conn.executescript(handle.read())
            conn.execute("INSERT INTO applied_migrations VALUES (?)", (name,))
            conn.commit()
            print("applied", name)


def backup(conn, directory="/backups"):
    """Copy the whole database to DIRECTORY/desk-YYYYmmdd-HHMMSS.db."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, datetime.datetime.now().strftime("desk-%Y%m%d-%H%M%S.db"))
    target = sqlite3.connect(path)
    conn.backup(target)
    target.close()
    print(path)
    return path


def add_user(conn, name, role):
    token = secrets.token_urlsafe(24)
    conn.execute("INSERT INTO users (name, role, token) VALUES (?, ?, ?)", (name, role, token))
    conn.commit()
    print(token)


if __name__ == "__main__":
    command, args = sys.argv[1], sys.argv[2:]
    connection = sqlite3.connect(DB)
    {"migrate": migrate, "backup": backup, "add-user": add_user}[command](connection, *args)
