RULE = {"pattern": "refund", "queue": "billing", "priority": 10}
ANSWER = {"keywords": ["refund"], "text": "Refunds take five days."}


def test_a_lead_sees_only_their_organisations_rules(client, orgs):
    acme, globex = orgs
    assert client.put("/admin/rules/refunds", json=RULE, headers=globex["lead"]).status_code == 200
    assert client.get("/admin/rules", headers=acme["lead"]).get_json() == []
    assert client.get("/admin/rules/refunds/history", headers=acme["lead"]).get_json() == []


def test_the_widget_answers_only_from_its_own_organisation(client, orgs):
    acme, globex = orgs
    client.put("/admin/answers/refunds", json=ANSWER, headers=globex["lead"])
    reply = client.post("/ask", json={"question": "refund please", "area": "billing"}, headers=acme["widget"])
    assert reply.get_json()["answer"] is None


def test_failure_groups_and_drafts_are_per_organisation(client, orgs, conn):
    acme, globex = orgs
    client.post("/ask", json={"question": "Pay by cheque?", "area": "billing"}, headers=globex["widget"])
    assert client.get("/admin/failure-groups", headers=acme["lead"]).get_json() == []
    conn.execute("INSERT INTO drafts (org_id, key, body, check_errors, source_type, source_ref, model, prompt_version) "
                 "VALUES (%s, 'cheques', '{}', '[]', 'request', '1', 'm', 'p')", (globex["id"],))
    assert client.post("/admin/drafts/1/publish", headers=acme["lead"]).status_code == 404
