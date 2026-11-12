"""Operator commands: deskctl.py migrate | backup [DIR] | add-org NAME | add-user NAME ORG ROLE"""
import datetime
import os
import secrets
import subprocess
import sys

import psycopg

URL = os.environ.get("DATABASE_URL", "postgresql://desk@localhost/desk")
MIGRATIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrations")


def migrate(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS applied_migrations (name TEXT PRIMARY KEY)")
    done = {row[0] for row in conn.execute("SELECT name FROM applied_migrations")}
    for name in sorted(n for n in os.listdir(MIGRATIONS) if n.endswith(".sql") and n not in done):
        with open(os.path.join(MIGRATIONS, name), encoding="utf-8") as handle:
            conn.execute(handle.read())
        conn.execute("INSERT INTO applied_migrations VALUES (%s)", (name,))
        print("applied", name)


def backup(_conn, directory="/backups"):
    """pg_dump the whole database to DIRECTORY/desk-YYYYmmdd-HHMMSS.dump."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, datetime.datetime.now().strftime("desk-%Y%m%d-%H%M%S.dump"))
    subprocess.run(["pg_dump", "--format=custom", "--file", path, URL], check=True)
    return path


def add_org(conn, name):
    conn.execute("INSERT INTO organisations (name, widget_key) VALUES (%s, %s)", (name, secrets.token_urlsafe(16)))


def add_user(conn, name, org, role):
    token = secrets.token_urlsafe(24)
    conn.execute("INSERT INTO users (name, org_id, role, token) SELECT %s, id, %s, %s FROM organisations "
                 "WHERE name = %s", (name, role, token, org))
    print(token)


if __name__ == "__main__":
    with psycopg.connect(URL, autocommit=True) as connection:
        {"migrate": migrate, "backup": backup, "add-org": add_org, "add-user": add_user}[sys.argv[1]](
            connection, *sys.argv[2:])
