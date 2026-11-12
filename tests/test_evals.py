"""Tests for evals/agreement.py, evals/run.py and the evaluation cases.

Run with: python3 -m unittest tests.test_evals -v
"""

import contextlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVALS = os.path.join(ROOT, "evals")
SKILL = os.path.join(ROOT, "skills", "evolvable-software")
RUBRIC = os.path.join(SKILL, "references", "rubric.md")
SCORER = os.path.join(SKILL, "scripts", "score.py")
CASES = os.path.join(EVALS, "cases")
SECOND = os.path.join(ROOT, "assessments", "2026-09-field-test", "second-rating")
sys.path.insert(0, EVALS)
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import agreement  # noqa: E402
import run  # noqa: E402
import score  # noqa: E402

CRITERIA, ORDER, MODEL = score.load_rubric(RUBRIC)
CASE_NAMES = sorted(n for n in os.listdir(CASES) if os.path.isdir(os.path.join(CASES, n)))


def rubric_ids():
    with open(RUBRIC, encoding="utf-8") as handle:
        return set(re.findall(r"^### ([A-Z]{3}-\d{2}) ", handle.read(), re.M)) | {"LRN-10"}


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def entry(value):
    """A short score entry: an int, 'na', 'ne', or (score, alt)."""
    if value == "na":
        return {"status": "not_applicable", "rationale": "fact is false"}
    if value == "ne":
        return {"status": "not_evidenced", "searched": "src/"}
    if isinstance(value, tuple):
        return {"status": "assessed", "score": value[0], "alt_score": value[1], "alt_note": "x", "evidence": "e"}
    return {"status": "assessed", "score": value, "evidence": "e"}


def assessment(scores, facts=None, kinds=None, ai=None, product="Example"):
    data = {"product": product, "scores": {cid: entry(v) for cid, v in scores.items()},
            "scope_facts": {f: {"value": v, "evidence": "e"} for f, v in (facts or {}).items()}}
    for cid, value in (ai or {}).items():
        data["scores"][cid]["ai"] = entry(value)
    if kinds is not None:
        data["change_kinds"] = [{"id": i, "name": n, "who": "admins", "main": m, "reach": r, "evidence": "e"}
                                for i, n, m, r in kinds]
    return data


def reference(case_dir, pick=min):
    """A complete assessment of a case that reads every expectation at one end of its range."""
    exp = load(os.path.join(case_dir, "expected.json"))
    facts = {f: False for f in MODEL["scope_facts"]}
    facts.update({f: s["value"] for f, s in exp["scope_facts"].items()})
    archetype = exp["archetype"]["allowed"][0]
    excluded = MODEL["archetype_exclusions"][archetype]
    scores = {}
    for cid in ORDER:
        spec = exp["criteria"].get(cid, {})
        gate = MODEL["applies_when"].get(cid, [])
        gate = [gate] if isinstance(gate, str) else gate
        if cid in excluded or (gate and not any(facts[g] for g in gate)) or spec.get("status") == "not_applicable":
            scores[cid] = {"status": "not_applicable", "rationale": "archetype or scope fact"}
        else:
            value = pick(spec["range"]) if "range" in spec else 0
            scores[cid] = {"status": "assessed", "score": value, "grade": "A", "evidence": "reference reading"}
    view = MODEL["ai_view"]
    if facts["ai_features"]:
        for cid in view["readings"]:
            spec = exp.get("ai_readings", {}).get(cid, {})
            gate = view.get("reading_applies_when", {}).get(cid)
            if scores[cid]["status"] == "not_applicable" or (gate and not facts[gate]):
                scores[cid]["ai"] = {"status": "not_applicable", "rationale": "parent or scope fact"}
            else:
                scores[cid]["ai"] = {"status": "assessed", "score": pick(spec["range"]) if spec else 0,
                                     "grade": "A", "evidence": "reference reading"}
    kinds = [{"id": re.sub(r"[^a-z0-9]+", "-", k["label"]).strip("-"), "name": k["label"], "who": "operators",
              "main": k.get("main", True), "reach": pick(k["reach"]), "evidence": ", ".join(k["files"])}
             for k in exp["change_kinds"]["kinds"]]
    return {"product": exp["case"], "date": "2026-11-12", "source": "evals/cases/" + exp["case"],
            "archetype": archetype, "change_kinds": kinds, "scores": scores,
            "scope_facts": {f: {"value": v, "evidence": "reference reading"} for f, v in facts.items()}}


class Temp(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir)

    def write(self, name, data):
        path = os.path.join(self.dir, name)
        with open(path, "w", encoding="utf-8") as handle:
            if isinstance(data, str):
                handle.write(data)
            else:
                json.dump(data, handle)
        return path

    def compare(self, *docs, **kwargs):
        paths = [self.write(f"r{i}.json", d) for i, d in enumerate(docs)]
        return agreement.compare(paths, **kwargs)


class AgreementTest(Temp):
    def test_exact_within_one_and_mean_difference(self):
        a = assessment({"ARC-02": 2, "ARC-09": 1, "GOV-05": 2, "GOV-04": 3})
        b = assessment({"ARC-02": 2, "ARC-09": 2, "GOV-05": 0, "GOV-04": 3})
        s = self.compare(a, b)["pairs"][0]["scores"]["overall"]
        self.assertEqual((s["both_assessed"], s["exact"], s["within_one"]), (4, 2, 3))
        self.assertEqual(s["mean_abs_diff"], 0.75)
        self.assertEqual(s["differ"], ["ARC-09", "GOV-05"])

    def test_alternates_make_ranges_overlap(self):
        s = self.compare(assessment({"ARC-09": (2, 3)}), assessment({"ARC-09": 3}))["pairs"][0]["scores"]["overall"]
        self.assertEqual((s["exact"], s["ranges_overlap"]), (0, 1))

    def test_status_mismatches_are_counted_not_scored(self):
        a = assessment({"DEL-11": "na", "ARC-05": "ne", "GOV-10": "na", "LRN-08": "ne", "GOV-05": 2})
        b = assessment({"DEL-11": 2, "ARC-05": 1, "GOV-10": "na", "LRN-08": "na", "GOV-05": 2})
        s = self.compare(a, b)["pairs"][0]["scores"]["overall"]
        self.assertEqual(s["not_applicable_vs_assessed"], ["DEL-11"])
        self.assertEqual(s["not_evidenced_vs_assessed"], ["ARC-05"])
        self.assertEqual(s["not_applicable_vs_not_evidenced"], ["LRN-08"])
        self.assertEqual((s["both_assessed"], s["both_not_applicable"]), (1, 1))

    def test_per_capability(self):
        a = assessment({"ARC-02": 2, "ARC-09": 2, "GOV-05": 1})
        b = assessment({"ARC-02": 2, "ARC-09": 3, "GOV-05": 1})
        caps = self.compare(a, b)["pairs"][0]["scores"]["by_capability"]
        self.assertEqual(list(caps), ["ARC", "GOV"])
        self.assertEqual((caps["ARC"]["exact"], caps["GOV"]["exact"]), (1, 1))

    def test_three_raters(self):
        a = assessment({"ARC-02": 2, "ARC-09": 1, "GOV-05": 2, "LRN-08": 2, "DEL-11": "na"})
        b = assessment({"ARC-02": 2, "ARC-09": 2, "GOV-05": 2, "LRN-08": 1, "DEL-11": 2})
        c = assessment({"ARC-02": 2, "ARC-09": 0, "GOV-05": 2, "LRN-08": 0, "DEL-11": "na"})
        result = self.compare(a, b, c)
        self.assertEqual(len(result["pairs"]), 3)
        g = result["all_raters"]["scores"]["overall"]
        self.assertEqual((g["all_assessed"], g["all_same"], g["all_within_one"]), (4, 2, 2))
        self.assertEqual(g["status_differs"], ["DEL-11"])
        critical = {c["id"]: c for c in result["critical"]}
        self.assertTrue(critical["ARC-09"]["disagree"])
        self.assertFalse(critical["GOV-05"]["disagree"])
        self.assertEqual(critical["DEL-11"]["readings"], {"r0": "n/a", "r1": "2", "r2": "n/a"})

    def test_criteria_filter(self):
        a = assessment({"ARC-02": 2, "ARC-09": 1, "MAL-06": 1})
        b = assessment({"ARC-02": 1, "ARC-09": 1, "MAL-06": 2})
        result = self.compare(a, b, criteria=["MAL-06", "ARC-09", "XXX-01"])
        s = result["pairs"][0]["scores"]["overall"]
        self.assertEqual((s["both_assessed"], s["exact"]), (2, 1))
        self.assertEqual(result["criteria_filter"], ["ARC-09", "MAL-06", "XXX-01"])
        self.assertTrue(any("XXX-01" in w for w in result["warnings"]))

    def test_abbreviated_and_pre_v07_files(self):
        full = assessment({"ARC-02": 2, "ARC-09": 1, "GOV-05": 2},
                          facts={"multi_tenant": True, "code_release_path": False},
                          kinds=[("answers", "Answers", True, 1)])
        short = assessment({"GOV-05": 2}, facts={"multi_tenant": False})
        result = self.compare(full, short)
        pair = result["pairs"][0]
        self.assertEqual(pair["scores"]["overall"]["not_in_both_files"], 2)
        self.assertEqual(pair["scores"]["overall"]["exact"], 1)
        self.assertEqual(pair["scope_facts"], {"compared": 1, "differ": ["multi_tenant"]})
        self.assertFalse(pair["change_kinds"]["compared"])
        self.assertIn("pre-v0.7", pair["change_kinds"]["note"])
        self.assertEqual(result["raters"][1]["v07_fields"], [])
        self.assertIn("Kinds of change", agreement.render(result))

    def test_kinds_of_change_by_id_name_and_words(self):
        a = assessment({}, kinds=[("answers", "What the assistant tells customers", True, 1),
                                  ("routing", "Routing rules for questions", True, 2),
                                  ("hours", "Opening hours", False, 0)])
        b = assessment({}, kinds=[("answers", "Answers", True, 1),
                                  ("rules", "Routing rules", True, 1),
                                  ("queues", "New queues", True, 0)])
        k = self.compare(a, b)["pairs"][0]["change_kinds"]
        self.assertEqual([(m["a"], m["b"], m["how"]) for m in k["matched"]],
                         [("answers", "answers", "id"), ("routing", "rules", "words")])
        self.assertEqual((k["main_a"], k["main_b"], k["reach_exact"], k["reach_within_one"]), (2, 3, 1, 2))
        self.assertEqual((k["only_a"], k["only_b"]), (["hours"], ["queues"]))

    def test_ai_readings_compared_like_scores(self):
        a = assessment({"DEL-04": 2, "LRN-05": 2}, ai={"DEL-04": 2, "LRN-05": 2})
        b = assessment({"DEL-04": 2, "LRN-05": 2}, ai={"DEL-04": 2, "LRN-05": 0})
        result = self.compare(a, b)
        s = result["pairs"][0]["ai"]["overall"]
        self.assertEqual((s["both_assessed"], s["exact"], s["within_one"]), (2, 1, 1))
        self.assertEqual([d["id"] for d in result["ai_differences"]], ["LRN-05"])
        self.assertEqual(result["differences"], [])

    def test_product_and_commit_warnings(self):
        a, b = assessment({"GOV-05": 2}, product="n8n"), assessment({"GOV-05": 2}, product="Dify")
        a["commit"], b["source"] = "c17c48043eb1080e5ae9795ea3a384960f8748f1", "github.com/x @ c17c480 (main)"
        warnings = self.compare(a, b)["warnings"]
        self.assertTrue(any("different products" in w for w in warnings))
        self.assertFalse(any("commits" in w for w in warnings))

    def test_cli_markdown_json_and_bad_input(self):
        a = self.write("a.json", assessment({"GOV-05": 2, "ARC-09": 1}))
        b = self.write("b.json", assessment({"GOV-05": 2, "ARC-09": 2}))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(agreement.main([a, b]), 0)
        self.assertIn("| a · b | 2 | 1 of 2 (50%) |", out.getvalue())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(agreement.main([a, b, "--json", "--criteria", "gov-05"]), 0)
        self.assertEqual(json.loads(out.getvalue())["criteria_compared"], 1)
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(agreement.main([a, self.write("bad.json", "{not json")]), 2)

    def test_reproduces_the_second_rating_study(self):
        """Second and third raters, summed over n8n, OpenClaw and Dify: 12 of 19 exact (README)."""
        exact = both = 0
        for product in ("n8n", "openclaw", "dify"):
            result = agreement.compare([os.path.join(SECOND, f"{product}.json"),
                                        os.path.join(SECOND, f"chatgpt-{product}.json")])
            s = result["pairs"][0]["scores"]["overall"]
            exact, both = exact + s["exact"], both + s["both_assessed"]
        self.assertEqual((exact, both), (12, 19))


FAKE_SCORER = """import json, sys
print(json.dumps({"sal": {"loops": {"request": {"level": %d}, "fix": {"level": %d}, "expansion": {"level": %d}}}}))
"""
FAILING_SCORER = "print('VALIDATION FAILED')\nprint(' - change_kinds: missing')\nraise SystemExit(2)\n"


class RunTest(Temp):
    def make_case(self):
        case = os.path.join(self.dir, "case")
        os.makedirs(os.path.join(case, "repo"))
        expected = {
            "case": "tiny", "archetype": {"allowed": ["focused-application"], "reason": "r", "files": ["a.py"]},
            "scope_facts": {"multi_tenant": {"value": False, "reason": "r", "files": ["a.py"]}},
            "criteria": {"GOV-05": {"range": [2, 2], "reason": "r", "files": ["a.py"]},
                         "ARC-09": {"range": [0, 1], "reason": "r", "files": ["a.py"], "trap": True},
                         "ARC-05": {"status": "not_applicable", "reason": "r", "files": ["a.py"]}},
            "ai_readings": {"LRN-05": {"range": [0, 0], "reason": "r", "files": ["a.py"], "trap": True}},
            "change_kinds": {"main_count": {"range": [1, 1], "reason": "r", "files": ["a.py"]},
                             "kinds": [{"label": "rules", "keywords": ["rule"], "reach": [1, 1], "main": True,
                                        "reason": "r", "files": ["a.py"]}]},
            "loops": {"request": {"range": [1, 1], "reason": "r", "files": ["a.py"]}}}
        with open(os.path.join(case, "expected.json"), "w", encoding="utf-8") as handle:
            json.dump(expected, handle)
        return case

    def good(self):
        data = assessment({"GOV-05": 2, "ARC-09": 1, "ARC-05": "na", "LRN-05": 2}, facts={"multi_tenant": False},
                          kinds=[("rules", "Routing rules", True, 1), ("hours", "Opening hours", False, 0)],
                          ai={"LRN-05": 0})
        data["archetype"] = "focused-application"
        return data

    def test_an_assessment_that_meets_every_expectation(self):
        case = self.make_case()
        path = self.write("good.json", self.good())
        result = run.evaluate(case, path, scorer=self.write("fake.py", FAKE_SCORER % (1, 1, 0)))
        self.assertEqual((result["met"], result["counted"], result["unavailable"]), (10, 10, 0))
        self.assertEqual((result["traps_met"], result["traps"]), (2, 2))
        gov05 = [i for i in result["items"] if i["id"] == "GOV-05"][0]
        self.assertEqual((gov05["observed"], gov05["evidence"]), ("2", "e"))
        self.assertEqual([i["observed"] for i in result["items"] if i["section"] == "loops"], ["L1"])

    def test_an_assessment_that_misses(self):
        case = self.make_case()
        data = self.good()
        data["scores"]["ARC-09"] = entry(2)          # the trap: an untested backup scored 2
        data["scores"]["ARC-05"] = entry(2)          # assessed where it should be not applicable
        data["scores"]["LRN-05"]["ai"] = entry(2)    # rule-based grouping credited to AI
        data["change_kinds"][0]["reach"] = 2
        data["archetype"] = "configurable-application-platform"
        path = self.write("bad.json", data)
        result = run.evaluate(case, path, scorer=self.write("fake.py", FAKE_SCORER % (2, 1, 0)))
        missed = sorted(i["id"] for i in result["items"] if i["met"] is False)
        self.assertEqual(missed, ["ARC-05", "ARC-09", "LRN-05", "Request → Release", "archetype", "rules: reach"])
        self.assertEqual((result["traps_met"], result["traps"]), (0, 2))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = run.main([case, path, "--scorer", self.write("fake2.py", FAKE_SCORER % (2, 1, 0))])
        self.assertEqual(code, 1)
        self.assertIn("| MISSED | ARC-09 (trap) | 0 to 1 | 2 |", out.getvalue())
        self.assertIn("Verdict: FAIL", out.getvalue())

    def test_levels_unavailable_when_the_assessment_does_not_validate(self):
        case = self.make_case()
        path = self.write("good.json", self.good())
        result = run.evaluate(case, path, scorer=self.write("fail.py", FAILING_SCORER))
        loop = [i for i in result["items"] if i["section"] == "loops"][0]
        self.assertIsNone(loop["met"])
        self.assertEqual((result["counted"], result["unavailable"]), (9, 1))
        self.assertIn("change_kinds: missing", result["levels_unavailable_because"])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(run.main([case, path, "--json", "--no-levels"]), 0)
        self.assertTrue(json.loads(out.getvalue())["passed"])

    def test_missing_v07_fields_are_misses_not_crashes(self):
        case = self.make_case()
        data = self.good()
        del data["change_kinds"]
        result = run.evaluate(case, self.write("old.json", data), levels=False)
        kinds = [i for i in result["items"] if i["section"] == "kinds"]
        self.assertTrue(kinds and all(i["met"] is False for i in kinds))
        self.assertEqual(kinds[0]["observed"], "change_kinds not recorded")


class CasesTest(unittest.TestCase):
    def test_there_are_three_cases(self):
        self.assertEqual(CASE_NAMES, ["drafting-desk", "rules-desk", "static-notes"])

    def test_expected_files_are_well_formed(self):
        ids = rubric_ids()
        for name in CASE_NAMES:
            case = os.path.join(CASES, name)
            exp = load(os.path.join(case, "expected.json"))
            with self.subTest(case=name):
                self.assertEqual(exp["case"], name)
                self.assertTrue(set(exp["archetype"]["allowed"]) <= set(MODEL["archetype_exclusions"]))
                self.assertTrue(set(exp["scope_facts"]) <= set(MODEL["scope_facts"]))
                self.assertTrue(15 <= len(exp["criteria"]) <= 25, len(exp["criteria"]))
                self.assertTrue(set(exp["criteria"]) <= ids, set(exp["criteria"]) - ids)
                self.assertTrue(set(exp.get("ai_readings", {})) <= set(MODEL["ai_view"]["readings"]))
                traps = [c for c in exp["criteria"].values() if c.get("trap")] + \
                    [c for c in exp.get("ai_readings", {}).values() if c.get("trap")]
                self.assertGreaterEqual(len(traps), 3)
                specs = list(exp["criteria"].values()) + list(exp.get("ai_readings", {}).values())
                for spec in specs:
                    if "range" in spec:
                        lo, hi = spec["range"]
                        self.assertTrue(0 <= lo <= hi <= 4, spec)
                    else:
                        self.assertIn(spec["status"], ("not_applicable", "not_evidenced"))
                kinds = exp["change_kinds"]
                for k in kinds["kinds"]:
                    self.assertTrue(k["keywords"] and 0 <= k["reach"][0] <= k["reach"][1] <= 5, k)
                self.assertEqual(set(exp["loops"]), set(MODEL["loops"]))
                everything = [exp["archetype"]] + list(exp["scope_facts"].values()) + specs + kinds["kinds"] + \
                    [v for key, v in kinds.items() if key != "kinds"] + list(exp["loops"].values())
                for spec in everything:
                    self.assertTrue(spec["reason"].strip(), spec)
                    self.assertTrue(spec["files"], spec)
                    for f in spec["files"]:
                        self.assertTrue(os.path.isfile(os.path.join(case, "repo", f)), f"{name}: {f}")

    def test_fixtures_stay_small(self):
        for name in CASE_NAMES:
            total = 0
            for folder, _dirs, files in os.walk(os.path.join(CASES, name, "repo")):
                for f in files:
                    with open(os.path.join(folder, f), encoding="utf-8") as handle:
                        total += sum(1 for _ in handle)
            with self.subTest(case=name):
                self.assertTrue(100 <= total <= 800, total)

    def test_reference_readings_reach_the_expected_levels(self):
        """Read every expectation at the low end, then at the high end, of its range: the real
        scorer must accept the assessment and every expectation, loop levels included, must hold."""
        with tempfile.TemporaryDirectory() as tmp:
            for name in CASE_NAMES:
                for pick in (min, max):
                    path = os.path.join(tmp, f"{name}-{pick.__name__}.json")
                    with open(path, "w", encoding="utf-8") as handle:
                        json.dump(reference(os.path.join(CASES, name), pick), handle)
                    result = run.evaluate(os.path.join(CASES, name), path, scorer=SCORER)
                    with self.subTest(case=name, end=pick.__name__):
                        self.assertIsNone(result["levels_unavailable_because"])
                        self.assertEqual(result["met"], result["counted"],
                                         [i for i in result["items"] if not i["met"]])


if __name__ == "__main__":
    unittest.main()
