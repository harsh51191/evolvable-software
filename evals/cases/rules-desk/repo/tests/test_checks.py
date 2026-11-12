from desk import checks

QUEUES = {"general", "billing"}


def test_bad_pattern_is_refused():
    assert checks.check_rule({"pattern": "(refund", "queue": "billing", "priority": 10}, QUEUES)


def test_unknown_queue_is_refused():
    errors = checks.check_rule({"pattern": "refund", "queue": "sales", "priority": 10}, QUEUES)
    assert errors == ["queue: must be one of billing, general"]


def test_duplicate_keywords_are_refused():
    current = [{"key": "refunds", "keywords": ["refund"], "text": "..."}]
    errors = checks.check_answer("refund-time", {"keywords": ["refund"], "text": "Five days."}, current)
    assert errors == ["keywords: the same as answer refunds"]
