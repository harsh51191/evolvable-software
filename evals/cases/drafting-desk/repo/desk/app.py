"""Drafting Desk: answers customer questions, routes the rest, and drafts rule changes with AI."""
import os

import psycopg
from flask import Flask, abort, g, jsonify, request, send_from_directory
from psycopg.rows import dict_row

from desk import checks, matching, store

VERSION = "3.1.0"
SETTINGS = ("greeting", "opening_hours")
app = Flask(__name__)


def db():
    if "db" not in g:
        g.db = psycopg.connect(os.environ["DATABASE_URL"], autocommit=True, row_factory=dict_row)
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def caller(lead=True, kind="rule"):
    """(organisation id, user name) for the token; 403 for a non-lead where a lead is needed."""
    user = db().execute("SELECT name, org_id, role FROM users WHERE token = %s",
                        (request.headers.get("X-Desk-Token", ""),)).fetchone()
    if user is None or (lead and user["role"] != "lead"):
        abort(403)
    if kind not in store.KINDS:
        abort(404)
    return user["org_id"], user["name"]


@app.post("/ask")
def ask():
    org = db().execute("SELECT id FROM organisations WHERE widget_key = %s",
                       (request.headers.get("X-Desk-Key", ""),)).fetchone() or abort(403)
    question, area = request.json.get("question", ""), request.json.get("area", "unknown")
    answer = matching.best_answer(question, store.all_current(db(), org["id"], "answer"))
    if answer is None:
        store.record_failed_lookup(db(), org["id"], question, area, request.json.get("channel", "widget"))
    return {"answer": answer and answer["text"],
            "queue": matching.route(question, store.all_current(db(), org["id"], "rule"))}


@app.get("/admin")
def admin_page():
    return send_from_directory("templates", "admin.html")


@app.get("/admin/<kind>s")
def list_definitions(kind):
    org, _ = caller(kind=kind)
    return jsonify(store.all_current(db(), org, kind))


def publish(org, author, kind, key, body, note):
    errors = checks.check(kind, key, body, store.all_current(db(), org, kind), checks.load_queues())
    if errors:
        return {"errors": errors}, 422
    return {"key": key, "version": store.save(db(), org, kind, key, body, author, note)}


@app.put("/admin/<kind>s/<key>")
def save_definition(kind, key):
    org, author = caller(kind=kind)
    return publish(org, author, kind, key, request.json, request.args.get("note", ""))


@app.get("/admin/<kind>s/<key>/history")
def history(kind, key):
    org, _ = caller(kind=kind)
    return jsonify(store.history(db(), org, kind, key))


@app.post("/admin/<kind>s/<key>/undo")
def undo(kind, key):
    org, author = caller(kind=kind)
    return {"version": store.undo(db(), org, kind, key, author) or abort(409)}


@app.put("/admin/settings/<name>")
def set_setting(name):
    org, _ = caller()
    if name not in SETTINGS:
        abort(404)
    db().execute("INSERT INTO settings (org_id, name, value) VALUES (%s, %s, %s) ON CONFLICT (org_id, name) "
                 "DO UPDATE SET value = EXCLUDED.value", (org, name, request.json["value"]))
    return {"name": name}


@app.post("/requests")
def new_request():
    org, requester = caller(lead=False)
    missing = [f for f in ("area", "what") if not request.json.get(f)]
    if missing:
        return {"errors": [f"{f}: required" for f in missing]}, 422
    return {"id": store.add_request(db(), org, requester, request.json)}


@app.get("/admin/requests")
def open_requests():
    org, _ = caller()
    return jsonify(store.rows(db(), org, "change_requests", "open"))


@app.get("/admin/failure-groups")
def failure_groups():
    org, _ = caller()
    return jsonify(store.failure_groups(db(), org, int(request.args.get("days", 14))))


@app.post("/admin/drafts")
def ask_for_draft():
    """Queue an AI draft from a failure group ({"failure_group": text}) or a request ({"request": id})."""
    org, _ = caller()
    if "failure_group" in request.json:
        payload = {"source_type": "failure_group", "source_ref": request.json["failure_group"]}
    else:
        payload = {"source_type": "request", "source_ref": str(request.json["request"])}
    store.queue_job(db(), org, payload)
    return {"queued": payload}, 202


@app.get("/admin/drafts")
def drafts():
    org, _ = caller()
    return jsonify(store.rows(db(), org, "drafts", "awaiting_review"))


@app.post("/admin/drafts/<int:draft_id>/<action>")
def finish_draft(draft_id, action):
    """A lead publishes a draft, edited or as it is, or discards it."""
    org, author = caller()
    draft = store.get(db(), org, "drafts", draft_id)
    if draft is None or draft["status"] != "awaiting_review" or action not in ("publish", "discard"):
        abort(404)
    if action == "discard":
        store.set_status(db(), org, "drafts", draft_id, "discarded")
        return {"status": "discarded"}
    body = request.get_json(silent=True) or draft["body"]
    result = publish(org, author, "rule", draft["key"], body, f"from AI draft {draft_id}")
    if isinstance(result, dict):
        store.set_status(db(), org, "drafts", draft_id, "published")
    return result


@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION}
