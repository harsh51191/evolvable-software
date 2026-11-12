import os

import psycopg
import pytest
from psycopg.rows import dict_row

import deskctl
from desk.app import app


@pytest.fixture
def conn():
    url = os.environ["TEST_DATABASE_URL"]
    with psycopg.connect(url, autocommit=True, row_factory=dict_row) as connection:
        connection.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public")
        deskctl.migrate(connection)
        yield connection


@pytest.fixture
def orgs(conn, monkeypatch):
    """Two organisations, each with a lead token and a widget key."""
    monkeypatch.setenv("DATABASE_URL", os.environ["TEST_DATABASE_URL"])
    out = []
    for name in ("acme", "globex"):
        org = conn.execute("INSERT INTO organisations (name, widget_key) VALUES (%s, %s) RETURNING id",
                           (name, f"key-{name}")).fetchone()["id"]
        conn.execute("INSERT INTO users VALUES (%s, %s, 'lead', %s)", (f"lead-{name}", org, f"token-{name}"))
        out.append({"id": org, "lead": {"X-Desk-Token": f"token-{name}"}, "widget": {"X-Desk-Key": f"key-{name}"}})
    return out


@pytest.fixture
def client():
    return app.test_client()
