"""Tests for skills/evolvable-software/scripts/score.py. Run with: python3 -m unittest discover -s tests"""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "evolvable-software")
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import init_scores  # noqa: E402
import score  # noqa: E402

RUBRIC = os.path.join(SKILL, "references", "rubric.md")
REMEDIATION = os.path.join(SKILL, "references", "remediation.md")
CRITERIA, ORDER, MODEL = score.load_rubric(RUBRIC)
ALL_FACETS = {"implemented": True, "tested": True, "operated": True}


def kinds_at(reach, main=(True, True, False)):
    """Kinds of change, all at one reach: two main kinds and one that is not, unless main says otherwise."""
    names = ("settings", "workflows", "reports")
    return [{"id": names[i], "name": f"Change the {names[i]}", "who": "admins", "main": m, "reach": reach,
             "evidence": f"docs/{names[i]}.md"} for i, m in enumerate(main)]


def assessment(value=3, archetype="configurable-application-platform", facts=None, kinds=None, **overrides):
    """An assessment with every criterion at one value; depth facets and inventories filled in.

    The kinds of change default to self-serve (reach 1) when value is 2 or more and to engineers only
    (reach 0) below that. Before v0.7 the people build path was the MAL average, which equals value here,
    and passed at 2; this keeps every uniform assessment at the level it had, and reach 1 needs no other
    criterion, so tests that lower one criterion keep their meaning."""
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
            entry["inventory"] = {s: value for s in (MODEL["inventories"][cid] or ["surface"])}
        scores[cid] = entry
    view = MODEL["ai_view"]
    for cid in view["readings"]:
        fact = view["reading_applies_when"].get(cid)
        if scores[cid]["status"] == "not_applicable" or (fact and not facts[fact]):
            scores[cid]["ai"] = {"status": "not_applicable", "rationale": "does not apply"}
        elif facts["ai_features"]:
            scores[cid]["ai"] = {"status": "assessed", "score": value, "grade": "A", "evidence": "src/ai.py"}
            if value >= 3:
                scores[cid]["ai"]["facets"] = dict(ALL_FACETS)
    data = {"product": "P", "date": "2026-01-01", "source": "repo@abc", "archetype": archetype,
            "scope_facts": {f: {"value": v, "evidence": "README"} for f, v in facts.items()},
            "change_kinds": kinds_at(1 if value >= 2 else 0) if kinds is None else kinds,
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
    def test_sixty_seven_criteria_in_six_capabilities_plus_eight_ai_checks(self):
        self.assertEqual(len([c for c in ORDER if not CRITERIA[c]["ai_check"]]), 67)
        self.assertEqual(len(ORDER), 75)
        self.assertEqual(MODEL["version"], "0.7.0")
        self.assertEqual(len([c for c in ORDER if CRITERIA[c]["ai_check"]]), 8)
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
        data["scores"]["ARC-09"]["inventory"] = {"data": 3, "definitions": 3, "files": 2, "secrets": "n/a"}
        del data["scores"]["ARC-08"]["inventory"]
        errs = errors(data)
        self.assertIn("ARC-09: score 3 exceeds the lowest inventory level 2", errs)
        self.assertIn("ARC-08: inventory criterion read at 3 or more needs an inventory", errs)

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

    def test_a_four_needs_tested_only(self):
        data = assessment(4)
        data["scores"]["ARC-03"]["facets"] = {"implemented": True, "tested": True, "operated": False}
        self.assertEqual(result(data)["variants"]["default"]["effective"]["ARC-03"], 4)
        data["scores"]["ARC-03"]["facets"] = {"implemented": True, "tested": False, "operated": True}
        res = result(data)
        self.assertEqual(res["variants"]["default"]["effective"]["ARC-03"], 2)
        self.assertIn("ARC-03: evidence depth caps 4 -> 2", res["flags"])

    def test_depth_does_not_cap_other_criteria(self):
        data = assessment()
        del data["scores"]["MAL-01"]["facets"]
        self.assertEqual(errors(data), [])
        self.assertEqual(result(data)["variants"]["default"]["effective"]["MAL-01"], 3)


class LevelTests(unittest.TestCase):
    def test_everything_at_four_with_tested_evidence_is_level_five(self):
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
        data = assessment(3, facts={"agent_mutations": False, "evolution_auto_apply": False})
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
        data = assessment(0, kinds=kinds_at(1))
        for cid in ("GOV-05", "DEL-11"):
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



class ReviewRoundTests(unittest.TestCase):
    """Regression tests for the second review of the v0.4 implementation."""

    def test_alternate_reading_cannot_bypass_inventory(self):
        data = assessment(3)
        data["scores"]["ARC-09"] = {"status": "assessed", "score": 2, "grade": "A", "evidence": "x",
                                    "alt_score": 3, "alt_note": "higher", "facets": dict(ALL_FACETS)}
        self.assertIn("ARC-09: inventory criterion read at 3 or more needs an inventory", errors(data))
        data["scores"]["ARC-09"]["inventory"] = {"data": 3, "definitions": 3, "files": 2, "secrets": 3}
        self.assertIn("ARC-09: alt_score 3 exceeds the lowest inventory level 2", errors(data))

    def test_scoring_caps_any_reading_at_the_weakest_surface(self):
        data = assessment(3)
        data["scores"]["ARC-09"].update(score=2, alt_score=3, alt_note="higher",
                                          inventory={"data": 3, "definitions": 3, "files": 2, "secrets": 3})
        res = result(data)
        self.assertEqual(res["variants"]["high"]["effective"]["ARC-09"], 2)

    def test_rollback_follows_the_change_paths(self):
        data = assessment(3, facts={"definition_change_path": False})
        self.assertEqual(errors(data), [])
        status = controls(data)
        self.assertEqual(status["Definition rollback"], "n/a")
        self.assertEqual(status["Release rollback"], "pass")
        data["scores"]["DEL-11"]["score"] = 2
        self.assertEqual(controls(data)["Release rollback"], "fail")
        self.assertEqual(sal(data)["headline"], 2)

    def test_a_change_path_must_exist(self):
        data = assessment(3, facts={"definition_change_path": False, "code_release_path": False})
        self.assertTrue(any("at least one change path" in e for e in errors(data)))

    def test_agent_safe_actions_need_a_machine_surface(self):
        data = assessment(3, facts={"machine_actions": False})
        self.assertEqual(errors(data), [])
        self.assertEqual(data["scores"]["GOV-09"]["status"], "not_applicable")

    def test_progress_counts_next_level_conditions(self):
        data = assessment(2)
        info = sal(data)["loops"]["request"]
        self.assertEqual(info["level"], 2)
        self.assertGreater(info["next_total"], info["next_met"])
        self.assertEqual(info["next_total"] - info["next_met"], len(info["blockers"]))

    def test_sensitivity_flags_single_criterion_boundaries(self):
        data = assessment(3)
        data["scores"]["ARC-06"] = {"status": "assessed", "score": 1, "grade": "A", "evidence": "x"}
        sens = result(data)["sensitivity"]
        self.assertIn("ARC-06", sens["raise_headline"])
        self.assertIn("ARC-06", sens["lower_headline"])
        self.assertNotIn("GOV-04", sens["lower_headline"])

    def test_inventory_must_list_every_named_surface(self):
        data = assessment(3)
        data["scores"]["ARC-09"]["inventory"] = {"data": 4}
        self.assertIn('ARC-09: inventory must list every surface, using "n/a" where one does not apply '
                      '(missing: definitions, files, secrets, schedules)', errors(data))
        data["scores"]["ARC-09"]["inventory"] = {s: "n/a" for s in MODEL["inventories"]["ARC-09"]}
        self.assertIn("ARC-09: inventory needs at least one surface with a level", errors(data))

    def test_silently_resuming_scheduled_work_fails_the_restore_control(self):
        data = assessment(3)
        data["scores"]["ARC-09"]["inventory"] = {"data": 3, "definitions": 3, "files": 3, "secrets": 3,
                                                 "schedules": 2}
        self.assertIn("ARC-09: score 3 exceeds the lowest inventory level 2", errors(data))
        data["scores"]["ARC-09"]["score"] = 2
        self.assertEqual(controls(data)["Tested backup and restore"], "fail")
        data["scores"]["ARC-09"]["score"] = 3
        data["scores"]["ARC-09"]["inventory"]["schedules"] = "n/a"
        self.assertEqual(errors(data), [])

    def test_progress_ignores_conditions_that_do_not_apply(self):
        on = sal(assessment(2))["loops"]["request"]
        off = sal(assessment(2, facts={"multi_tenant": False, "schema_changes": False,
                                       "code_release_path": False}))["loops"]["request"]
        self.assertEqual(off["next_total"], on["next_total"] - 3)
        self.assertEqual(off["next_total"] - off["next_met"], on["next_total"] - on["next_met"] - 3)


def ai(data, variant="default"):
    return result(data)["variants"][variant]["ai_readiness"]


def set_ai(data, cid, value, **extra):
    entry = {"status": "assessed", "score": value, "grade": "A", "evidence": "src/ai.py", **extra}
    if value >= 3 or extra.get("alt_score", 0) >= 3:
        entry.setdefault("facets", dict(ALL_FACETS))
    data["scores"][cid]["ai"] = entry


class AIReadinessTests(unittest.TestCase):
    """Adversarial tests for the AI Readiness View (spec v0.5, section 8)."""

    def test_sal_and_profile_are_unchanged_by_the_ai_view(self):
        data = assessment(3)
        base = result(data)
        for cid in [c for c in ORDER if CRITERIA[c]["ai_check"]]:
            data["scores"][cid]["score"] = 0
            data["scores"][cid].pop("facets", None)
        for cid in MODEL["ai_view"]["readings"]:
            data["scores"][cid]["ai"] = {"status": "not_evidenced", "searched": "src/"}
        after = result(data)
        strip = lambda sal: {k: v for k, v in sal.items() if k != "ai_driven"}
        for variant in ("default", "high", "available"):
            self.assertEqual(strip(base["variants"][variant]["sal"]), strip(after["variants"][variant]["sal"]))
            self.assertEqual(base["variants"][variant]["capabilities"], after["variants"][variant]["capabilities"])
        self.assertNotEqual(ai(data)["level"], 3)

    def test_high_general_score_without_ai_evidence_adds_nothing(self):
        data = assessment(4)
        data["scores"]["GOV-09"]["ai"] = {"status": "assessed", "score": 0, "grade": "A", "evidence": "scripts only"}
        contributors = ai(data)["dimensions"]["Governance"]["contributors"]
        self.assertEqual(contributors["GOV-09 (AI)"], 0)
        self.assertEqual(data["scores"]["GOV-09"]["score"], 4)

    def test_missing_ai_reading_is_rejected_when_ai_features_is_true(self):
        data = assessment(3)
        del data["scores"]["DEL-01"]["ai"]
        self.assertIn("DEL-01 (AI): an AI-qualified reading is required because ai_features is true", errors(data))

    def test_not_applicable_is_allowed_only_in_the_stated_cases(self):
        data = assessment(3)
        data["scores"]["LRN-05"]["ai"] = {"status": "not_applicable", "rationale": "rules do this"}
        self.assertTrue(any(e.startswith("LRN-05 (AI): may be not_applicable only") for e in errors(data)))
        data = assessment(3, facts={"ai_actions": False})
        self.assertEqual(data["scores"]["GOV-09"]["ai"]["status"], "not_applicable")
        self.assertEqual(errors(data), [])

    def test_not_evidenced_counts_as_zero_and_is_reported(self):
        data = assessment(3)
        data["scores"]["GOV-11"]["ai"] = {"status": "not_evidenced", "searched": "src/ai"}
        out = ai(data)
        self.assertEqual(out["dimensions"]["Governance"]["contributors"]["GOV-11 (AI)"], 0)
        self.assertIn("GOV-11 (AI)", out["not_evidenced"])

    def test_arc08_reading_must_match_the_ai_provider_surface(self):
        data = assessment(3)
        data["scores"]["ARC-08"]["inventory"]["ai_providers"] = 3
        set_ai(data, "ARC-08", 2)
        self.assertIn("ARC-08 (AI): score 2 must equal the ai_providers inventory level 3", errors(data))

    def test_arc08_alternate_and_opt_in_readings_cannot_exceed_the_ai_provider_surface(self):
        data = assessment(3)
        data["scores"]["ARC-08"]["inventory"]["ai_providers"] = 2
        set_ai(data, "ARC-08", 2, alt_score=3, alt_note="breaker", available_score=3)
        errs = errors(data)
        self.assertIn("ARC-08 (AI): alt_score 3 may not exceed the ai_providers inventory level 2", errs)
        self.assertIn("ARC-08 (AI): available_score 3 may not exceed the ai_providers inventory level 2", errs)

    def test_arc08_inventory_caps_every_variant_when_scoring(self):
        data = assessment(3)
        data["scores"]["ARC-08"]["inventory"]["ai_providers"] = 2
        set_ai(data, "ARC-08", 2, alt_score=3, alt_note="breaker", available_score=3)
        for variant in ("default", "high", "available"):
            values, _, flags = score.effective_ai_readings(data, MODEL, variant)
            self.assertEqual(values["ARC-08"], 2, variant)
        self.assertIn("ARC-08 (AI): ai_providers inventory caps 3 -> 2",
                      score.effective_ai_readings(data, MODEL, "high")[2])

    def test_ai_reading_alternates_are_upward_and_opt_in_not_lower(self):
        data = assessment(2)
        set_ai(data, "DEL-04", 2, alt_score=1, alt_note="lower", available_score=1)
        errs = errors(data)
        self.assertTrue(any(e.startswith("DEL-04 (AI): alt_score must be the next level up") for e in errs))
        self.assertIn("DEL-04 (AI): available_score cannot be below score", errs)

    def test_contradictory_ai_facts_are_rejected(self):
        data = assessment(3, facts={"ai_features": False, "ai_data_access": True, "ai_actions": False})
        self.assertIn("scope fact ai_data_access: cannot be true by default while ai_features is not", errors(data))

    def test_prompt_only_product_has_no_context_dimension(self):
        data = assessment(3, facts={"ai_data_access": False})
        self.assertEqual(errors(data), [])
        out = ai(data)
        self.assertIsNone(out["dimensions"]["Context"]["level"])
        self.assertEqual(out["level"], 3)
        self.assertEqual({g["gate"]: g["status"] for g in out["gates"]}["Permission-preserving access"], "n/a")

    def test_no_ai_features_gives_no_headline(self):
        data = assessment(3, facts={"ai_features": False, "ai_data_access": False, "ai_actions": False})
        self.assertEqual(errors(data), [])
        self.assertEqual(ai(data)["status"], "no_ai_features")

    def test_ai_off_by_default_scores_only_the_opt_in_reading(self):
        data = assessment(3, facts={"ai_features": False, "ai_data_access": False, "ai_actions": False})
        for fact in ("ai_features", "ai_data_access", "ai_actions"):
            data["scope_facts"][fact]["available_value"] = True
        for cid in [c for c in ORDER if CRITERIA[c]["ai_check"]]:
            data["scores"][cid] = {"status": "assessed", "score": 3, "grade": "A", "evidence": "x",
                                   "facets": dict(ALL_FACETS)}
        for cid in MODEL["ai_view"]["readings"]:
            if data["scores"][cid]["status"] != "not_applicable":
                set_ai(data, cid, 3)
        self.assertEqual(errors(data), [])
        self.assertEqual(ai(data)["status"], "no_ai_features")
        self.assertEqual(ai(data, "available")["level"], 3)

    def test_one_weak_dimension_sets_the_headline(self):
        data = assessment(4)
        data["scores"]["AIR-02"].update(score=1)
        data["scores"]["AIR-08"].update(score=1)
        out = ai(data)
        self.assertEqual(out["dimensions"]["Context"]["level"], 4)
        self.assertEqual(out["dimensions"]["Operations"]["level"], 2)
        self.assertEqual(out["level"], 2)

    def test_dimension_uses_floor_not_rounding(self):
        data = assessment(3)
        data["scores"]["AIR-05"].update(score=2)
        data["scores"]["AIR-06"].update(score=3)
        self.assertEqual(ai(data)["dimensions"]["Quality"]["level"], 2)

    def test_failed_gate_caps_and_labels(self):
        data = assessment(4)
        data["scores"]["AIR-07"].update(score=2)
        out = ai(data)
        self.assertEqual(out["level"], 2)
        self.assertEqual(out["label"], "not production-governed")
        data = assessment(4, facts={"ai_actions": False})
        out = ai(data)
        self.assertIsNone(out["label"])
        self.assertEqual({g["gate"]: g["status"] for g in out["gates"]}["Traceability of consequential AI actions"],
                         "n/a")

    def test_gate_criteria_need_tested_evidence(self):
        data = assessment(3)
        data["scores"]["AIR-06"]["facets"] = {"implemented": True, "tested": False, "operated": False}
        out = ai(data)
        self.assertEqual(out["level"], 2)
        self.assertEqual({g["gate"]: g["status"] for g in out["gates"]}["Regression evaluation before release"],
                         "fail")

    def test_footprint_never_changes_readiness(self):
        data = assessment(3)
        before = ai(data)["level"]
        for cid in ("MAL-19", "MAL-20", "DEL-01", "DEL-04", "LRN-05", "LRN-06", "LRN-07", "EXP-05"):
            set_ai(data, cid, 0)
        out = ai(data)
        self.assertEqual(out["level"], before)
        self.assertEqual(out["footprint"]["Build"]["level"], 0)

    def test_lrn08_counts_for_governance_only_when_ai_changes_the_product(self):
        data = assessment(3, facts={"agent_mutations": False})
        self.assertNotIn("LRN-08 (AI)", ai(data)["dimensions"]["Governance"]["contributors"])
        data = assessment(3)
        self.assertIn("LRN-08 (AI)", ai(data)["dimensions"]["Governance"]["contributors"])

def driven(data, variant="default"):
    return sal(data, variant)["ai_driven"]


class AIDrivenTests(unittest.TestCase):
    """How far AI itself carries each loop (v0.6)."""

    def test_a_product_with_no_ai_is_driven_by_ai_nowhere(self):
        data = assessment(3, facts={"ai_features": False, "ai_data_access": False, "ai_actions": False})
        self.assertEqual(sal(data)["headline"], 3)
        self.assertEqual(driven(data)["headline"], 0)
        self.assertEqual(driven(data)["headline_name"], "AI drives no stage")
        self.assertTrue(all(v["level"] == 0 for v in driven(data)["loops"].values()))

    def test_ai_level_never_exceeds_the_loop_level(self):
        data = assessment(2)
        for cid in MODEL["ai_view"]["driven"]["request"]:
            set_ai(data, cid, 4)
        self.assertEqual(driven(data)["loops"]["request"]["level"], sal(data)["loops"]["request"]["level"])

    def test_rule_based_diagnosis_does_not_count_as_ai(self):
        data = assessment(3)
        self.assertEqual(driven(data)["loops"]["fix"]["level"], 3)
        set_ai(data, "LRN-05", 0, evidence="rule-based grouping")
        self.assertEqual(sal(data)["loops"]["fix"]["level"], 3)
        self.assertEqual(driven(data)["loops"]["fix"]["level"], 0)
        self.assertTrue(any("LRN-05" in b["needs"] for b in driven(data)["loops"]["fix"]["blockers"]))

    def test_headline_is_the_lower_of_the_request_and_fix_loops(self):
        data = assessment(3)
        set_ai(data, "DEL-01", 2)
        self.assertEqual(driven(data)["loops"]["request"]["level"], 2)
        self.assertEqual(driven(data)["headline"], 2)

    def test_not_evidenced_ai_reading_counts_as_zero(self):
        data = assessment(3)
        data["scores"]["EXP-05"]["ai"] = {"status": "not_evidenced", "searched": "src/"}
        self.assertEqual(driven(data)["loops"]["expansion"]["level"], 0)

    def test_alternate_ai_readings_move_only_the_high_variant(self):
        data = assessment(3)
        set_ai(data, "DEL-01", 2, alt_score=3, alt_note="close to a specification")
        self.assertEqual(driven(data)["loops"]["request"]["level"], 2)
        self.assertEqual(driven(data, "high")["loops"]["request"]["level"], 3)

    def test_headline_text_reports_ai_beside_each_loop(self):
        text = score.headline_text(sal(assessment(3)), MODEL)
        self.assertIn("AI-driven 3", text)
        self.assertIn("Issue → Fix L3 (AI L3)", text)


class ChecklistTests(unittest.TestCase):
    """What done means at a target level: a challenge per loop and the conditions from the rubric."""

    def loops(self, data, target):
        default = result(data)["variants"]["default"]
        return score.checklist(data, CRITERIA, MODEL, default, target)

    def test_every_criterion_has_five_anchored_levels(self):
        for cid, info in CRITERIA.items():
            self.assertEqual(sorted(info["anchors"]), [0, 1, 2, 3, 4], cid)

    def test_every_level_and_loop_has_a_challenge(self):
        for level in range(1, len(MODEL["levels"])):
            for loop in MODEL["loops"]:
                self.assertTrue(MODEL["challenges"][str(level)][loop])

    def test_a_missing_challenge_is_a_model_error(self):
        with self.assertRaises(score.ModelError):
            rubric_with('"expansion": "A new capability launches to a cohort', '"other": "A new capability launches to a cohort')

    def test_items_agree_with_the_scorer_progress_count(self):
        data = assessment(2)
        set_score(data, "GOV-05", 2)
        sal_now = sal(data)
        for loop, info in self.loops(data, 3).items():
            target = [i for i in info["items"] if i["level"] == 3]
            self.assertEqual(sum(i["met"] for i in target), sal_now["loops"][loop]["next_met"])
            self.assertEqual(len(target), sal_now["loops"][loop]["next_total"])

    def test_unmet_items_are_exactly_the_blockers(self):
        data = assessment(2)
        info = self.loops(data, 3)["request"]
        blockers = {b["needs"] for b in sal(data)["loops"]["request"]["blockers"]}
        self.assertEqual({i["needs"] for i in info["items"] if not i["met"]}, blockers)

    def test_unmet_lower_levels_are_listed_and_met_ones_are_not(self):
        data = assessment(2)
        set_score(data, "DEL-01", 1)
        items = self.loops(data, 3)["request"]["items"]
        self.assertTrue(any(i["level"] == 2 and "DEL-01" in i["needs"] for i in items))
        self.assertFalse(any(i["level"] == 2 and i["met"] for i in items))

    def test_description_uses_the_anchor_at_the_required_level(self):
        items = self.loops(assessment(2), 3)["request"]["items"]
        rollback = [i for i in items if i.get("control") == "Definition rollback"][0]
        self.assertIn(CRITERIA["GOV-05"]["anchors"][3], rollback["description"])

    def test_rollback_names_only_change_paths_that_exist(self):
        data = assessment(0, facts={"code_release_path": False})
        item = [i for i in self.loops(data, 1)["request"]["items"] if i["stage"] == "Roll back"][0]
        self.assertIn("GOV-05", item["description"])
        self.assertNotIn("DEL-11", item["description"])

    def test_checklist_command_prints_challenges_and_boxes(self):
        code, out = run(assessment(2), "--checklist", "3")
        self.assertEqual(code, 0)
        self.assertIn("**Challenge.**", out)
        self.assertIn("- [ ]", out)
        self.assertIn("- [x]", out)

    def test_checklist_does_not_change_scores(self):
        data = assessment(2)
        before = sal(data)
        run(data, "--checklist", "4")
        self.assertEqual(sal(data), before)


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
        self.assertIn("**Built to SAL 2 (Assisted) · Proven: not evidenced · AI-driven 2", out)
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


def rate(data, level="high", **low):
    """Record confidence on every assessed criterion; ids given as keywords get that level instead."""
    for cid, entry in data["scores"].items():
        if entry["status"] == "assessed":
            entry["confidence"] = low.get(cid.replace("-", "_"), level)
    return data


class KindsOfChangeTests(unittest.TestCase):
    """Kinds of change (v0.7 section 2)."""

    def test_an_assessment_without_change_kinds_fails(self):
        data = assessment(3)
        del data["change_kinds"]
        self.assertTrue(any(e.startswith("change_kinds: missing") for e in errors(data)))
        data["change_kinds"] = []
        self.assertTrue(any(e.startswith("change_kinds: none listed yet") for e in errors(data)))
        data["change_kinds"] = {"settings": 1}
        self.assertTrue(any(e.startswith("change_kinds must be a list") for e in errors(data)))

    def test_fields_are_validated(self):
        kinds = kinds_at(1)
        kinds[0].update(id="Settings", reach=6, name="", confidence="sure", extra=1)
        kinds[1].update(id="reports", main="yes")
        kinds[2].update(who=" ", evidence="todo")
        errs = errors(assessment(3, kinds=kinds))
        self.assertIn("change kind Settings: id must be lowercase letters, digits and hyphens, got 'Settings'", errs)
        self.assertIn("change kind Settings: reach must be an integer 0..5, got 6", errs)
        self.assertIn("change kind Settings: name must be non-empty text", errs)
        self.assertTrue(any(e.startswith("change kind Settings: confidence must be one of") for e in errs))
        self.assertTrue(any(e.startswith("change kind Settings: unknown field 'extra'") for e in errs))
        self.assertIn("change kind reports: main must be true or false", errs)
        self.assertIn("change kind reports: id is listed more than once", errs)
        self.assertIn("change kind reports: who must be non-empty text", errs)
        self.assertIn("change kind reports: evidence must be non-empty text", errs)

    def test_at_least_one_main_kind_and_at_most_eight(self):
        self.assertIn("change_kinds: at least one kind must be main",
                      errors(assessment(3, kinds=kinds_at(1, main=(False, False)))))
        many = [dict(kinds_at(1)[0], id=f"kind-{i}") for i in range(9)]
        self.assertTrue(any(e.startswith("change_kinds: at most 8 kinds, got 9") for e in errors(assessment(3, kinds=many))))
        self.assertEqual(errors(assessment(3, kinds=many[:8])), [])

    def test_reach_two_needs_a_drafting_product(self):
        data = assessment(1, kinds=kinds_at(2))
        errs = errors(data)
        self.assertIn("change kind settings: reach 2 (Drafted) needs DEL-04 ≥ 2 or (LRN-07 ≥ 2 with LRN-08 ≥ 2) "
                      "for reach 2 or more, but has DEL-04 1, LRN-07 1, LRN-08 1", errs)
        set_score(data, "DEL-04", 2)
        self.assertEqual(errors(data), [])
        data = assessment(1, kinds=kinds_at(2))
        set_score(data, "LRN-07", 2)
        self.assertTrue(errors(data))
        set_score(data, "LRN-08", 2)
        self.assertEqual(errors(data), [])

    def test_reach_three_needs_del04_at_three(self):
        data = assessment(2, kinds=kinds_at(3))
        self.assertTrue(any("reach 3 (Carried) needs DEL-04 ≥ 3" in e for e in errors(data)))
        data["scores"]["DEL-04"].update(score=3)
        self.assertEqual(errors(data), [])

    def test_reach_four_needs_gov07_at_three(self):
        data = assessment(3, kinds=kinds_at(4))
        set_score(data, "GOV-07", 2)
        self.assertTrue(any("reach 4 (Pre-approved) needs GOV-07 ≥ 3" in e for e in errors(data)))
        set_score(data, "GOV-07", 3)
        self.assertEqual(errors(data), [])

    def test_reach_five_needs_lrn07_at_three(self):
        data = assessment(3, kinds=kinds_at(5))
        set_score(data, "LRN-07", 2)
        self.assertTrue(any("reach 5 (Self-chosen) needs LRN-07 ≥ 3" in e for e in errors(data)))
        set_score(data, "LRN-07", 3)
        self.assertEqual(errors(data), [])

    def test_consistency_uses_default_effective_scores(self):
        data = assessment(3, kinds=kinds_at(3))
        data["scores"]["DEL-04"]["grade"] = "C"  # grade C caps the default score at 2
        self.assertTrue(any("needs DEL-04 ≥ 3" in e and "has DEL-04 2" in e for e in errors(data)))
        data = assessment(3, kinds=kinds_at(3))
        data["scores"]["DEL-04"].update(score=2, alt_score=3, alt_note="higher")  # the alternate does not count
        self.assertTrue(any("needs DEL-04 ≥ 3" in e for e in errors(data)))

    def test_self_serve_main_kinds_reach_level_one_whatever_mal(self):
        data = assessment(0, kinds=kinds_at(1))
        for cid in ("GOV-05", "DEL-11"):
            set_score(data, cid, 2)
        self.assertEqual(errors(data), [])
        self.assertEqual(result(data)["variants"]["default"]["capabilities"]["MAL"], 0)
        self.assertEqual(sal(data)["loops"]["request"]["level"], 1)
        data = assessment(4, kinds=kinds_at(1))
        for cid in [c for c in ORDER if c.startswith("MAL-")]:
            set_score(data, cid, 0)
            data["scores"][cid].pop("facets", None)
        self.assertEqual(errors(data), [])
        self.assertEqual(sal(data)["headline"], 5)

    def test_one_main_kind_engineers_only_fails_level_one(self):
        kinds = kinds_at(1)
        kinds[1]["reach"] = 0
        data = assessment(0, kinds=kinds)
        for cid in [c for c in ORDER if c.startswith("MAL-")] + ["GOV-05", "DEL-11"]:
            set_score(data, cid, 4 if cid.startswith("MAL-") else 2)
            if cid in MODEL["depth_capped"] or cid in MODEL["inventories"]:
                data["scores"][cid]["score"] = 2
        self.assertEqual(errors(data), [])
        request = sal(data)["loops"]["request"]
        self.assertEqual(request["level"], 0)
        build = [b for b in request["blockers"] if b["stage"] == "Build"][0]
        self.assertIn("kinds 1 of 2 main self-serve", build["observed"])
        self.assertEqual(result(data)["kinds"]["value"], 1)

    def test_a_kind_that_is_not_main_does_not_hold_level_one(self):
        kinds = kinds_at(1)
        kinds[2]["reach"] = 0
        data = assessment(0, kinds=kinds)
        for cid in ("GOV-05", "DEL-11"):
            set_score(data, cid, 2)
        self.assertEqual(sal(data)["loops"]["request"]["level"], 1)
        self.assertEqual(result(data)["kinds"]["text"], "2 of 2 main kinds are self-serve")

    def test_kinds_path_values(self):
        self.assertEqual(score.kinds_summary({"change_kinds": kinds_at(0)})["value"], 0)
        mixed = kinds_at(0)
        mixed[2]["reach"] = 2
        self.assertEqual(score.kinds_summary({"change_kinds": mixed})["value"], 1)
        self.assertEqual(score.kinds_summary({"change_kinds": kinds_at(1)})["value"], 2)

    def test_expansion_keeps_exp02_as_its_people_path(self):
        self.assertEqual(MODEL["build_paths"]["expansion"]["people"], [{"c": "EXP-02"}])
        for loop in ("request", "fix"):
            self.assertEqual(MODEL["build_paths"][loop]["people"], [{"kinds": "main"}])

    def test_checklist_describes_kinds_in_plain_words(self):
        kinds = kinds_at(1)
        kinds[0]["reach"] = 0
        default = result(assessment(2, kinds=kinds))["variants"]["default"]
        items = score.checklist(assessment(2, kinds=kinds), CRITERIA, MODEL, default, 1)["request"]["items"]
        build = [i for i in items if i["stage"] == "Build"][0]
        self.assertIn("Every main kind of change can be made by the people running the product, and undone.",
                      build["description"])
        self.assertIn("Not yet: Change the settings.", build["description"])

    def test_report_has_a_kinds_table(self):
        code, out = run(assessment(3))
        self.assertEqual(code, 0)
        self.assertIn("### Kinds of change", out)
        self.assertIn("2 of 2 main kinds are self-serve", out)
        self.assertIn("| Change the settings (`settings`) | admins | yes | 1 Self-serve | docs/settings.md |", out)


class BasisAndProvenTests(unittest.TestCase):
    """Designed, Built, Proven (v0.7 section 3)."""

    def test_grade_d_only_in_a_design_assessment(self):
        data = assessment(3)
        data["scores"]["MAL-01"]["grade"] = "D"
        self.assertIn("MAL-01: grade D (a design document) is only allowed when basis is design", errors(data))
        data["basis"] = "design"
        self.assertEqual(errors(data), [])
        data["basis"] = "planned"
        self.assertIn("basis must be one of shipped, design, got 'planned'", errors(data))

    def test_design_needs_no_facets_and_has_no_depth_cap(self):
        data = assessment(4)
        for entry in data["scores"].values():
            entry.pop("facets", None)
            if isinstance(entry.get("ai"), dict):
                entry["ai"].pop("facets", None)
        self.assertIn("ARC-03: depth-capped criterion read at 3 or more needs facets", errors(data))
        data["basis"] = "design"
        self.assertEqual(errors(data), [])
        self.assertEqual(result(data)["variants"]["default"]["effective"]["ARC-03"], 4)
        del data["scores"]["ARC-09"]["inventory"]
        self.assertIn("ARC-09: inventory criterion read at 3 or more needs an inventory", errors(data))

    def test_design_headline_and_report(self):
        data = assessment(3)
        data["basis"] = "design"
        res = result(data)
        text = score.result_headline(res, MODEL)
        self.assertTrue(text.startswith("Designed for SAL 3 (Supervised) · AI-driven 3 · "), text)
        self.assertNotIn("Proven", text)
        self.assertIsNone(res["proven"])
        code, out = run(data)
        self.assertEqual(code, 0)
        self.assertIn("not comparable with a shipped", out)
        code, out = run(data, "--quiet")
        self.assertTrue(out.startswith("Designed for SAL 3"))

    def test_proven_is_not_allowed_in_a_design_assessment(self):
        data = assessment(3)
        data["basis"] = "design"
        data["proven"] = {"request": {"level": 1, "evidence": "changelog"}}
        self.assertIn("proven: not allowed when basis is design; a design reading has no operating records",
                      errors(data))

    def test_proven_above_the_built_level_is_an_error(self):
        data = assessment(3)
        data["proven"] = {"request": {"level": 4, "evidence": "release records"}}
        self.assertIn("proven request: level 4 is above the built level L3; a loop cannot be proven above what "
                      "it is built to do", errors(data))
        data["proven"]["request"]["level"] = 3
        self.assertEqual(errors(data), [])

    def test_proven_shape(self):
        data = assessment(3)
        data["proven"] = {"request": {"level": "2", "evidence": ""},
                          "fix": {"status": "not_evidenced", "searched": ""},
                          "expansion": {"status": "todo"}, "other": {}}
        errs = errors(data)
        self.assertIn("proven request: level must be an integer 0..5, got '2'", errs)
        self.assertIn("proven request: a proven level needs evidence from operating records", errs)
        self.assertIn("proven fix: not_evidenced needs the searched scope", errs)
        self.assertTrue(any(e.startswith("proven expansion: not yet assessed") for e in errs))
        self.assertTrue(any(e.startswith("proven other: not a loop") for e in errs))

    def test_proven_headline_is_the_lower_of_request_and_fix(self):
        data = assessment(3)
        self.assertEqual(result(data)["proven"]["text"], "Proven: not evidenced")
        data["proven"] = {"request": {"level": 2, "evidence": "changelog"},
                          "fix": {"status": "not_evidenced", "searched": "issue tracker"}}
        self.assertEqual(result(data)["proven"]["text"], "Proven: not evidenced")
        data["proven"]["fix"] = {"level": 1, "evidence": "incident records"}
        proven = result(data)["proven"]
        self.assertEqual(proven["headline"], 1)
        self.assertEqual(proven["text"], "Proven: SAL 1 (Configurable)")
        self.assertEqual(proven["loops"]["expansion"]["status"], "not_recorded")
        self.assertTrue(score.result_headline(result(data), MODEL).startswith(
            "Built to SAL 3 (Supervised) · Proven: SAL 1 (Configurable) · AI-driven 3 · Request → Release L3 (AI L3)"))

    def test_proven_never_changes_the_built_level(self):
        data = assessment(3)
        before = sal(data)
        data["proven"] = {"request": {"level": 0, "evidence": "x"}, "fix": {"level": 0, "evidence": "y"}}
        self.assertEqual(sal(data), before)

    def test_no_level_condition_requires_operated(self):
        def walk(cond):
            yield cond
            for key in ("any", "all"):
                for sub in cond.get(key, []):
                    yield from walk(sub)
        for conds in MODEL["conditions"].values():
            for cond in conds:
                self.assertFalse(any("operated" in c for c in walk(cond)), cond)
        with self.assertRaises(score.ModelError):
            rubric_with('{"part": "governance", "stage": "Ceiling", "c": "GOV-10", "min": 4}',
                        '{"part": "governance", "stage": "Ceiling", "c": "GOV-10", "min": 4, "operated": true}')

    def test_level_five_without_any_operated_facet(self):
        data = assessment(4)
        for entry in data["scores"].values():
            for item in (entry, entry.get("ai")):
                if isinstance(item, dict) and "facets" in item:
                    item["facets"]["operated"] = False
        self.assertEqual(errors(data), [])
        self.assertEqual(sal(data)["headline"], 5)
        self.assertEqual(result(data)["flags"], [])


class RecursionTests(unittest.TestCase):
    """LRN-10 and the Recursion line (v0.7 section 4)."""

    def level_four(self):
        data = assessment(3)
        set_score(data, "GOV-05", 4)
        set_score(data, "DEL-11", 4)
        return data

    def test_lrn10_is_required_at_level_four(self):
        data = self.level_four()
        set_score(data, "LRN-10", 2)
        self.assertEqual(sal(data)["headline"], 4)
        set_score(data, "LRN-10", 1)
        out = sal(data)
        self.assertEqual(out["headline"], 3)
        self.assertTrue(any(b["needs"] == "LRN-10 ≥ 2" and b["part"] == "spine" and b["stage"] == "Observe"
                            for b in out["loops"]["request"]["blockers"]))

    def test_lrn10_is_required_at_level_five(self):
        data = assessment(4)
        set_score(data, "LRN-10", 3)
        out = sal(data)
        self.assertEqual(out["headline"], 4)
        self.assertTrue(any(b["needs"] == "LRN-10 ≥ 4" for b in out["loops"]["fix"]["blockers"]))

    def test_recursion_line_follows_the_score(self):
        names = ["Fixed", "By hand", "Governed", "Results-driven", "Self-improving"]
        self.assertEqual(MODEL["recursion"], names)
        for value, name in enumerate(names):
            data = assessment(2)
            data["scores"]["LRN-10"] = {"status": "assessed", "score": value, "grade": "A", "evidence": "x"}
            reading = result(data)["recursion"]
            self.assertEqual((reading["score"], reading["name"]), (value, name))
            self.assertEqual(reading["text"], f"Recursion: {value} {name} (LRN-10 at {value})")
        data = assessment(2, LRN_10={"status": "not_evidenced", "searched": "src/"})
        self.assertEqual(result(data)["recursion"]["name"], "Fixed")
        code, out = run(data)
        self.assertIn("**Recursion: 0 Fixed (LRN-10 not evidenced, counted as 0).**", out)

    def test_lrn10_sits_under_measure(self):
        self.assertEqual(CRITERIA["LRN-10"]["area"], "Measure")
        self.assertEqual(MODEL["areas"]["LRN"]["Measure"], ["LRN-09", "LRN-10"])


class AIDeliveryTests(unittest.TestCase):
    """The AI delivery record (v0.7 section 5)."""

    def test_record_never_changes_a_score(self):
        data = assessment(2)
        before = result(data)
        for present, qualifies in ((True, True), (True, False), (False, False)):
            data["ai_delivery"] = {"present": present, "qualifies": qualifies, "evidence": "AGENTS.md"}
            self.assertEqual(errors(data), [])
            after = result(data)
            self.assertEqual(after["variants"], before["variants"])
            self.assertEqual(after["sensitivity"], before["sensitivity"])
            self.assertEqual(after["proven"], before["proven"])

    def test_record_shape(self):
        data = assessment(2)
        data["ai_delivery"] = {"present": False, "qualifies": True, "evidence": "", "note": 3, "extra": 1}
        errs = errors(data)
        self.assertIn("ai_delivery: qualifies can be true only when present is true", errs)
        self.assertIn("ai_delivery: needs evidence (what was found, or what was searched)", errs)
        self.assertIn("ai_delivery: note must be text", errs)
        self.assertTrue(any(e.startswith("ai_delivery: unknown field 'extra'") for e in errs))
        data["ai_delivery"] = {"present": None, "qualifies": None, "evidence": "x"}
        self.assertIn("ai_delivery: present must be true or false, got None", errors(data))

    def test_report_says_whether_it_counts(self):
        data = assessment(2)
        data["ai_delivery"] = {"present": True, "qualifies": False, "evidence": "AGENTS.md"}
        code, out = run(data)
        self.assertIn("not the product evolving itself, and it does not meet scoring rule 12", out)


class ConfidenceTests(unittest.TestCase):
    """Confidence on every score (v0.7 section 6)."""

    def test_confidence_is_all_or_nothing(self):
        data = assessment(2)
        self.assertEqual(errors(data), [])
        data["scores"]["MAL-01"]["confidence"] = "high"
        errs = errors(data)
        self.assertTrue(any(e.startswith("confidence is all or nothing: 1 assessed criteria record it") for e in errs))
        self.assertEqual(errors(rate(assessment(2))), [])

    def test_values_and_statuses(self):
        data = rate(assessment(2), MAL_01="certain")
        data["scores"]["MAL-02"] = {"status": "not_evidenced", "searched": "src/", "confidence": "low"}
        data["scores"]["DEL-01"]["ai"]["confidence"] = "unsure"
        errs = errors(data)
        self.assertIn("MAL-01: confidence must be one of high, medium, low, got 'certain'", errs)
        self.assertIn("MAL-02: confidence is only allowed when status is assessed", errs)
        self.assertIn("DEL-01 (AI): confidence must be one of high, medium, low, got 'unsure'", errs)

    def test_confidence_never_changes_a_score(self):
        data = assessment(2)
        before = result(data)["variants"]
        self.assertEqual(result(rate(data, "low"))["variants"], before)

    def test_counts_and_check_these_first(self):
        data = rate(assessment(2), GOV_05="low", MAL_01="low", DEL_05="medium")
        data["change_kinds"][0]["confidence"] = "low"
        conf = result(data)["confidence"]
        self.assertTrue(conf["recorded"])
        assessed = result(data)["coverage"]["assessed"]
        self.assertEqual(conf["criteria"], {"high": assessed - 3, "medium": 1, "low": 2, "none": 0})
        self.assertEqual(conf["change_kinds"], {"high": 0, "medium": 0, "low": 1, "none": 2})
        check = {i["id"]: i["holds"] for i in conf["check_first"]}
        self.assertEqual(list(check), ["GOV-05"])
        self.assertIn("Definition rollback control", check["GOV-05"])
        self.assertIn("Request → Release to L3", check["GOV-05"])
        code, out = run(data)
        self.assertIn("Check these first", out)
        self.assertIn("GOV-05 (", out)

    def test_not_recorded(self):
        conf = result(assessment(2))["confidence"]
        self.assertFalse(conf["recorded"])
        self.assertEqual(conf["check_first"], [])


class V07OutputTests(unittest.TestCase):
    def test_json_payload_carries_the_new_readings(self):
        data = rate(assessment(3))
        data["ai_delivery"] = {"present": True, "qualifies": False, "evidence": "AGENTS.md"}
        code, out = run(data, "--json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        for key in ("basis", "headline_text", "change_kinds", "kinds_summary", "proven", "recursion",
                    "ai_delivery", "confidence"):
            self.assertIn(key, payload)
        self.assertEqual(payload["basis"], "shipped")
        self.assertEqual(payload["change_kinds"][0]["reach_name"], "Self-serve")
        self.assertEqual(payload["kinds_summary"]["value"], 2)
        self.assertEqual(payload["recursion"]["name"], "Results-driven")
        self.assertFalse(payload["ai_delivery"]["qualifies"])
        self.assertEqual(payload["criteria_in_rubric"], 75)

    def test_markdown_shows_proven_and_quiet_and_checklist_still_work(self):
        code, out = run(assessment(3))
        self.assertIn("### Proven", out)
        self.assertIn("From a repository alone, proven is usually not evidenced.", out)
        code, out = run(assessment(3), "--quiet")
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("Built to SAL 3 (Supervised) · Proven: not evidenced · AI-driven 3"))
        code, out = run(assessment(2), "--checklist", "3")
        self.assertIn("Today: Built to SAL 2", out)
        code, out = run(assessment(2), "--prescribe")
        self.assertEqual(code, 0)
        self.assertIn("Current: Built to SAL 2", out)

    def test_init_template_parts_are_rejected_until_filled(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            init_scores.main(["--product", "P", "--archetype", "other", "--source", "x"])
        template = json.loads(out.getvalue())
        self.assertEqual(template["basis"], "shipped")
        errs = errors(template)
        self.assertTrue(any(e.startswith("change_kinds: none listed yet") for e in errs))
        self.assertTrue(any(e.startswith("proven request: not yet assessed") for e in errs))
        self.assertIn("ai_delivery: present must be true or false, got None", errs)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            init_scores.main(["--product", "P", "--archetype", "other", "--source", "x", "--basis", "design"])
        template = json.loads(out.getvalue())
        self.assertEqual(template["basis"], "design")
        self.assertNotIn("proven", template)


if __name__ == "__main__":
    unittest.main()
