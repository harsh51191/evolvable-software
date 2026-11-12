"""Foundations 6 and 9: measured changes, gradual release, the off switch and automatic reversal."""
import unittest

from helpers import DeskTest, seed_policy

from answerdesk.desk import bucket


class GradualRelease(DeskTest):
    def test_a_share_of_sessions_sees_the_change_and_each_session_stays_put(self):
        change = self.person_change("answers", "opening-hours", {"keywords": ["hours"], "answer": "NEW"}, share=0.3)
        seen = [self.desk.ask("What are your hours?", "s%d" % i)["text"] == "NEW" for i in range(200)]
        self.assertTrue(0.2 < sum(seen) / 200 < 0.4, sum(seen))
        again = [self.desk.ask("What are your hours?", "s%d" % i)["text"] == "NEW" for i in range(200)]
        self.assertEqual(seen, again)
        rows = self.store.exposure_rows(change["id"])
        self.assertEqual(len(rows), 400)
        self.assertEqual(sum(arm == "candidate" for arm, _ in rows), 2 * sum(seen))

    def test_unrelated_questions_are_not_counted_against_a_change(self):
        change = self.person_change("answers", "opening-hours", {"keywords": ["hours"], "answer": "NEW"})
        self.desk.ask("How do I reset my password?", "s1")
        self.assertEqual(self.store.exposure_rows(change["id"]), [])

    def test_off_switch_stops_it_at_once_and_on_resumes(self):
        change = self.person_change("answers", "opening-hours", {"keywords": ["hours"], "answer": "NEW"}, share=1.0)
        self.assertEqual(self.desk.ask("hours?", "s1")["text"], "NEW")
        self.door.switch_off(change["id"], "product:scheduler")
        self.assertNotEqual(self.desk.ask("hours?", "s1")["text"], "NEW")
        self.door.switch_on(change["id"], "person:sam")
        self.assertEqual(self.desk.ask("hours?", "s1")["text"], "NEW")
        self.assertEqual([e["event"] for e in self.store.events(change["id"])][-2:], ["switched_off", "switched_on"])


class Measurement(DeskTest):
    def test_release_records_baseline_target_and_window(self):
        self.customers([("How do I export my invoices?", 4)])
        change = self.door.approve(self.app.draft("How do I export my invoices?")["id"], "person:sam")
        m = change["measure"]
        self.assertEqual((m["name"], m["baseline"], m["target"], m["window"]), ("answered_and_helpful", 0.0, 0.1, 8))
        self.assertEqual(self.door.evaluate(change["id"])["decision"], "waiting")

    def test_keep_is_applied_by_the_product_at_dial_3(self):
        change = self.door.approve(self.app.draft("How do I export my invoices?")["id"], "person:sam")
        self.customers([("How do I export my invoices?", 24)])
        actions = self.app.tick()
        self.assertEqual(actions[0]["action"], "kept")
        self.assertEqual(self.store.live("answers", "exporting-invoices"), (change["id"], None))

    def test_at_dial_2_a_person_keeps_it(self):
        self.fresh(seed_policy(answers={"dial": 2}))
        change = self.door.approve(self.app.draft("How do I export my invoices?")["id"], "person:sam")
        self.customers([("How do I export my invoices?", 24)])
        self.assertEqual(self.app.tick()[0]["action"], "needs_review")
        self.assertEqual(self.store.get_change(change["id"])["status"], "live")


class AutomaticReversal(DeskTest):
    def release_bad_draft(self):
        self.customers([("How do I change my password?", 4), ("Can an admin change the password rules?", 2)])
        bad = self.app.draft("Can an admin change the password rules?")
        if bad["status"] == "awaiting_approval":
            bad = self.door.approve(bad["id"], "person:sam")
        self.assertEqual(bad["status"], "live")
        self.customers([("How do I change my password?", 3), ("Can an admin change the password rules?", 1)] * 8)
        return bad

    def test_worse_measure_reverses_records_a_wrong_pass_and_proposes_a_check(self):
        bad = self.release_bad_draft()
        actions = self.app.tick()
        self.assertEqual(actions[0]["action"], "reversed")
        self.assertEqual(actions[0]["result"]["decision"], "undo")
        self.assertEqual(self.store.get_change(bad["id"])["status"], "undone")
        self.assertNotIn("password-rules", self.store.stable_view("answers"))
        self.assertEqual(self.desk.ask("How do I change my password?", "x")["answer_key"], "reset-password")
        wrong = self.events(bad["id"], "wrong_pass")[0]["detail"]["checks_that_passed_it"]
        self.assertEqual(len(wrong), 2)
        check = self.store.get_change(actions[1]["change"])
        self.assertEqual((check["kind"], check["actor"], check["status"]), ("checks", "product:scheduler", "awaiting_approval"))
        self.assertEqual(check["body"], {"question": "How do I change my password?", "expect": {"answer": "reset-password"}})

    def test_pre_approved_changes_ship_without_a_person_and_repeated_reversals_lower_the_dial(self):
        self.fresh(seed_policy(top={"demote_after_reversals": 1}, answers={"dial": 4}))
        bad = self.release_bad_draft()
        self.assertEqual(bad["decision"], "pre_approved")
        actions = self.app.tick()
        lowered = [a for a in actions if a["action"] == "lowered_dial"][0]
        self.assertEqual((lowered["to"], lowered["status"]), (3, "kept"))
        self.assertEqual(self.door.policy()["kinds"]["answers"]["dial"], 3)
        self.assertEqual(self.store.get_change(lowered["change"])["actor"], "product:scheduler")


class Bucketing(unittest.TestCase):
    def test_bucket_is_deterministic_and_spread(self):
        values = [bucket(7, "s%d" % i) for i in range(1000)]
        self.assertEqual(values, [bucket(7, "s%d" % i) for i in range(1000)])
        self.assertTrue(0.45 < sum(v < 0.5 for v in values) / 1000 < 0.55)


if __name__ == "__main__":
    unittest.main()
