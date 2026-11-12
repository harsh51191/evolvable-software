"""Checks that run before an answer or rule change goes live, by hand or from an AI draft."""
import re

import yaml

MAX_TEXT = 2000
QUOTA = {"rule": 500, "answer": 1000}  # per organisation, since the June 2026 incident


def load_queues(path="config/queues.yaml"):
    with open(path, encoding="utf-8") as handle:
        return {q["name"] for q in yaml.safe_load(handle)["queues"]}


def check(kind, key, body, current, queues):
    if not re.fullmatch(r"[a-z0-9-]{3,40}", key or ""):
        return ["key: 3 to 40 lowercase letters, digits or hyphens"]
    if key not in {c["key"] for c in current} and len(current) >= QUOTA[kind]:
        return [f"quota: at most {QUOTA[kind]} {kind}s per organisation"]
    return check_answer(key, body, current) if kind == "answer" else check_rule(body, queues)


def check_answer(key, body, current):
    errors = []
    keywords = body.get("keywords") or []
    if not keywords or not all(isinstance(k, str) and k.strip() for k in keywords):
        errors.append("keywords: give at least one keyword")
    if not body.get("text") or len(body["text"]) > MAX_TEXT:
        errors.append(f"text: required, at most {MAX_TEXT} characters")
    for other in current:
        if other["key"] != key and set(keywords) == set(other.get("keywords", [])):
            errors.append(f"keywords: the same as answer {other['key']}")
    return errors


def check_rule(body, queues):
    errors = []
    try:
        re.compile(body.get("pattern") or "")
    except re.error as exc:
        errors.append(f"pattern: {exc}")
    if not body.get("pattern"):
        errors.append("pattern: required")
    if body.get("queue") not in queues:
        errors.append(f"queue: must be one of {', '.join(sorted(queues))}")
    if not isinstance(body.get("priority"), int) or not 1 <= body["priority"] <= 100:
        errors.append("priority: a whole number from 1 to 100")
    return errors
