"""Foundations 7, 11 and 12: failures become checks; the policy changes through the door; dials rise on a record."""
import unittest

from helpers import DeskTest, seed_policy

RULES_ANSWER = {"keywords": ["password", "rules"], "need": 2, "answer": "Admins set them under Security settings."}


class FailuresBecomeChecks(DeskTest):
    def test_a_flagged_failure_becomes_a_check_that_then_guards_the_fix(self):
        reply = self.desk.ask("Can an admin change the password rules?", "s1")
        self.assertEqual(reply["answer_key"], "reset-password")
        self.desk.feedback(reply["signal"], False, {"answer": "password-rules"})
        proposed = [a for a in self.app.tick() if a["action"] == "proposed_check"][0]
        check = self.store.get_change(proposed["change"])
        self.assertEqual((check["actor"], check["status"], check["provenance"]), ("product:scheduler", "awaiting_approval",
                                                                                 {"signal": reply["signal"]}))
        self.assertEqual(self.app.tick(), [])  # the same failure is not proposed twice
        self.door.approve(check["id"], "person:sam")
        self.assertFalse(self.events(check["id"], "checked")[-1]["detail"]["report"]["passes_now"])

        fix = self.person_change("answers", "password-rules", RULES_ANSWER)
        self.assertEqual(self.events(fix["id"], "checked")[-1]["detail"]["report"]["fixed"], [check["key"]])
        self.door.promote(fix["id"], "person:sam")
        removal = self.door.submit("answers", "password-rules", None, "person:sam")
        self.assertEqual(removal["status"], "rejected")


class PolicyThroughTheDoor(DeskTest):
    def test_a_person_changes_the_policy_through_the_door(self):
        change = self.door.submit("policy", "main", self.policy_with(**{"routing-rules": {"initial_share": 0.2}}), "person:owner")
        self.assertEqual(change["status"], "awaiting_approval")
        self.door.approve(change["id"], "person:owner")
        self.assertEqual(self.door.policy()["kinds"]["routing-rules"]["initial_share"], 0.2)
        self.assertEqual([e["event"] for e in self.store.events(change["id"])],
                         ["proposed", "checked", "awaiting_approval", "approved", "checked", "released"])

    def test_ai_and_product_cannot_loosen_the_policy_but_the_product_can_tighten_it(self):
        looser = self.policy_with(answers={"protected_keys": []})
        self.assertEqual(self.door.submit("policy", "main", looser, "ai:rule-drafter")["status"], "blocked")
        self.assertEqual(self.door.submit("policy", "main", looser, "product:scheduler")["status"], "blocked")
        tighter = self.door.submit("policy", "main", self.policy_with(answers={"dial": 2}), "product:scheduler")
        self.assertEqual((tighter["status"], tighter["decision"]), ("kept", "pre_approved"))
        self.assertEqual(self.door.policy()["kinds"]["answers"]["dial"], 2)

    def test_raising_a_dial_needs_a_measured_record(self):
        early = self.door.submit("policy", "main", self.policy_with(answers={"dial": 4}), "person:owner")
        self.assertEqual(early["status"], "rejected")
        self.keep_changes(3)
        later = self.door.submit("policy", "main", self.policy_with(answers={"dial": 4}), "person:owner")
        self.assertEqual(self.door.approve(later["id"], "person:owner")["status"], "kept")
        self.assertEqual(self.app.draft("How do I export my invoices?")["decision"], "pre_approved")

    def test_reversals_count_against_raising(self):
        self.keep_changes(3)
        self.keep_changes(2, undo=True)
        change = self.door.submit("policy", "main", self.policy_with(answers={"dial": 4}), "person:owner")
        self.assertEqual(change["status"], "rejected")
        self.assertIn("3 kept, 2 undone", self.events(change["id"], "checked")[0]["detail"]["errors"][0])

    def test_invariants_held_in_code(self):
        self.keep_changes(3)
        for policy in (self.policy_with(answers={"dial": 5}),            # two steps at once
                       self.policy_with(policy={"dial": 4})):            # the policy can never ship without a person
            self.assertEqual(self.door.submit("policy", "main", policy, "person:owner")["status"], "rejected", policy)
        # the rule in force decides, so a raise cannot loosen the rule and use it at once
        loosened = dict(self.door.policy(), raise_rule={"min_kept": 0, "max_reversal_rate": 1.0})
        loosened["kinds"] = dict(loosened["kinds"], **{"routing-rules": dict(loosened["kinds"]["routing-rules"], dial=4)})
        self.assertEqual(self.door.submit("policy", "main", loosened, "person:owner")["status"], "rejected")


class TheLoopIsMeasured(DeskTest):
    def test_a_check_change_is_measured_by_later_changes(self):
        check = self.person_change("checks", "case-hours", {"question": "What are your hours?", "expect": {"answer": "opening-hours"}})
        self.assertEqual(check["measure"]["name"], "changes_kept")
        self.keep_changes(5)
        measured = [a for a in self.app.tick() if a["action"] == "measured"]
        self.assertEqual(measured[0]["change"], check["id"])
        self.assertEqual(measured[0]["result"], {"decision": "keep", "kept_rate": 1.0, "later_changes": 5})

    def test_a_loop_change_followed_by_reversals_is_flagged_for_revision(self):
        self.keep_changes(5)
        check = self.person_change("checks", "case-hours", {"question": "What are your hours?", "expect": {"answer": "opening-hours"}})
        self.keep_changes(5, undo=True)
        self.assertEqual(self.door.evaluate(check["id"])["decision"], "revise")


class SelfChosen(DeskTest):
    policy = seed_policy(answers={"dial": 5})

    def test_at_dial_5_the_product_drafts_for_frequent_unmet_questions(self):
        self.customers([("How do I export my invoices?", 3)])
        drafted = [a for a in self.app.tick() if a["action"] == "drafted"]
        self.assertEqual(drafted, [{"action": "drafted", "question": "how do i export my invoices", "status": "live"}])
        self.assertEqual(self.store.list_changes("answers", "exporting-invoices")[0]["actor"], "product:scheduler")
        self.assertEqual([a for a in self.app.tick() if a["action"] == "drafted"], [])


if __name__ == "__main__":
    unittest.main()
