"""Tests for scripts/score.py. Run with: python3 -m unittest discover -s tests"""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import score  # noqa: E402

RUBRIC = os.path.join(ROOT, "references", "rubric.md")
REMEDIATION = os.path.join(ROOT, "references", "remediation.md")
CRITERIA, ORDER, TITLES, MODEL = score.load_rubric(RUBRIC)


def assessment(value=3, archetype="configurable-application-platform", **overrides):
    data = {"product": "P", "date": "2026-01-01", "source": "repo@abc", "archetype": archetype,
            "scores": {c: {"status": "assessed", "score": value, "grade": "A", "evidence": "src/x.py"}
                       for c in ORDER}}
    for cid, entry in overrides.items():
        data["scores"][cid] = entry
    return data


def run(data, *args):
    tmp = tempfile.mkdtemp()
    try:
        path = os.path.join(tmp, "s.json")
        with open(path, "w") as handle:
            json.dump(data, handle)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = score.main([path, *args])
        return code, out.getvalue()
    finally:
        shutil.rmtree(tmp)


class ModelTests(unittest.TestCase):
    def test_every_criterion_has_a_remediation_entry(self):
        remediation = score.load_remediation(REMEDIATION, CRITERIA)
        self.assertEqual(set(remediation), set(CRITERIA))

    def test_dimension_missing_from_model_is_rejected(self):
        tmp = tempfile.mkdtemp()
        try:
            path = os.path.join(tmp, "rubric.md")
            with open(RUBRIC) as handle:
                text = handle.read() + "\n## Dimension Z: Probe\n\n### Z1 Probe\n- **0** x\n"
            with open(path, "w") as handle:
                handle.write(text)
            with self.assertRaises(SystemExit):
                score.load_rubric(path)
        finally:
            shutil.rmtree(tmp)

    def test_remediation_requires_are_acyclic(self):
        remediation = score.load_remediation(REMEDIATION, CRITERIA)
        zeros = {c: 0 for c in ORDER}
        build, slices = score.schedule(ORDER, zeros, remediation, 3)
        self.assertEqual(sorted(build), sorted(ORDER))
        self.assertEqual(sum(len(s) for s in slices), len(ORDER))


class ValidationTests(unittest.TestCase):
    def errors(self, data):
        return score.validate(data, CRITERIA, ORDER, MODEL)

    def test_valid_assessment_passes(self):
        self.assertEqual(self.errors(assessment()), [])

    def test_string_booleans_are_rejected(self):
        data = assessment()
        data["scores"]["A1"]["single_entity"] = "false"
        data["scores"]["A2"]["incident"] = "no"
        errs = self.errors(data)
        self.assertTrue(any("single_entity must be true or false" in e for e in errs))
        self.assertTrue(any("incident must be true or false" in e for e in errs))

    def test_non_object_entry_is_a_validation_error(self):
        data = assessment(A1=3)
        self.assertTrue(any("A1: entry must be an object" in e for e in self.errors(data)))

    def test_template_placeholders_are_rejected(self):
        data = assessment(A1={"status": "todo"}, A2={"status": "not_evidenced", "searched": "Not evaluated yet"})
        errs = self.errors(data)
        self.assertIn("A1: not yet assessed", errs)
        self.assertTrue(any("A2: not_evidenced needs the searched scope" in e for e in errs))

    def test_exclusion_outside_archetype_is_rejected(self):
        data = assessment(M1={"status": "not_applicable", "rationale": "no"})
        self.assertTrue(any("may not exclude M1" in e for e in self.errors(data)))

    def test_exclusion_inside_archetype_is_accepted(self):
        data = assessment(archetype="agent-runtime", A1={"status": "not_applicable", "rationale": "agent"})
        self.assertEqual(self.errors(data), [])

    def test_available_score_below_score_is_rejected(self):
        data = assessment()
        data["scores"]["F3"]["available_score"] = 1
        self.assertTrue(any("available_score cannot be below score" in e for e in self.errors(data)))


class ScoringTests(unittest.TestCase):
    def result(self, data):
        return score.score_assessment(data, CRITERIA, ORDER, MODEL)

    def test_indexes_do_not_share_dimensions(self):
        seen = [d for members in MODEL["indexes"].values() for d in members]
        self.assertEqual(len(seen), len(set(seen)))

    def test_rounding_is_half_up_and_applied_once(self):
        self.assertEqual(score.r1(1.45), 1.5)
        self.assertEqual(score.r1(2.25), 2.3)
        # Unrounded dimension means feed the index; nothing is rounded before display.
        values = {c: None for c in ORDER}
        values.update({"J1": 0, "J2": 4, "J3": 4, "M1": 2, "M3": 2, "M4": 1, "P1": 2, "P2": 2})
        idx = score.aggregate(values, CRITERIA, MODEL)["indexes"]["learning"]
        self.assertAlmostEqual(idx, (8 / 3 + 5 / 3 + 2) / 3)
        self.assertEqual(score.band(1.49, MODEL), "code-only")
        self.assertEqual(score.band(1.5, MODEL), "mechanism")

    def test_measure_floor_needs_level_three(self):
        data = assessment(2)
        for cid in ("F3",):
            data["scores"][cid]["score"] = 3
        loop = self.result(data)["variants"]["default"]["closed_loop_candidate"]
        self.assertFalse(loop, "M4 and P2 at 2 must not pass the measure floor")
        data["scores"]["P2"]["score"] = 3
        self.assertTrue(self.result(data)["variants"]["default"]["closed_loop_candidate"])

    def test_default_and_available_variants(self):
        data = assessment(2)
        data["scores"]["F3"]["available_score"] = 3
        data["scores"]["P2"]["available_score"] = 3
        res = self.result(data)
        self.assertFalse(res["variants"]["default"]["closed_loop_candidate"])
        self.assertTrue(res["variants"]["available"]["closed_loop_candidate"])

    def test_alternates_produce_a_range(self):
        data = assessment(2)
        data["scores"]["F1"].update(alt_score=3, alt_note="adjacent level also defensible")
        res = self.result(data)
        low, high = res["ranges"]["governance"]
        self.assertLess(low, high)

    def test_not_evidenced_is_zero_in_default_and_excluded_in_assessed_only(self):
        data = assessment(3, M1={"status": "not_evidenced", "searched": "src/"})
        res = self.result(data)
        self.assertEqual(res["variants"]["default"]["effective"]["M1"], 0)
        self.assertIsNone(res["variants"]["assessed_only"]["effective"]["M1"])
        self.assertGreater(res["variants"]["assessed_only"]["indexes"]["learning"],
                           res["variants"]["default"]["indexes"]["learning"])

    def test_grade_c_cap(self):
        data = assessment(4)
        data["scores"]["A1"]["grade"] = "C"
        self.assertEqual(self.result(data)["variants"]["default"]["effective"]["A1"], 2)


class ReviewFixTests(unittest.TestCase):
    """Regression tests for the v0.3 review findings."""

    def errors(self, data):
        return score.validate(data, CRITERIA, ORDER, MODEL)

    def test_opposite_alternates_do_not_cancel(self):
        data = assessment(2)
        data["scores"]["J1"].update(alt_score=3, alt_note="higher reading")
        data["scores"]["J2"].update(alt_score=1, alt_note="lower reading")
        res = score.score_assessment(data, CRITERIA, ORDER, MODEL)
        low, high = res["ranges"]["learning"]
        default = res["variants"]["default"]["indexes"]["learning"]
        self.assertLess(low, default)
        self.assertGreater(high, default)

    def test_alt_score_must_be_adjacent_and_explained(self):
        data = assessment(2)
        data["scores"]["A1"].update(alt_score=4, alt_note="too far")
        data["scores"]["A2"]["alt_score"] = 3
        errs = self.errors(data)
        self.assertIn("A1: alt_score must be an adjacent level (score +/- 1)", errs)
        self.assertIn("A2: alt_score needs an alt_note", errs)

    def test_optional_fields_only_on_their_status(self):
        data = assessment(2, A1={"status": "not_evidenced", "searched": "src/", "alt_score": 1, "alt_note": "x"},
                          A2={"status": "not_evidenced", "searched": "src/", "available_score": 3})
        data["scores"]["A3"]["if_applicable"] = 2
        errs = self.errors(data)
        self.assertIn("A1: alt_score is only allowed when status is assessed", errs)
        self.assertIn("A2: available_score is only allowed when status is assessed", errs)
        self.assertIn("A3: if_applicable is only allowed when status is not_applicable", errs)

    def model_with(self, old, new):
        tmp = tempfile.mkdtemp()
        try:
            path = os.path.join(tmp, "rubric.md")
            with open(RUBRIC) as handle:
                text = handle.read()
            self.assertIn(old, text)
            with open(path, "w") as handle:
                handle.write(text.replace(old, new, 1))
            score.load_rubric(path)
        finally:
            shutil.rmtree(tmp)

    def test_overlapping_indexes_are_rejected(self):
        with self.assertRaises(SystemExit):
            self.model_with('"governance": ["E", "F"]', '"governance": ["E", "F", "A"]')

    def test_dimension_in_two_profiles_is_rejected(self):
        with self.assertRaises(SystemExit):
            self.model_with('"Agent Interface": ["K"]', '"Agent Interface": ["K", "G"]')


class OutputTests(unittest.TestCase):
    def test_pipes_and_newlines_are_escaped_in_the_table(self):
        data = assessment()
        data["scores"]["A1"]["evidence"] = "a || b\nsecond line"
        code, out = run(data)
        self.assertEqual(code, 0)
        row = [line for line in out.splitlines() if line.startswith("| A1 ")][0]
        self.assertEqual(row.count("|") - row.count("\\|"), 8)

    def test_missing_option_value_is_a_usage_error(self):
        with self.assertRaises(SystemExit) as ctx, contextlib.redirect_stderr(io.StringIO()):
            score.main(["x.json", "--prescribe", "--target"])
        self.assertEqual(ctx.exception.code, 2)

    def test_prescription_sends_not_evidenced_to_investigate(self):
        data = assessment(1, A1={"status": "not_evidenced", "searched": "src/"})
        code, out = run(data, "--prescribe", "--json")
        self.assertEqual(code, 0)
        plan = json.loads(out)
        self.assertEqual(plan["investigate_first"], ["A1"])
        scheduled = [item["id"] for sl in plan["slices"] for item in sl]
        self.assertNotIn("A1", scheduled)

    def test_soft_prerequisites_do_not_order_work(self):
        remediation = score.load_remediation(REMEDIATION, CRITERIA)
        self.assertEqual(remediation["N1"]["requires"], [])
        self.assertIn("A1", remediation["N1"]["helps"])

    def test_dependency_cycle_is_an_error(self):
        remediation = {"A1": {"requires": ["B1"]}, "B1": {"requires": ["A1"]}}
        with self.assertRaises(SystemExit):
            score.schedule(["A1", "B1"], {"A1": 0, "B1": 0}, remediation, 3)


if __name__ == "__main__":
    unittest.main()
