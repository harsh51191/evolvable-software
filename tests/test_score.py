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
import init_scores  # noqa: E402
import score  # noqa: E402

RUBRIC = os.path.join(ROOT, "references", "rubric.md")
REMEDIATION = os.path.join(ROOT, "references", "remediation.md")
CRITERIA, ORDER, MODEL = score.load_rubric(RUBRIC)
ALL_FACETS = {"implemented": True, "tested": True, "operated": True}


def assessment(value=3, archetype="configurable-application-platform", facts=None, **overrides):
    """An assessment with every criterion at one value; depth facets and inventories filled in."""
    facts = dict({f: True for f in MODEL["scope_facts"]}, **(facts or {}))
    scores = {}
    for cid in ORDER:
        gate = MODEL["applies_when"].get(cid, [])
        gate = [gate] if isinstance(gate, str) else gate
        if gate and not any(facts[f] for f in gate):
            scores[cid] = {"status": "not_applicable", "rationale": "scope fact is false"}
            continue
        entry = {"status": "assessed", "score": value, "grade": "A", "evidence": "src/x.py"}
        if value >= 3:
            entry["facets"] = dict(ALL_FACETS)
        if cid in MODEL["inventories"] and value >= 3:
            entry["inventory"] = {(MODEL["inventories"][cid] or ["surface"])[0]: value}
        scores[cid] = entry
    data = {"product": "P", "date": "2026-01-01", "source": "repo@abc", "archetype": archetype,
            "scope_facts": {f: {"value": v, "evidence": "README"} for f, v in facts.items()},
            "scores": scores}
    for key, entry in overrides.items():
        data["scores"][key.replace("_", "-")] = entry
    return data


def set_score(data, cid, value):
    """Set one criterion, keeping its inventory consistent."""
    entry = data["scores"][cid]
    entry["score"] = value
    if "inventory" in entry:
        entry["inventory"] = {k: value for k in entry["inventory"]}


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


def result(data):
    return score.score_assessment(data, CRITERIA, ORDER, MODEL)


def sal(data, variant="default"):
    return result(data)["variants"][variant]["sal"]


def controls(data):
    return {c["control"]: c["status"] for c in sal(data)["controls"]}


def errors(data):
    return score.validate(data, CRITERIA, ORDER, MODEL)


def rubric_with(old, new):
    """Load a copy of the rubric with one replacement."""
    tmp = tempfile.mkdtemp()
    try:
        path = os.path.join(tmp, "rubric.md")
        with open(RUBRIC) as handle:
            text = handle.read()
        assert old in text, old
        with open(path, "w") as handle:
            handle.write(text.replace(old, new, 1))
        return score.load_rubric(path)
    finally:
        shutil.rmtree(tmp)


class ModelTests(unittest.TestCase):
    def test_sixty_six_criteria_in_six_capabilities(self):
        self.assertEqual(len(ORDER), 66)
        self.assertEqual(list(MODEL["capabilities"]), ["ARC", "DEL", "MAL", "LRN", "GOV", "EXP"])

    def test_every_criterion_has_a_remediation_entry(self):
        remediation = score.load_remediation(REMEDIATION, CRITERIA)
        self.assertEqual(set(remediation), set(CRITERIA))

    def test_remediation_requires_are_acyclic(self):
        remediation = score.load_remediation(REMEDIATION, CRITERIA)
        build, slices = score.schedule(ORDER, {c: 0 for c in ORDER}, remediation, 3)
        self.assertEqual(sorted(build), sorted(ORDER))
        self.assertEqual(sum(len(s) for s in slices), len(ORDER))

    def test_criterion_outside_its_capability_is_rejected(self):
        with self.assertRaises(SystemExit):
            rubric_with("### ARC-02 ", "### DEL-99 ")

    def test_condition_naming_unknown_criterion_is_rejected(self):
        with self.assertRaises(SystemExit):
            rubric_with('"stage": "Stage", "c": "DEL-09"', '"stage": "Stage", "c": "DEL-99"')

    def test_unknown_scope_fact_is_rejected(self):
        with self.assertRaises(SystemExit):
            rubric_with('"ARC-02": "schema_changes"', '"ARC-02": "has_schema"')


class ValidationTests(unittest.TestCase):
    def test_valid_assessment_passes(self):
        self.assertEqual(errors(assessment()), [])
        self.assertEqual(errors(assessment(2)), [])

    def test_scope_facts_need_booleans_and_evidence(self):
        data = assessment()
        data["scope_facts"]["multi_tenant"] = {"value": "yes", "evidence": "x"}
        data["scope_facts"]["hosted_service"]["evidence"] = ""
        errs = errors(data)
        self.assertIn("scope fact multi_tenant: value must be true or false", errs)
        self.assertIn("scope fact hosted_service: needs evidence", errs)

    def test_false_scope_fact_requires_not_applicable(self):
        data = assessment(facts={"multi_tenant": False})
        data["scores"]["ARC-05"] = {"status": "assessed", "score": 2, "grade": "A", "evidence": "x"}
        self.assertTrue(any("ARC-05: does not apply" in e for e in errors(data)))

    def test_scope_fact_allows_exclusion_without_archetype(self):
        self.assertEqual(errors(assessment(facts={"persistent_data": False, "multi_tenant": False})), [])

    def test_exclusion_outside_archetype_is_rejected(self):
        data = assessment(LRN_06={"status": "not_applicable", "rationale": "no"})
        self.assertTrue(any("may not exclude LRN-06" in e for e in errors(data)))

    def test_alt_score_must_be_one_level_up(self):
        data = assessment(2)
        data["scores"]["MAL-01"].update(alt_score=1, alt_note="lower reading")
        data["scores"]["MAL-02"]["alt_score"] = 3
        errs = errors(data)
        self.assertTrue(any(e.startswith("MAL-01: alt_score must be the next level up") for e in errs))
        self.assertIn("MAL-02: alt_score needs an alt_note", errs)

    def test_depth_capped_criterion_at_three_needs_facets(self):
        data = assessment(2)
        data["scores"]["ARC-03"]["score"] = 3
        data["scores"]["GOV-04"].update(alt_score=3, alt_note="higher")
        errs = errors(data)
        self.assertIn("ARC-03: depth-capped criterion read at 3 or more needs facets", errs)
        self.assertIn("GOV-04: depth-capped criterion read at 3 or more needs facets", errs)

    def test_facets_must_be_cumulative(self):
        data = assessment()
        data["scores"]["ARC-03"]["facets"] = {"implemented": False, "tested": True, "operated": False}
        self.assertIn("ARC-03: tested or operated facets require implemented", errors(data))

    def test_inventory_score_must_equal_weakest_surface(self):
        data = assessment()
        data["scores"]["ARC-09"]["inventory"] = {"data": 3, "files": 2}
        del data["scores"]["ARC-08"]["inventory"]
        errs = errors(data)
        self.assertIn("ARC-09: score 3 exceeds the lowest inventory level 2", errs)
        self.assertIn("ARC-08: inventory criterion scored 3 or more needs an inventory", errs)

    def test_string_booleans_and_placeholders_are_rejected(self):
        data = assessment(MAL_01={"status": "todo"},
                          MAL_02={"status": "not_evidenced", "searched": "Not evaluated yet"})
        data["scores"]["MAL-03"]["single_entity"] = "false"
        errs = errors(data)
        self.assertIn("MAL-01: not yet assessed", errs)
        self.assertTrue(any("MAL-02: not_evidenced needs the searched scope" in e for e in errs))
        self.assertTrue(any("MAL-03: single_entity must be true or false" in e for e in errs))

    def test_available_score_below_score_is_rejected(self):
        data = assessment()
        data["scores"]["GOV-07"]["available_score"] = 1
        self.assertTrue(any("available_score cannot be below score" in e for e in errors(data)))

    def test_init_template_is_rejected_until_filled(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            init_scores.main(["--product", "P", "--archetype", "other", "--source", "x"])
        errs = errors(json.loads(out.getvalue()))
        self.assertIn("scope fact persistent_data: value must be true or false", errs)
        self.assertIn("ARC-01: not yet assessed", errs)


class DepthTests(unittest.TestCase):
    def test_untested_three_counts_as_two(self):
        data = assessment()
        data["scores"]["ARC-09"]["facets"] = {"implemented": True, "tested": False, "operated": True}
        res = result(data)
        self.assertEqual(res["variants"]["default"]["effective"]["ARC-09"], 2)
        self.assertIn("ARC-09: evidence depth caps 3 -> 2", res["flags"])

    def test_four_without_operated_counts_as_three(self):
        data = assessment(4)
        data["scores"]["ARC-03"]["facets"] = {"implemented": True, "tested": True, "operated": False}
        self.assertEqual(result(data)["variants"]["default"]["effective"]["ARC-03"], 3)

    def test_depth_does_not_cap_other_criteria(self):
        data = assessment()
        del data["scores"]["MAL-01"]["facets"]
        self.assertEqual(errors(data), [])
        self.assertEqual(result(data)["variants"]["default"]["effective"]["MAL-01"], 3)


class LevelTests(unittest.TestCase):
    def test_everything_at_four_with_operated_evidence_is_level_five(self):
        out = sal(assessment(4))
        self.assertEqual(out["headline"], 5)
        self.assertEqual({l: v["level"] for l, v in out["loops"].items()},
                         {"request": 5, "fix": 5, "expansion": 5})

    def test_everything_at_three_is_level_three_because_rollback_is_not_automatic(self):
        out = sal(assessment(3))
        self.assertEqual(out["headline"], 3)
        self.assertTrue(all(c["status"] == "pass" for c in out["controls"]))
        self.assertTrue(all(b["stage"] == "Roll back" for b in out["loops"]["request"]["blockers"]))

    def test_automatic_rollback_unlocks_level_four(self):
        data = assessment(3)
        set_score(data, "GOV-05", 4)
        set_score(data, "DEL-11", 4)
        self.assertEqual(sal(data)["headline"], 4)

    def test_release_rollback_only_counts_with_code_release_path(self):
        data = assessment(3, facts={"code_release_path": False})
        set_score(data, "GOV-05", 4)
        self.assertEqual(sal(data)["headline"], 4)

    def test_everything_at_two_is_level_two_and_controls_fail(self):
        out = sal(assessment(2))
        self.assertEqual(out["headline"], 2)
        failing = {c["control"] for c in out["controls"] if c["status"] == "fail"}
        self.assertIn("Tested backup and restore", failing)
        self.assertIn("Security as infrastructure", failing)

    def test_weak_architecture_caps_every_loop(self):
        data = assessment(3)
        data["scores"]["ARC-06"] = {"status": "assessed", "score": 1, "grade": "A", "evidence": "x"}
        out = sal(data)
        self.assertEqual(out["headline"], 2)
        request = out["loops"]["request"]
        self.assertEqual(request["parts"]["architecture"], 2)
        self.assertEqual(request["parts"]["spine"], 3)
        self.assertTrue(any("ARC-06 1" in b["observed"] for b in request["blockers"]))

    def test_failed_control_caps_at_two(self):
        data = assessment(3)
        data["scores"]["ARC-02"] = {"status": "assessed", "score": 2, "grade": "A", "evidence": "x"}
        self.assertEqual(sal(data)["headline"], 2)
        self.assertEqual(controls(data)["Safe migrations"], "fail")

    def test_controls_do_not_apply_without_their_scope_fact(self):
        data = assessment(3, facts={"schema_changes": False, "multi_tenant": False, "code_release_path": False})
        status = controls(data)
        self.assertEqual(status["Safe migrations"], "n/a")
        self.assertEqual(status["Tenant isolation"], "n/a")
        self.assertEqual(status["Release rollback"], "n/a")

    def test_bounded_self_change_only_when_self_change_is_possible(self):
        data = assessment(3, facts={"agent_mutations": False, "automatic_apply": False})
        self.assertEqual(errors(data), [])
        self.assertEqual(data["scores"]["GOV-10"]["status"], "not_applicable")
        self.assertEqual(controls(data)["Bounded self-change"], "n/a")
        data = assessment(3, facts={"agent_mutations": False})
        data["scores"]["GOV-10"] = {"status": "assessed", "score": 1, "grade": "A", "evidence": "x"}
        self.assertEqual(controls(data)["Bounded self-change"], "fail")

    def test_headline_is_the_lower_of_request_and_fix(self):
        data = assessment(3)
        data["scores"]["LRN-05"] = {"status": "assessed", "score": 1, "grade": "A", "evidence": "x"}
        data["scores"]["EXP-04"] = {"status": "assessed", "score": 0, "grade": "A", "evidence": "x"}
        out = sal(data)
        self.assertEqual(out["loops"]["request"]["level"], 3)
        self.assertEqual(out["loops"]["fix"]["level"], 1)
        self.assertEqual(out["loops"]["expansion"]["level"], 1)
        self.assertEqual(out["headline"], 1)

    def test_people_build_path_gives_level_one(self):
        data = assessment(0)
        for cid in [c for c in ORDER if c.startswith("MAL-")] + ["GOV-05", "DEL-11"]:
            data["scores"][cid]["score"] = 2
        out = sal(data)
        self.assertEqual(out["loops"]["request"]["level"], 1)
        self.assertEqual(out["loops"]["fix"]["level"], 0)

    def test_opt_in_and_alternate_variants(self):
        data = assessment(3)
        data["scores"]["DEL-10"].update(score=1, available_score=2)
        data["scores"]["DEL-09"].update(score=1, alt_score=2, alt_note="adjacent")
        res = result(data)
        self.assertEqual(res["variants"]["default"]["sal"]["headline"], 2)
        self.assertEqual(res["variants"]["high"]["sal"]["headline"], 2)
        data["scores"]["DEL-09"]["available_score"] = 2
        res = result(data)
        self.assertEqual(res["variants"]["available"]["sal"]["headline"], 3)
        self.assertLess(res["ranges"]["DEL"][0], res["ranges"]["DEL"][1])


class ScoringTests(unittest.TestCase):
    def test_rounding_is_half_up_and_applied_once(self):
        self.assertEqual(score.r1(1.45), 1.5)
        self.assertEqual(score.r1(2.25), 2.3)

    def test_capability_is_mean_of_area_means(self):
        values = {c: None for c in ORDER}
        values.update({"EXP-01": 0, "EXP-02": 0, "EXP-03": 3, "EXP-04": 4, "EXP-05": 2, "EXP-06": 1})
        caps = score.aggregate(values, CRITERIA, MODEL)["capabilities"]
        self.assertAlmostEqual(caps["EXP"], (1 + 3 + 1) / 3)

    def test_not_evidenced_is_zero_by_default_and_excluded_in_assessed_only(self):
        data = assessment(3, LRN_06={"status": "not_evidenced", "searched": "src/"})
        res = result(data)
        self.assertEqual(res["variants"]["default"]["effective"]["LRN-06"], 0)
        self.assertIsNone(res["variants"]["assessed_only"]["effective"]["LRN-06"])

    def test_grade_c_cap(self):
        data = assessment(4)
        data["scores"]["MAL-01"]["grade"] = "C"
        self.assertEqual(result(data)["variants"]["default"]["effective"]["MAL-01"], 2)


class OutputTests(unittest.TestCase):
    def test_pipes_and_newlines_are_escaped_in_the_table(self):
        data = assessment()
        data["scores"]["MAL-01"]["evidence"] = "a || b\nsecond line"
        code, out = run(data)
        self.assertEqual(code, 0)
        row = [line for line in out.splitlines() if line.startswith("| MAL-01 ")][0]
        self.assertEqual(row.count("|") - row.count("\\|"), 9)

    def test_report_names_blockers(self):
        data = assessment(3)
        data["scores"]["ARC-06"] = {"status": "assessed", "score": 1, "grade": "A", "evidence": "x"}
        code, out = run(data)
        self.assertEqual(code, 0)
        self.assertIn("**SAL 2 (Assisted)", out)
        self.assertIn("ARC-06 1", out)

    def test_missing_option_value_is_a_usage_error(self):
        with self.assertRaises(SystemExit) as ctx, contextlib.redirect_stderr(io.StringIO()):
            score.main(["x.json", "--prescribe", "--target"])
        self.assertEqual(ctx.exception.code, 2)

    def test_prescription_sends_not_evidenced_to_investigate(self):
        data = assessment(1, MAL_01={"status": "not_evidenced", "searched": "src/"})
        code, out = run(data, "--prescribe", "--json")
        self.assertEqual(code, 0)
        plan = json.loads(out)
        self.assertEqual(plan["investigate_first"], ["MAL-01"])
        self.assertNotIn("MAL-01", [item["id"] for sl in plan["slices"] for item in sl])
        self.assertIn("Request → Release", plan["next_level_blockers"])

    def test_soft_prerequisites_do_not_order_work(self):
        remediation = score.load_remediation(REMEDIATION, CRITERIA)
        self.assertEqual(remediation["MAL-16"]["requires"], [])
        self.assertIn("MAL-01", remediation["MAL-16"]["helps"])

    def test_dependency_cycle_is_an_error(self):
        remediation = {"MAL-01": {"requires": ["MAL-02"]}, "MAL-02": {"requires": ["MAL-01"]}}
        with self.assertRaises(SystemExit):
            score.schedule(["MAL-01", "MAL-02"], {"MAL-01": 0, "MAL-02": 0}, remediation, 3)


if __name__ == "__main__":
    unittest.main()
