"""Versioned answers and routing rules, and the failed-lookup log.

Every save is a new version with its author. Undo saves the previous version again."""
import json

from desk.matching import normalise

KINDS = ("answer", "rule")


def all_current(conn, kind):
    rows = conn.execute(
        "SELECT v.key, v.version, v.body FROM definition_versions v WHERE v.kind = ? AND v.version = "
        "(SELECT MAX(version) FROM definition_versions WHERE kind = v.kind AND key = v.key) ORDER BY v.key",
        (kind,)).fetchall()
    return [dict(json.loads(r["body"]), key=r["key"], version=r["version"]) for r in rows]


def save(conn, kind, key, body, author, note=""):
    latest = conn.execute("SELECT MAX(version) FROM definition_versions WHERE kind = ? AND key = ?",
                          (kind, key)).fetchone()[0] or 0
    conn.execute("INSERT INTO definition_versions (kind, key, version, body, author, note) VALUES (?, ?, ?, ?, ?, ?)",
                 (kind, key, latest + 1, json.dumps(body), author, note))
    conn.commit()
    return latest + 1


def history(conn, kind, key):
    rows = conn.execute("SELECT version, body, author, note, created_at FROM definition_versions "
                        "WHERE kind = ? AND key = ? ORDER BY version DESC", (kind, key)).fetchall()
    return [dict(r, body=json.loads(r["body"])) for r in rows]


def undo(conn, kind, key, author):
    versions = history(conn, kind, key)
    if len(versions) < 2:
        return None
    return save(conn, kind, key, versions[1]["body"], author, f"undo of version {versions[0]['version']}")


def record_failed_lookup(conn, question, area, channel):
    conn.execute("INSERT INTO failed_lookups (question, normalised, area, channel) VALUES (?, ?, ?, ?)",
                 (question, normalise(question), area, channel))
    conn.commit()


def failed_lookups(conn, area=None):
    sql, args = "SELECT * FROM failed_lookups", ()
    if area:
        sql, args = sql + " WHERE area = ?", (area,)
    return [dict(r) for r in conn.execute(sql + " ORDER BY created_at DESC LIMIT 500", args)]
