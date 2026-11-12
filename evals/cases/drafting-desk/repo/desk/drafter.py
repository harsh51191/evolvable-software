"""The AI lane: drafts routing-rule changes for a lead to finish and publish.

A draft is stored with its check results, source, model and prompt version. Nothing here
makes a change live; only a lead's publish does (desk/app.py). Run: python -m desk.drafter"""
import json
import os
import time

import psycopg
import requests
from psycopg.rows import dict_row

from desk import checks, store

PROMPT_PATH = "prompts/draft_rule.txt"
PROMPT_VERSION = "draft-rule-3"
MODEL = os.environ.get("LLM_MODEL", "small-1")
ALLOWED_FIELDS = {"key", "pattern", "queue", "priority"}  # routing rules only
MAX_AI_PRIORITY = 50  # an AI draft may not outrank the rules leads put above 50


class OutOfScope(Exception):
    pass


def complete(prompt):
    """One model call: 20-second timeout, up to three attempts."""
    for attempt in range(3):
        try:
            reply = requests.post(os.environ["LLM_API_URL"], json={"model": MODEL, "prompt": prompt}, timeout=20)
            reply.raise_for_status()
            return reply.json()["text"]
        except requests.RequestException:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def enforce_scope(body):
    if set(body) - ALLOWED_FIELDS:
        raise OutOfScope(f"fields outside the AI's scope: {sorted(set(body) - ALLOWED_FIELDS)}")
    if not isinstance(body.get("priority"), int) or body["priority"] > MAX_AI_PRIORITY:
        raise OutOfScope(f"priority must be at most {MAX_AI_PRIORITY}")
    return body


def evidence(conn, org, payload):
    if payload["source_type"] == "failure_group":
        group = [g for g in store.failure_groups(conn, org) if g["normalised"] == payload["source_ref"]]
        return group[0]["samples"] if group else []
    request = store.get(conn, org, "change_requests", int(payload["source_ref"]))
    return [request["what"]] + request["examples"]


def draft(conn, org, payload):
    with open(PROMPT_PATH, encoding="utf-8") as handle:
        prompt = handle.read().replace("{questions}", "\n".join(
            f"<question>{q}</question>" for q in evidence(conn, org, payload)))
    body = enforce_scope(json.loads(complete(prompt)))
    errors = checks.check("rule", body["key"], body, store.all_current(conn, org, "rule"), checks.load_queues())
    return conn.execute("INSERT INTO drafts (org_id, key, body, check_errors, source_type, source_ref, model, "
                        "prompt_version) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                        (org, body["key"], json.dumps(body), json.dumps(errors), payload["source_type"],
                         payload["source_ref"], MODEL, PROMPT_VERSION)).fetchone()["id"]


def run_worker(conn):
    while True:
        job = store.next_job(conn)
        if job is None:
            time.sleep(5)
            continue
        try:
            draft(conn, job["org_id"], job["payload"])
            store.finish_job(conn, job["id"], "done")
        except Exception as exc:  # retried until the third attempt, then left failed with the reason
            store.finish_job(conn, job["id"], "failed" if job["attempts"] >= 3 else "queued", str(exc))


if __name__ == "__main__":
    run_worker(psycopg.connect(os.environ["DATABASE_URL"], autocommit=True, row_factory=dict_row))
