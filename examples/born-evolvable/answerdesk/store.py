"""Foundations 2 and 4: the versioned store, its migrations (with down steps), backup and restore.

Every definition is a row in `changes`: a version with an author, a status and the version it
replaced, so any change can be undone in one step. `live` points at the stable version of each
definition and at the one candidate version being released gradually.
"""
import json
import os
import sqlite3
import time

# Each migration is (up statements, down statements). Schema changes are undoable too.
MIGRATIONS = [
    (
        [
            """CREATE TABLE changes (
                id INTEGER PRIMARY KEY, kind TEXT NOT NULL, key TEXT NOT NULL, version INTEGER NOT NULL,
                body TEXT, actor_type TEXT NOT NULL, actor TEXT NOT NULL, note TEXT, provenance TEXT,
                status TEXT NOT NULL, decision TEXT, share REAL NOT NULL DEFAULT 0, replaces INTEGER,
                measure TEXT, created_at REAL NOT NULL, released_at REAL, UNIQUE (kind, key, version))""",
            "CREATE TABLE live (kind TEXT NOT NULL, key TEXT NOT NULL, stable INTEGER, candidate INTEGER, PRIMARY KEY (kind, key))",
            """CREATE TABLE events (id INTEGER PRIMARY KEY, at REAL NOT NULL, change_id INTEGER,
                actor TEXT NOT NULL, event TEXT NOT NULL, detail TEXT)""",
            """CREATE TABLE signals (id INTEGER PRIMARY KEY, at REAL NOT NULL, session TEXT NOT NULL,
                question TEXT NOT NULL, answer_key TEXT, answer_change INTEGER, team TEXT,
                feedback TEXT, expected TEXT, check_change INTEGER)""",
            "CREATE INDEX signals_at ON signals (at)",
        ],
        ["DROP TABLE signals", "DROP TABLE events", "DROP TABLE live", "DROP TABLE changes"],
    ),
    (
        [
            "CREATE TABLE exposures (signal_id INTEGER NOT NULL, change_id INTEGER NOT NULL, arm TEXT NOT NULL)",
            "CREATE INDEX exposures_change ON exposures (change_id)",
        ],
        ["DROP TABLE exposures"],
    ),
]
JSON_COLUMNS = ("body", "provenance", "measure")


def _dump(value):
    return None if value is None else json.dumps(value, sort_keys=True)


class Store:
    def __init__(self, path, clock=time.time):
        self.path = path
        self.clock = clock
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row

    def close(self):
        self.db.close()

    def now(self):
        return float(self.clock())

    # Schema ---------------------------------------------------------------
    def schema_version(self):
        return self.db.execute("PRAGMA user_version").fetchone()[0]

    def migrate(self, target=None):
        target = len(MIGRATIONS) if target is None else target
        if not 0 <= target <= len(MIGRATIONS):
            raise ValueError("unknown schema version %s" % target)
        version = self.schema_version()
        while version < target:
            for statement in MIGRATIONS[version][0]:
                self.db.execute(statement)
            version += 1
            self.db.execute("PRAGMA user_version = %d" % version)
        while version > target:
            for statement in MIGRATIONS[version - 1][1]:
                self.db.execute(statement)
            version -= 1
            self.db.execute("PRAGMA user_version = %d" % version)
        self.db.commit()
        return version

    # Changes (versions of definitions) -------------------------------------
    def insert_change(self, kind, key, body, actor_type, actor, note, provenance, status="proposed"):
        version = self.db.execute(
            "SELECT COALESCE(MAX(version), 0) + 1 FROM changes WHERE kind = ? AND key = ?", (kind, key)
        ).fetchone()[0]
        cur = self.db.execute(
            "INSERT INTO changes (kind, key, version, body, actor_type, actor, note, provenance, status, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (kind, key, version, _dump(body), actor_type, actor, note, _dump(provenance), status, self.now()),
        )
        self.db.commit()
        return cur.lastrowid

    def update_change(self, change_id, **fields):
        for name in JSON_COLUMNS:
            if name in fields:
                fields[name] = _dump(fields[name])
        sets = ", ".join("%s = ?" % name for name in fields)
        self.db.execute("UPDATE changes SET %s WHERE id = ?" % sets, list(fields.values()) + [change_id])
        self.db.commit()

    def get_change(self, change_id):
        row = self.db.execute("SELECT * FROM changes WHERE id = ?", (change_id,)).fetchone()
        return self._change(row) if row else None

    def list_changes(self, kind=None, key=None):
        sql, args = "SELECT * FROM changes WHERE 1 = 1", []
        if kind:
            sql, args = sql + " AND kind = ?", args + [kind]
        if key:
            sql, args = sql + " AND key = ?", args + [key]
        return [self._change(r) for r in self.db.execute(sql + " ORDER BY id", args)]

    @staticmethod
    def _change(row):
        change = dict(row)
        for name in JSON_COLUMNS:
            change[name] = json.loads(change[name]) if change[name] is not None else None
        return change

    # Live pointers ------------------------------------------------------------
    def live(self, kind, key):
        row = self.db.execute("SELECT stable, candidate FROM live WHERE kind = ? AND key = ?", (kind, key)).fetchone()
        return (row["stable"], row["candidate"]) if row else (None, None)

    def set_live(self, kind, key, stable, candidate):
        self.db.execute(
            "INSERT INTO live (kind, key, stable, candidate) VALUES (?, ?, ?, ?)"
            " ON CONFLICT (kind, key) DO UPDATE SET stable = excluded.stable, candidate = excluded.candidate",
            (kind, key, stable, candidate),
        )
        self.db.commit()

    def stable_view(self, kind):
        """The definitions everyone sees: {key: body}, leaving out removed ones."""
        rows = self.db.execute(
            "SELECT l.key, c.body FROM live l JOIN changes c ON c.id = l.stable WHERE l.kind = ? ORDER BY l.key", (kind,)
        )
        return {r["key"]: json.loads(r["body"]) for r in rows if r["body"] is not None}

    def candidates(self, kind):
        rows = self.db.execute(
            "SELECT c.* FROM live l JOIN changes c ON c.id = l.candidate WHERE l.kind = ? AND c.status = 'live' ORDER BY c.id",
            (kind,),
        )
        return [self._change(r) for r in rows]

    # Audit ------------------------------------------------------------------------
    def event(self, change_id, actor, event, detail=None):
        self.db.execute(
            "INSERT INTO events (at, change_id, actor, event, detail) VALUES (?, ?, ?, ?, ?)",
            (self.now(), change_id, actor, event, _dump(detail)),
        )
        self.db.commit()

    def events(self, change_id=None):
        sql, args = "SELECT * FROM events", []
        if change_id is not None:
            sql, args = sql + " WHERE change_id = ?", [change_id]
        rows = self.db.execute(sql + " ORDER BY id", args)
        return [dict(r, detail=json.loads(r["detail"]) if r["detail"] else None) for r in rows]

    # Signals ------------------------------------------------------------------------
    def add_signal(self, session, question, answer_key, answer_change, team, exposures):
        cur = self.db.execute(
            "INSERT INTO signals (at, session, question, answer_key, answer_change, team) VALUES (?, ?, ?, ?, ?, ?)",
            (self.now(), session, question, answer_key, answer_change, team),
        )
        self.db.executemany(
            "INSERT INTO exposures (signal_id, change_id, arm) VALUES (?, ?, ?)",
            [(cur.lastrowid, change_id, arm) for change_id, arm in exposures],
        )
        self.db.commit()
        return cur.lastrowid

    def signal(self, signal_id):
        row = self.db.execute("SELECT * FROM signals WHERE id = ?", (signal_id,)).fetchone()
        return self._signal(row) if row else None

    def signals(self, since=None, limit=None):
        sql, args = "SELECT * FROM signals", []
        if since is not None:
            sql, args = sql + " WHERE at >= ?", [since]
        sql += " ORDER BY id DESC" + (" LIMIT %d" % limit if limit else "")
        return [self._signal(r) for r in self.db.execute(sql, args)][::-1]

    @staticmethod
    def _signal(row):
        signal = dict(row)
        signal["expected"] = json.loads(signal["expected"]) if signal["expected"] else None
        return signal

    def set_feedback(self, signal_id, feedback, expected=None):
        self.db.execute(
            "UPDATE signals SET feedback = ?, expected = ? WHERE id = ?", (feedback, _dump(expected), signal_id)
        )
        self.db.commit()

    def link_check(self, signal_id, change_id):
        self.db.execute("UPDATE signals SET check_change = ? WHERE id = ?", (change_id, signal_id))
        self.db.commit()

    def exposure_rows(self, change_id):
        rows = self.db.execute(
            "SELECT e.arm, s.* FROM exposures e JOIN signals s ON s.id = e.signal_id WHERE e.change_id = ? ORDER BY s.id",
            (change_id,),
        )
        return [(r["arm"], self._signal(r)) for r in rows]

    def purge_signals(self, before):
        """Retention: delete signals (and their exposures) recorded before a time."""
        self.db.execute("DELETE FROM exposures WHERE signal_id IN (SELECT id FROM signals WHERE at < ?)", (before,))
        count = self.db.execute("DELETE FROM signals WHERE at < ?", (before,)).rowcount
        self.db.commit()
        return count

    # Backup and restore ------------------------------------------------------------
    def backup(self, dest_path):
        dest = sqlite3.connect(dest_path)
        try:
            self.db.backup(dest)
        finally:
            dest.close()
        return dest_path

    @staticmethod
    def restore(backup_path, into_path):
        """Restore a backup into a fresh location and verify it. Refuses to overwrite a store."""
        if os.path.exists(into_path):
            raise FileExistsError("refusing to restore over an existing store: %s" % into_path)
        source = sqlite3.connect(backup_path)
        dest = sqlite3.connect(into_path)
        try:
            source.backup(dest)
            ok = dest.execute("PRAGMA integrity_check").fetchone()[0]
            version = dest.execute("PRAGMA user_version").fetchone()[0]
        finally:
            source.close()
            dest.close()
        if ok != "ok" or version != len(MIGRATIONS):
            raise RuntimeError("restored store failed verification (integrity %s, schema %s)" % (ok, version))
        return into_path
