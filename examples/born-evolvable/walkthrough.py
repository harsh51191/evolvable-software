"""Five-minute walkthrough of Answer Desk. Deterministic: a fixed clock and simulated customers.

    python3 walkthrough.py            # uses a temporary store
    python3 walkthrough.py --store desk.db --quiet

Simulated customers mark an answer helpful when it is the one they needed; nothing here is real
traffic. Every step uses the same door, policy and checks as the command line.
"""
import argparse
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from answerdesk.app import App  # noqa: E402
from answerdesk.describe import capability_map  # noqa: E402

WANTED = {  # what each simulated customer actually needed
    "How do I change my password?": "reset-password",
    "How do I export my invoices?": "exporting-invoices",
    "Can an admin change the password rules?": "password-rules",
}


class Clock:
    def __init__(self):
        self.t = 1800000000.0

    def __call__(self):
        self.t += 60
        return self.t


class Walkthrough:
    def __init__(self, path, quiet=False):
        self.app = App(path, Clock())
        self.quiet = quiet
        self.session = 0

    def say(self, text, data=None):
        if not self.quiet:
            print(text)
            if data is not None:
                print("   " + json.dumps(data, sort_keys=True))

    def customers(self, plan):
        """plan: list of (question, how many). Each customer is a new session and gives feedback."""
        for question, count in plan:
            for _ in range(count):
                self.session += 1
                reply = self.app.desk.ask(question, "customer-%d" % self.session)
                if reply["answer_key"]:
                    self.app.desk.feedback(reply["signal"], reply["answer_key"] == WANTED[question])

    def brief(self, change):
        keys = ("id", "kind", "key", "actor", "status", "decision", "share")
        return {k: change[k] for k in keys}

    def run(self):
        app, door = self.app, self.app.door
        app.seed()
        self.say("1. Answer Desk starts with three answers, two routing rules, two checks and a policy.")
        self.say("   Dials:", {k: v["dial"] for k, v in door.policy()["kinds"].items()})

        self.customers([("How do I change my password?", 4), ("How do I export my invoices?", 3),
                        ("Can an admin change the password rules?", 2)])
        self.say("\n2. Customers ask questions. Every question is a signal; unmet ones are grouped:", app.desk.unmet())

        draft = app.draft("How do I export my invoices?")
        self.say("\n3. The AI drafter (a rule-based stand-in) drafts an answer from the help centre."
                 " Checks pass; the answers dial is 3, so a person approves:", self.brief(draft))
        released = door.approve(draft["id"], "person:sam")
        self.say("   Released to half the traffic, with a baseline and a target:", released["measure"])

        self.customers([("How do I export my invoices?", 24)])
        self.say("\n4. After more questions the product measures the change and keeps it:", app.tick())

        bad = app.draft("Can an admin change the password rules?")
        door.approve(bad["id"], "person:sam")
        self.say("\n5. The AI drafts a 'password rules' answer. It passes every check, and a person approves it.",
                 self.brief(door.store.get_change(bad["id"])))
        self.customers([("How do I change my password?", 3), ("Can an admin change the password rules?", 1)] * 8)
        actions = app.tick()
        self.say("   But it also catches 'How do I change my password?'. The measure gets worse, so the product"
                 " reverses it, records that the checks missed it, and proposes a new check:", actions)

        check_id = [a for a in actions if a["action"] == "proposed_check"][0]["change"]
        door.approve(check_id, "person:sam")
        again = app.draft("Can an admin change the password rules?")
        self.say("\n6. A person approves the new check. The same draft is now rejected at the door:",
                 {"status": again["status"], "why": [e["detail"]["errors"] for e in app.store.events(again["id"])
                                                     if e["event"] == "checked"][0]})
        better = door.submit("answers", "password-rules", {
            "keywords": ["password", "rules"], "need": 2, "source": "sources/help-centre.md#password-rules",
            "answer": "A password must be at least 12 characters long. Administrators can change the password rules"
                      " under Security settings."}, "person:sam", "narrower keywords")
        door.approve(better["id"], "person:sam")
        self.customers([("Can an admin change the password rules?", 20)])
        self.say("   A person writes a narrower answer; it passes the new check and is kept:", app.tick())

        blocked = app.draft("Do refunds go back to my card?")
        self.say("\n7. The AI drafts a change to the refunds answer. Refunds are protected, so the policy blocks"
                 " it in code:", [e["detail"] for e in app.store.events(blocked["id"]) if e["event"] == "blocked"][0])

        policy = door.policy()
        raised = json.loads(json.dumps(policy))
        raised["kinds"]["answers"]["dial"] = 4
        attempt = door.submit("policy", "main", raised, "person:owner", "let answers ship without a person")
        self.say("\n8. The owner tries to let answers ship without a person. The policy is a definition too, so"
                 " the change goes through the door, which reads the record:",
                 {"status": attempt["status"], "why": [e["detail"]["errors"] for e in app.store.events(attempt["id"])
                                                       if e["event"] == "checked"][0]})

        cmap = capability_map(app)
        self.say("\n9. The capability map an agent reads (summary):",
                 {k: {"dial": v["dial"], "dial_name": v["dial_name"], "who_may_propose": v["who_may_propose"]}
                  for k, v in cmap["kinds"].items()})
        return {"export": door.store.get_change(draft["id"])["status"], "bad": door.store.get_change(bad["id"])["status"],
                "check": door.store.get_change(check_id)["status"], "again": again["status"],
                "better": door.store.get_change(better["id"])["status"], "refunds": blocked["status"],
                "raise": attempt["status"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--store", help="path for the store (default: a temporary file)")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory() as tmp:
        walk = Walkthrough(args.store or os.path.join(tmp, "walkthrough.db"), args.quiet)
        try:
            outcome = walk.run()
        finally:
            walk.app.close()
    print("\nOutcome:", json.dumps(outcome, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
