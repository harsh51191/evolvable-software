"""Rules Desk: answers customer questions and routes the rest to the right queue."""
import os
import sqlite3

from flask import Flask, abort, g, jsonify, request, send_from_directory

from desk import checks, matching, store

VERSION = "2.3.1"
SETTINGS = ("greeting", "opening_hours")
app = Flask(__name__)


def db():
    if "db" not in g:
        g.db = sqlite3.connect(os.environ.get("DESK_DB", "/data/desk.db"))
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def require_lead(kind="rule"):
    """The calling lead's name; 403 for anyone else, 404 for a kind that is not answer or rule."""
    row = db().execute("SELECT name, role FROM users WHERE token = ?",
                       (request.headers.get("X-Desk-Token", ""),)).fetchone()
    if row is None or row["role"] != "lead":
        abort(403)
    if kind not in store.KINDS:
        abort(404)
    return row["name"]


@app.post("/ask")
def ask():
    question, area = request.json.get("question", ""), request.json.get("area", "unknown")
    answer = matching.best_answer(question, store.all_current(db(), "answer"))
    if answer is None:
        store.record_failed_lookup(db(), question, area, request.json.get("channel", "widget"))
    return {"answer": answer and answer["text"], "queue": matching.route(question, store.all_current(db(), "rule"))}


@app.get("/widget")
def widget():
    return {r["name"]: r["value"] for r in db().execute("SELECT name, value FROM settings")}


@app.get("/admin")
def admin_page():
    return send_from_directory("templates", "admin.html")


@app.get("/admin/<kind>s")
def list_definitions(kind):
    require_lead(kind)
    return jsonify(store.all_current(db(), kind))


@app.put("/admin/<kind>s/<key>")
def save_definition(kind, key):
    author = require_lead(kind)
    errors = checks.check(kind, key, request.json, store.all_current(db(), kind), checks.load_queues())
    if errors:
        return {"errors": errors}, 422
    return {"key": key, "version": store.save(db(), kind, key, request.json, author, request.args.get("note", ""))}


@app.get("/admin/<kind>s/<key>/history")
def history(kind, key):
    require_lead(kind)
    return jsonify(store.history(db(), kind, key))


@app.post("/admin/<kind>s/<key>/undo")
def undo(kind, key):
    author = require_lead(kind)
    version = store.undo(db(), kind, key, author)
    if version is None:
        abort(409)
    return {"key": key, "version": version}


@app.post("/admin/rules/try")
def try_rule():
    """Which queue a question would reach, with an unsaved rule in place of the live one."""
    require_lead()
    rules = store.all_current(db(), "rule")
    draft = request.json.get("rule")
    if draft:
        rules = [r for r in rules if r["key"] != draft["key"]] + [draft]
    return {"queue": matching.route(request.json["question"], rules)}


@app.get("/admin/failed-lookups")
def failed_lookups():
    require_lead()
    return jsonify(store.failed_lookups(db(), request.args.get("area")))


@app.put("/admin/settings/<name>")
def set_setting(name):
    require_lead()
    if name not in SETTINGS:
        abort(404)
    db().execute("INSERT OR REPLACE INTO settings (name, value) VALUES (?, ?)", (name, request.json["value"]))
    db().commit()
    return {"name": name}


@app.get("/health")
def health():
    return {"status": "ok", "version": VERSION}
