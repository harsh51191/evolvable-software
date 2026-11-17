"""Tests for skills/evolvable-software/scripts/recommend.py. Run with: python3 -m unittest discover -s tests"""

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "evolvable-software", "scripts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import recommend  # noqa: E402
import score  # noqa: E402
from test_score import CRITERIA, MODEL, ORDER, assessment, kinds_at, set_score  # noqa: E402

PLAIN = recommend.load_plain(recommend.DEFAULT_PLAIN)
REMEDIATION = score.load_remediation(recommend.DEFAULT_REMEDIATION, CRITERIA)
FIELD = os.path.join(ROOT, "assessments", "2026-09-field-test")


def rec(data):
    return recommend.recommend(data, CRITERIA, ORDER, MODEL, PLAIN, REMEDIATION)


def level_zero_product():
    """Level 0: one main kind people cannot undo; everything else just past Level 1."""
    kinds = kinds_at(1)
    kinds[1]["reach"] = 0
    data = assessment(1, kinds=kinds)
    for cid in ("GOV-05", "DEL-11", "LRN-03"):
        set_score(data, cid, 2)
    return data


class MoveTests(unittest.TestCase):
    def test_three_moves_in_order(self):
        r = rec(level_zero_product())
        self.assertEqual([m["kind"] for m in r["moves"]], ["people", "loop", "safety"])

    def test_a_main_kind_people_cannot_undo_comes_first(self):
        r = rec(level_zero_product())
        first = r["moves"][0]
        self.assertEqual((first["change_kind"], first["from"], first["to"]), ("workflows", 0, 1))
        self.assertIn("themselves, with undo", first["title"])
        self.assertEqual(first["level_alone"], 1)
        self.assertEqual((r["level"], r["next"], r["level_after"]), (0, 1, 1))

    def test_every_move_must_ship_on_by_default(self):
        for m in rec(level_zero_product())["moves"]:
            self.assertTrue(any("standard installation" in d for d in m["done_when"]), m["title"])
            self.assertIn("on by default in the standard installation", m["prompt"])

    def test_self_serve_kinds_move_to_drafted(self):
        data = assessment(1, kinds=kinds_at(1))
        for cid in ("GOV-05", "DEL-11", "LRN-03"):
            set_score(data, cid, 2)
        first = rec(data)["moves"][0]
        self.assertEqual((first["change_kind"], first["to"]), ("settings", 2))

    def test_the_rest_of_the_way_reaches_the_next_level(self):
        data = assessment(1, kinds=kinds_at(1))
        for cid in ("GOV-05", "DEL-11", "LRN-03"):
            set_score(data, cid, 2)
        r = rec(data)
        landed = data
        for step in r["moves"]:
            landed = recommend._apply(landed, step, MODEL)
        self.assertEqual(r["level_after"] >= r["next"], not r["rest"])
        self.assertEqual(r["simulation_errors"], [])

    def test_safety_move_looks_ahead_to_level_three_when_the_next_level_needs_none(self):
        safety = rec(level_zero_product())["moves"][2]
        self.assertEqual(safety["kind"], "safety")
        self.assertIn(safety["criterion"], recommend.CONTROL_OF)

    def test_same_assessment_same_moves(self):
        self.assertEqual(rec(level_zero_product())["moves"], rec(level_zero_product())["moves"])

    def test_render_has_no_unfilled_placeholders(self):
        text = recommend.render(rec(level_zero_product()), PLAIN)
        self.assertNotIn("TODO", text)
        self.assertIn("## For engineers", text)
        self.assertIn("Prompt for a coding agent", text)


class FieldTestTests(unittest.TestCase):
    def test_every_field_test_product_gets_three_valid_moves(self):
        for name in sorted(os.listdir(FIELD)):
            path = os.path.join(FIELD, name, "assessment.json")
            if not os.path.isfile(path):
                continue
            with self.subTest(product=name):
                r, _ = recommend.make(path)
                self.assertEqual(len(r["moves"]), 3)
                self.assertEqual(r["simulation_errors"], [])
                self.assertGreaterEqual(r["level_after"], r["level"])


if __name__ == "__main__":
    unittest.main()
