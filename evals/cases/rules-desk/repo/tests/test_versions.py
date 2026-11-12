from desk import store


def test_undo_restores_the_previous_version(conn):
    store.save(conn, "rule", "refunds", {"pattern": "refund", "queue": "billing", "priority": 10}, "alice")
    store.save(conn, "rule", "refunds", {"pattern": "refund|money back", "queue": "general", "priority": 10}, "bob")
    assert store.undo(conn, "rule", "refunds", "alice") == 3
    assert store.all_current(conn, "rule")[0]["queue"] == "billing"
    assert [v["author"] for v in store.history(conn, "rule", "refunds")] == ["alice", "bob", "alice"]


def test_failed_lookups_are_queryable_by_area(conn):
    store.record_failed_lookup(conn, "Can I pay by cheque?", "billing", "widget")
    store.record_failed_lookup(conn, "Where is my parcel?", "orders", "email")
    assert [r["question"] for r in store.failed_lookups(conn, "billing")] == ["Can I pay by cheque?"]
