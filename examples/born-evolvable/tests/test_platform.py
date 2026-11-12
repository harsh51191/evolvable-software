"""Foundations 4, 5 and 10: restore into a fresh place, undoable schema changes, privacy, self-description."""
import contextlib
import io
import json
import os
import sqlite3
import unittest

from helpers import HERE, DeskTest

import walkthrough
from answerdesk import cli
from answerdesk.describe import OPERATIONS, capability_map
from answerdesk.store import MIGRATIONS, Store

TABLES = ("changes", "live", "events", "signals", "exposures")


def dump(path):
    db = sqlite3.connect(path)
    try:
        return {t: db.execute("SELECT * FROM %s ORDER BY rowid" % t).fetchall() for t in TABLES}
    finally:
        db.close()


class BackupAndRestore(DeskTest):
    def test_restore_into_a_fresh_location_matches_and_works(self):
        self.customers([("How do I export my invoices?", 3)])
        self.door.approve(self.app.draft("How do I export my invoices?")["id"], "person:sam")
        backup = self.store.backup(os.path.join(self.tmp.name, "backup.db"))
        os.makedirs(os.path.join(self.tmp.name, "fresh"))
        restored = Store.restore(backup, os.path.join(self.tmp.name, "fresh", "desk.db"))
        self.assertEqual(dump(restored), dump(self.store.path))
        again = Store(restored)
        try:
            self.assertEqual(again.stable_view("answers"), self.store.stable_view("answers"))
            self.assertEqual(len(again.candidates("answers")), 1)
        finally:
            again.close()
        with self.assertRaises(FileExistsError):
            Store.restore(backup, restored)


class Migrations(DeskTest):
    def test_schema_changes_go_down_and_up_without_touching_definitions(self):
        before = self.store.stable_view("answers")
        self.assertEqual(self.store.schema_version(), len(MIGRATIONS))
        self.assertEqual(self.store.migrate(1), 1)
        self.assertIsNone(self.store.db.execute("SELECT name FROM sqlite_master WHERE name = 'exposures'").fetchone())
        self.assertEqual(self.store.migrate(), 2)
        self.assertEqual(self.store.stable_view("answers"), before)


class Privacy(DeskTest):
    def test_signals_hold_no_personal_data(self):
        reply = self.desk.ask("I am jo.bloggs@example.com, call +44 7700 900123 about my invoice", "jo-session")
        row = self.store.signal(reply["signal"])
        self.assertEqual(row["question"], "I am [email], call [number] about my invoice")
        self.assertNotIn("jo-session", json.dumps(row))
        self.assertEqual(row["team"], "billing")

    def test_retention_purges_old_signals(self):
        self.customers([("How do I change my password?", 3)])
        self.clock.t += 40 * 86400
        self.customers([("How do I change my password?", 1)])
        self.assertEqual(self.store.purge_signals(self.clock.t - 30 * 86400), 3)
        self.assertEqual(len(self.store.signals()), 1)


class SelfDescription(DeskTest):
    def test_capability_map_lists_kinds_dials_policy_and_operations(self):
        cmap = json.loads(json.dumps(capability_map(self.app)))
        self.assertEqual(cmap["kinds"]["answers"]["dial_name"], "Carried")
        self.assertEqual(cmap["kinds"]["policy"]["who_may_propose"], ["person"])
        self.assertIn("refunds", cmap["kinds"]["answers"]["limits"]["protected_keys"])
        self.assertEqual({op["name"] for op in cmap["operations"]}, {op["name"] for op in OPERATIONS})

    def test_the_command_line_is_generated_from_the_same_operations(self):
        parser = cli.build_parser()
        commands = parser._subparsers._group_actions[0].choices
        self.assertEqual(set(commands), {op["name"] for op in OPERATIONS})


class CommandLine(DeskTest):
    def run_cli(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = cli.main(["--store", self.path] + list(argv))
        return code, json.loads(out.getvalue()) if code == 0 else None

    def test_a_request_through_the_command_line(self):
        self.path = os.path.join(self.tmp.name, "cli.db")
        self.assertEqual(self.run_cli("init")[0], 0)
        code, reply = self.run_cli("ask", "How do I export my invoices?", "--session", "a")
        self.assertEqual(reply["team"], "billing")
        _, draft = self.run_cli("draft", "How do I export my invoices?")
        self.assertEqual(draft["status"], "awaiting_approval")
        _, live = self.run_cli("approve", str(draft["id"]), "--as", "person:sam")
        self.assertEqual(live["status"], "live")
        self.assertEqual(self.run_cli("approve", str(draft["id"]), "--as", "ai:x")[0], 1)
        _, undone = self.run_cli("undo", str(draft["id"]), "--as", "person:sam")
        self.assertEqual(undone["status"], "undone")
        _, cmap = self.run_cli("describe")
        self.assertEqual(cmap["product"], "Answer Desk")


class Walkthrough(unittest.TestCase):
    def test_the_walkthrough_tells_the_whole_story(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            walkthrough.main(["--quiet"])
        outcome = json.loads(out.getvalue().split("Outcome:", 1)[1])
        self.assertEqual(outcome, {"export": "kept", "bad": "undone", "check": "kept", "again": "rejected",
                                   "better": "kept", "refunds": "blocked", "raise": "rejected"})
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(HERE), "walkthrough.py")))


if __name__ == "__main__":
    unittest.main()
