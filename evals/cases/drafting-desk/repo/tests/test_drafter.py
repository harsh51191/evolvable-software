import json

import pytest

from desk import drafter


def test_a_draft_outside_the_ai_scope_is_refused():
    with pytest.raises(drafter.OutOfScope):
        drafter.enforce_scope({"key": "x", "pattern": "x", "queue": "billing", "priority": 10, "users": ["eve"]})
    with pytest.raises(drafter.OutOfScope):
        drafter.enforce_scope({"key": "x", "pattern": "x", "queue": "billing", "priority": 90})


def test_a_draft_is_stored_for_review_and_not_made_live(conn, orgs, monkeypatch):
    acme, _ = orgs
    monkeypatch.setattr(drafter, "complete", lambda prompt: json.dumps(
        {"key": "cheques", "pattern": "cheque", "queue": "billing", "priority": 20}))
    conn.execute("INSERT INTO change_requests (org_id, requester, area, what) VALUES (%s, 'a', 'billing', 'cheques')",
                 (acme["id"],))
    draft_id = drafter.draft(conn, acme["id"], {"source_type": "request", "source_ref": "1"})
    row = conn.execute("SELECT status, check_errors FROM drafts WHERE id = %s", (draft_id,)).fetchone()
    assert row == {"status": "awaiting_review", "check_errors": []}
    assert conn.execute("SELECT COUNT(*) AS n FROM definition_versions").fetchone()["n"] == 0
