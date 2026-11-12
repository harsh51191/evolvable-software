"""Storage. Every function takes the organisation and every query is scoped to it."""
import json

from desk.matching import normalise

KINDS = ("answer", "rule")


def all_current(conn, org, kind):
    rows = conn.execute("SELECT DISTINCT ON (key) key, version, body FROM definition_versions "
                        "WHERE org_id = %s AND kind = %s ORDER BY key, version DESC", (org, kind)).fetchall()
    return [dict(r["body"], key=r["key"], version=r["version"]) for r in rows]


def save(conn, org, kind, key, body, author, note=""):
    latest = conn.execute("SELECT COALESCE(MAX(version), 0) AS v FROM definition_versions "
                          "WHERE org_id = %s AND kind = %s AND key = %s", (org, kind, key)).fetchone()["v"]
    conn.execute("INSERT INTO definition_versions (org_id, kind, key, version, body, author, note) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)", (org, kind, key, latest + 1, json.dumps(body), author, note))
    return latest + 1


def history(conn, org, kind, key):
    return conn.execute("SELECT version, body, author, note, created_at FROM definition_versions "
                        "WHERE org_id = %s AND kind = %s AND key = %s ORDER BY version DESC", (org, kind, key)).fetchall()


def undo(conn, org, kind, key, author):
    versions = history(conn, org, kind, key)
    if len(versions) < 2:
        return None
    return save(conn, org, kind, key, versions[1]["body"], author, f"undo of version {versions[0]['version']}")


def record_failed_lookup(conn, org, question, area, channel):
    live = conn.execute("SELECT COALESCE(MAX(id), 0) AS v FROM definition_versions WHERE org_id = %s",
                        (org,)).fetchone()["v"]
    conn.execute("INSERT INTO failed_lookups (org_id, question, normalised, area, channel, rules_version) "
                 "VALUES (%s, %s, %s, %s, %s, %s)", (org, question, normalise(question), area, channel, live))


def failure_groups(conn, org, days=14):
    """Failed lookups grouped by question, with samples, areas and the rules versions in force."""
    return conn.execute(
        "SELECT normalised, COUNT(*) AS count, array_agg(DISTINCT area) AS areas, "
        "(array_agg(question ORDER BY created_at DESC))[1:5] AS samples, "
        "MIN(rules_version) AS first_rules_version, MAX(rules_version) AS last_rules_version, "
        "MIN(created_at) AS first_seen, MAX(created_at) AS last_seen FROM failed_lookups "
        "WHERE org_id = %s AND created_at > now() - make_interval(days => %s) "
        "GROUP BY normalised ORDER BY count DESC LIMIT 100", (org, days)).fetchall()


def add_request(conn, org, requester, body):
    return conn.execute("INSERT INTO change_requests (org_id, requester, area, what, examples, rule_keys) "
                        "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                        (org, requester, body["area"], body["what"], json.dumps(body.get("examples", [])),
                         json.dumps(body.get("rule_keys", [])))).fetchone()["id"]


def rows(conn, org, table, status):
    return conn.execute(f"SELECT * FROM {table} WHERE org_id = %s AND status = %s ORDER BY id DESC",
                        (org, status)).fetchall()


def get(conn, org, table, row_id):
    return conn.execute(f"SELECT * FROM {table} WHERE org_id = %s AND id = %s", (org, row_id)).fetchone()


def set_status(conn, org, table, row_id, status):
    conn.execute(f"UPDATE {table} SET status = %s WHERE org_id = %s AND id = %s", (status, org, row_id))


def queue_job(conn, org, payload):
    conn.execute("INSERT INTO jobs (org_id, payload) VALUES (%s, %s)", (org, json.dumps(payload)))


def next_job(conn):
    return conn.execute("UPDATE jobs SET attempts = attempts + 1, status = 'running' WHERE id = (SELECT id FROM jobs "
                        "WHERE status = 'queued' ORDER BY id FOR UPDATE SKIP LOCKED LIMIT 1) RETURNING *").fetchone()


def finish_job(conn, job_id, status, error=None):
    conn.execute("UPDATE jobs SET status = %s, last_error = %s WHERE id = %s", (status, error, job_id))
