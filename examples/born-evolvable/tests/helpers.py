"""Shared set-up for the Answer Desk tests: a fresh store, a fixed clock and simulated customers."""
import copy
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from answerdesk.app import SEED_DIR, App  # noqa: E402

WANTED = {
    "How do I change my password?": "reset-password",
    "How do I export my invoices?": "exporting-invoices",
    "Can an admin change the password rules?": "password-rules",
}


class Clock:
    def __init__(self):
        self.t = 1800000000.0

    def __call__(self):
        self.t += 1
        return self.t


def seed_policy(top=None, **kinds):
    """The seed policy with some rules changed, e.g. seed_policy(answers={"dial": 4})."""
    with open(os.path.join(SEED_DIR, "policy.json"), encoding="utf-8") as f:
        policy = json.load(f)["main"]
    policy.update(top or {})
    for kind, rules in kinds.items():
        policy["kinds"][kind].update(rules)
    return policy


class DeskTest(unittest.TestCase):
    policy = None  # override with seed_policy(...) in a subclass or call self.fresh(policy)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.fresh(self.policy)

    def tearDown(self):
        self.app.close()
        self.tmp.cleanup()

    def fresh(self, policy=None):
        if getattr(self, "app", None):
            self.app.close()
        self.stores = getattr(self, "stores", 0) + 1
        self.clock = Clock()
        self.app = App(os.path.join(self.tmp.name, "desk-%d.db" % self.stores), self.clock)
        self.app.seed(overrides={"policy": {"main": policy}} if policy else None)
        self.door, self.store, self.desk = self.app.door, self.app.store, self.app.desk
        self.session = 0

    def customers(self, plan):
        for question, count in plan:
            for _ in range(count):
                self.session += 1
                reply = self.desk.ask(question, "customer-%d" % self.session)
                if reply["answer_key"]:
                    self.desk.feedback(reply["signal"], reply["answer_key"] == WANTED.get(question))

    def events(self, change_id, name):
        return [e for e in self.store.events(change_id) if e["event"] == name]

    def person_change(self, kind, key, body, share=None):
        change = self.door.submit(kind, key, body, "person:sam", "test")
        self.assertEqual(change["status"], "awaiting_approval", change)
        return self.door.approve(change["id"], "person:sam", share)

    def policy_with(self, **kinds):
        policy = copy.deepcopy(self.door.policy())
        for kind, rules in kinds.items():
            policy["kinds"][kind].update(rules)
        return policy

    def keep_changes(self, n, undo=False):
        ids = []
        for i in range(n):
            change = self.person_change("answers", "opening-hours", {"keywords": ["hours"], "answer": "Version %d." % i})
            if undo:
                self.door.undo(change["id"], "person:sam")
            else:
                self.door.promote(change["id"], "person:sam")
            ids.append(change["id"])
        return ids
