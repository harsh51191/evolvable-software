"""Wires the parts together: store, door, desk, drafter and scheduler."""
import json
import os
import time

from . import scheduler
from .desk import Desk, redact
from .door import Door
from .drafter import RuleDrafter
from .kinds import ROOT, load_kinds, validate_body
from .store import Store

SEED_DIR = os.path.join(ROOT, "seed")
SOURCE_DIR = os.path.join(ROOT, "sources")
SEED_ORDER = ("policy", "checks", "answers", "routing-rules")
VERSION = "0.1.0"


class App:
    def __init__(self, path, clock=time.time, drafter=None):
        self.store = Store(path, clock)
        self.store.migrate()
        self.kinds = load_kinds()["kinds"]
        self.door = Door(self.store, self.kinds)
        self.desk = Desk(self.store)
        self.drafter = drafter or RuleDrafter(SOURCE_DIR)

    def close(self):
        self.store.close()

    def seed(self, seed_dir=SEED_DIR, overrides=None):
        """Load the starting definitions as version 1 of each, written by the founder.

        This is the only write that does not go through the door, because the door needs a policy
        to exist. It is recorded in the audit trail like any other change.
        """
        if self.store.list_changes():
            raise RuntimeError("the store already has definitions")
        for kind in SEED_ORDER:
            with open(os.path.join(seed_dir, kind + ".json"), encoding="utf-8") as f:
                definitions = json.load(f)
            definitions.update((overrides or {}).get(kind, {}))
            for key, body in sorted(definitions.items()):
                errors = validate_body(self.kinds[kind], body)
                if errors:
                    raise ValueError("seed %s/%s: %s" % (kind, key, "; ".join(errors)))
                change_id = self.store.insert_change(kind, key, body, "person", "person:founder", "starting definition",
                                                     {"seed": True}, status="kept")
                self.store.update_change(change_id, decision="seed", share=1.0, released_at=self.store.now())
                self.store.set_live(kind, key, change_id, None)
                self.store.event(change_id, "person:founder", "seeded")

    def draft(self, question, actor=None):
        """Ask the AI drafter for an answer and send the draft through the door."""
        actor = actor or "ai:" + self.drafter.name
        draft = self.drafter.draft_answer(question)
        if draft is None:
            return {"status": "no_source", "question": question}
        return self.door.submit("answers", draft["key"], draft["body"], actor,
                                "drafted from %s" % draft["body"]["source"],
                                {"question": redact(question).lower().strip(" ?!."), "drafter": self.drafter.name,
                                 "source": draft["body"]["source"]})

    def tick(self):
        return scheduler.tick(self)
