import os
import sqlite3

import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    path = tmp_path / "notes.db"
    with open(os.path.join(os.path.dirname(__file__), "..", "schema.sql")) as handle:
        sqlite3.connect(path).executescript(handle.read())
    monkeypatch.setenv("NOTES_DB", str(path))
    import importlib
    import settings
    importlib.reload(settings)
    from app import app
    return app.test_client()


def test_post_and_list(client):
    client.post("/notes", data={"title": "Printer down", "category": "outages", "body": "floor 3"})
    assert b"Printer down" in client.get("/").data


def test_unknown_category_is_refused(client):
    assert client.post("/notes", data={"title": "x", "category": "gossip"}).status_code == 400


def test_search(client):
    client.post("/notes", data={"title": "Refund policy", "category": "policies", "body": "from 1 May"})
    assert b"Refund policy" in client.get("/search?q=refund").data


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}
