"""Foundations 1 to 4, 7 and 8: kinds, versioned data, one door, undo, checks and written limits."""
import unittest

from helpers import DeskTest, seed_policy

from answerdesk.door import DoorError
from answerdesk.kinds import load_kinds


class KindsAndVersions(DeskTest):
    def test_kinds_are_declared_once_and_the_policy_covers_each(self):
        kinds = load_kinds()["kinds"]
        self.assertEqual(set(kinds), {"answers", "routing-rules", "checks", "policy"})
        self.assertEqual(set(self.door.policy()["kinds"]), set(kinds))
        self.assertTrue(any(k["main"] for k in kinds.values()))
        with self.assertRaises(DoorError):
            self.door.submit("prices", "basic", {"amount": 1}, "person:sam")

    def test_every_version_has_an_author_a_status_and_a_number(self):
        change = self.person_change("answers", "opening-hours", {"keywords": ["hours"], "answer": "Always open."})
        history = self.store.list_changes("answers", "opening-hours")
        self.assertEqual([c["version"] for c in history], [1, 2])
        self.assertEqual(history[0]["actor"], "person:founder")
        self.assertEqual((change["actor"], change["status"], change["replaces"]), ("person:sam", "live", history[0]["id"]))

    def test_invalid_definitions_are_rejected_with_plain_errors(self):
        change = self.door.submit("answers", "x", {"keywords": "hours", "answer": ""}, "person:sam")
        self.assertEqual(change["status"], "rejected")
        errors = self.events(change["id"], "checked")[0]["detail"]["errors"]
        self.assertIn("'keywords' must be a list of words", errors)
        self.assertIn("'answer' must be non-empty text", errors)


class OneDoorAndUndo(DeskTest):
    def test_people_need_a_person_to_release(self):
        change = self.door.submit("answers", "opening-hours", {"keywords": ["hours"], "answer": "Always."}, "person:sam")
        self.assertEqual((change["status"], change["decision"]), ("awaiting_approval", "needs_person"))
        with self.assertRaises(DoorError):
            self.door.approve(change["id"], "ai:rule-drafter")
        self.assertEqual(self.door.approve(change["id"], "person:kim")["status"], "live")

    def test_undo_answers_live_and_kept(self):
        old = self.store.stable_view("answers")["opening-hours"]
        live = self.person_change("answers", "opening-hours", {"keywords": ["hours"], "answer": "Always open."})
        self.door.undo(live["id"], "person:sam")
        self.assertEqual(self.store.live("answers", "opening-hours")[1], None)
        kept = self.person_change("answers", "opening-hours", {"keywords": ["hours"], "answer": "Always open."})
        self.door.promote(kept["id"], "person:sam")
        self.assertEqual(self.store.stable_view("answers")["opening-hours"]["answer"], "Always open.")
        self.door.undo(kept["id"], "person:sam")
        self.assertEqual(self.store.stable_view("answers")["opening-hours"], old)

    def test_undo_routing_rules_including_a_removal(self):
        removal = self.person_change("routing-rules", "bugs", None, share=1.0)
        self.door.promote(removal["id"], "person:sam")
        self.assertNotIn("bugs", self.store.stable_view("routing-rules"))
        self.door.undo(removal["id"], "person:sam")
        self.assertEqual(self.store.stable_view("routing-rules")["bugs"]["team"], "engineering")

    def test_undo_checks(self):
        change = self.person_change("checks", "case-hours", {"question": "When are you open?", "expect": {"answer": "opening-hours"}})
        self.assertEqual(change["status"], "kept")
        self.door.undo(change["id"], "person:sam")
        self.assertNotIn("case-hours", self.store.stable_view("checks"))

    def test_undo_policy_only_by_a_person_and_never_the_first(self):
        first = self.store.live("policy", "main")[0]
        change = self.person_change("policy", "main", self.policy_with(**{"routing-rules": {"dial": 2}}))
        self.assertEqual(self.door.policy()["kinds"]["routing-rules"]["dial"], 2)
        with self.assertRaises(DoorError):
            self.door.undo(change["id"], "product:scheduler")
        self.door.undo(change["id"], "person:sam")
        self.assertEqual(self.door.policy()["kinds"]["routing-rules"]["dial"], 3)
        with self.assertRaises(DoorError):
            self.door.undo(first, "person:sam")

    def test_undo_is_one_step_at_a_time(self):
        a = self.person_change("answers", "opening-hours", {"keywords": ["hours"], "answer": "A."})
        self.door.promote(a["id"], "person:sam")
        b = self.person_change("answers", "opening-hours", {"keywords": ["hours"], "answer": "B."})
        with self.assertRaises(DoorError):
            self.door.undo(a["id"], "person:sam")
        self.door.undo(b["id"], "person:sam")
        self.door.undo(a["id"], "person:sam")


class ChecksRunOnEveryChange(DeskTest):
    def test_a_regression_is_rejected(self):
        change = self.door.submit("answers", "reset-password", {"keywords": ["reset"], "answer": "Use the link."}, "person:sam")
        self.assertEqual(change["status"], "rejected")
        report = self.events(change["id"], "checked")[0]["detail"]["report"]
        self.assertEqual(report["regressions"], ["case-reset"])

    def test_approval_reruns_the_checks(self):
        greedy = self.door.submit("answers", "lockout", {"keywords": ["forgot", "password", "locked"], "need": 2,
                                                         "answer": "Wait ten minutes."}, "person:sam")
        self.assertEqual(greedy["status"], "rejected")  # 'I forgot my password' would now get the lockout answer
        ok = self.door.submit("answers", "lockout", {"keywords": ["locked"], "answer": "Wait ten minutes."}, "person:sam")
        self.person_change("checks", "case-locked", {"question": "my password is locked", "expect": {"answer": "reset-password"}})
        self.assertEqual(self.door.approve(ok["id"], "person:sam")["status"], "rejected")


class LimitsOutsideTheAI(DeskTest):
    def test_protected_answers_are_blocked_for_the_ai_and_logged(self):
        change = self.app.draft("Do refunds go back to my card?")
        self.assertEqual((change["key"], change["status"]), ("refunds", "blocked"))
        self.assertIn("protected", self.events(change["id"], "blocked")[0]["detail"]["reason"])
        self.assertEqual(self.store.stable_view("answers")["refunds"]["answer"][:30], "Refunds go back to the origina")

    def test_ai_may_not_remove_definitions_or_change_checks(self):
        removal = self.door.submit("answers", "opening-hours", None, "ai:rule-drafter")
        self.assertEqual(removal["status"], "blocked")
        weaken = self.door.submit("checks", "case-reset", {"question": "x", "expect": {"answer": None}}, "product:scheduler")
        self.assertEqual(weaken["status"], "blocked")

    def test_the_dial_decides_who_may_propose(self):
        self.fresh(seed_policy(answers={"dial": 1}))
        self.assertEqual(self.app.draft("How do I export my invoices?")["status"], "blocked")
        self.fresh(seed_policy(answers={"dial": 2}))
        self.assertEqual(self.app.draft("How do I export my invoices?")["status"], "awaiting_approval")
        self.assertEqual(self.door.submit("answers", "x", {"keywords": ["x"], "answer": "x"}, "product:scheduler")["status"], "blocked")

    def test_daily_limit_on_changes_without_a_person(self):
        self.fresh(seed_policy(answers={"dial": 4, "max_auto_per_day": 1}))
        first = self.app.draft("How do I export my invoices?")
        self.assertEqual((first["status"], first["decision"], first["share"]), ("live", "pre_approved", 0.5))
        second = self.app.draft("Can an admin change the password rules?")
        self.assertEqual(second["status"], "blocked")
        self.assertIn("limit", self.events(second["id"], "blocked")[0]["detail"]["reason"])
        self.clock.t += 86400
        self.assertEqual(self.app.draft("Can an admin change the password rules?")["status"], "live")


if __name__ == "__main__":
    unittest.main()
