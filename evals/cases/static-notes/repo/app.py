"""Static Notes: a notes board for the support team."""
import logging

from flask import Flask, abort, jsonify, redirect, render_template_string, request

import content
import db
import settings

app = Flask(__name__)
log = logging.getLogger("static-notes")

PAGE = """<!doctype html>
<title>{{ title }}</title>
<h1>{{ title }}</h1>
<p>{{ help }}</p>
<nav>{% for c in categories %}<a href="/?category={{ c }}">{{ c }}</a> {% endfor %}</nav>
<form action="/search"><input name="q"><button>Search</button></form>
<ul>{% for n in notes %}<li><a href="/notes/{{ n['id'] }}">{{ n['title'] }}</a> ({{ n['category'] }})</li>{% endfor %}</ul>
<form method="post" action="/notes">
  <input name="title">
  <select name="category">{% for c in categories %}<option>{{ c }}</option>{% endfor %}</select>
  <textarea name="body"></textarea><button>Post</button>
</form>
"""


def page(help_key, notes):
    return render_template_string(PAGE, title=content.TITLE, help=content.HELP_TEXT[help_key],
                                  categories=content.CATEGORIES, notes=notes)


@app.get("/")
def index():
    return page("index", db.list_notes(request.args.get("category"), settings.PAGE_SIZE))


@app.post("/notes")
def create_note():
    title = request.form.get("title", "").strip()
    category = request.form.get("category")
    if not title or category not in content.CATEGORIES:
        abort(400)
    db.add_note(title, category, request.form.get("body", ""))
    return redirect("/")


@app.get("/notes/<int:note_id>")
def show_note(note_id):
    note = db.get_note(note_id)
    if note is None:
        abort(404)
    return jsonify(dict(note))


@app.post("/notes/<int:note_id>/delete")
def delete_note(note_id):
    db.delete_note(note_id)
    log.info("deleted note %s", note_id)
    return redirect("/")


@app.get("/search")
def search():
    return page("search", db.search_notes(request.args.get("q", ""), settings.PAGE_SIZE))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.errorhandler(500)
def server_error(error):
    log.exception("unhandled error: %s", error)
    return "Something went wrong", 500
