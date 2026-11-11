"""Tests for skills/evolvable-software/scripts/quick_scan.py. Run with: python3 -m unittest tests.test_quick_scan -v"""

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
SKILL = os.path.join(ROOT, "skills", "evolvable-software")
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import quick_scan  # noqa: E402

QUESTIONS = os.path.join(SKILL, "references", "quick-scan.md")
MODEL = quick_scan.load_model(QUESTIONS)
IDS = [q["id"] for q in MODEL["questions"]]
GATES = [q["id"] for q in MODEL["questions"] if q.get("gate")]
NA_ALLOWED = [q["id"] for q in MODEL["questions"] if q.get("allows_na")]
LOOPS = [loop["id"] for loop in MODEL["loops"]]


def answers(value="yes", **overrides):
    out = {qid: value for qid in IDS}
    for key, val in overrides.items():
        out[key.replace("_", "-")] = val
    return out


def reading(ans):
    product, clean, notes = quick_scan.validate(MODEL, {"product": "Test", "answers": ans})
    return quick_scan.scan(MODEL, product, clean, notes)


def ranges(result):
    return {loop["id"]: (loop["low"], loop["high"]) for loop in result["loops"]}


class RunMixin:
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write(self, data, name="answers.json"):
        path = os.path.join(self.tmp, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(data if isinstance(data, str) else json.dumps(data))
        return path

    def run_main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = quick_scan.main(list(argv))
        return code, out.getvalue(), err.getvalue()


class TestQuestionFile(unittest.TestCase):
    def test_question_count(self):
        self.assertGreaterEqual(len(IDS), 16)
        self.assertLessEqual(len(IDS), 22)

    def test_table_matches_json(self):
        with open(QUESTIONS, encoding="utf-8") as handle:
            text = handle.read()
        start = text.index(quick_scan.TABLE_START) + len(quick_scan.TABLE_START)
        end = text.index(quick_scan.TABLE_END)
        self.assertEqual(text[start:end].strip("\n"), quick_scan.render_table(MODEL),
                         "regenerate the tables with quick_scan.py --table")

    def test_table_lists_every_id_once(self):
        with open(QUESTIONS, encoding="utf-8") as handle:
            text = handle.read()
        table = text[text.index(quick_scan.TABLE_START):text.index(quick_scan.TABLE_END)]
        listed = re.findall(r"^\| \d+ \| `([a-z0-9-]+)` \|", table, re.M)
        self.assertEqual(listed, IDS)

    def test_plain_words(self):
        banned = re.compile(r"\b(rollback|roll back|tenant|schema|CI|deploy\w*|pipeline|SLO|canary)\b", re.I)
        code = re.compile(r"\b[A-Z]{3}-\d{2}\b")
        for q in MODEL["questions"]:
            for field in ("question", "where", "maps_to", "allows_na", "gate"):
                text = q.get(field, "")
                self.assertIsNone(banned.search(text), "%s.%s: %s" % (q["id"], field, text))
                self.assertIsNone(code.search(text), "%s.%s: %s" % (q["id"], field, text))

    def test_covers_sections_in_order(self):
        sections = []
        for q in MODEL["questions"]:
            if q["section"] not in sections:
                sections.append(q["section"])
        self.assertEqual(sections, ["Kinds of change", "Request → Release", "Issue → Fix",
                                    "Opportunity → Expansion", "Measurement", "Recursion", "Safety gates"])
        self.assertEqual(len(GATES), 7)
        self.assertEqual(sorted(NA_ALLOWED), ["gate-ai-limits", "gate-customer-isolation"])

    def test_bad_model_is_refused(self):
        broken = json.loads(json.dumps(MODEL))
        broken["loops"][0]["levels"]["2"].append("no-such-question")
        with self.assertRaises(quick_scan.QuickScanError):
            quick_scan.check_model(broken)


class TestReading(unittest.TestCase):
    def test_notice_comes_first(self):
        result = reading(answers("yes"))
        self.assertEqual(list(result)[0], "notice")
        md = quick_scan.render_markdown(result)
        self.assertIn("Indicative quick scan, not an EVOLVE assessment", md.splitlines()[0])
        self.assertIn("do not publish it as a level", md.splitlines()[0])

    def test_all_yes_stops_at_level_4(self):
        result = reading(answers("yes"))
        self.assertEqual(ranges(result), {lid: (4, 4) for lid in LOOPS})
        self.assertEqual(result["loops"][0]["range"], "likely L4")
        kinds = [cap["kind"] for cap in result["caps"]]
        self.assertEqual(kinds, ["level-5"])
        self.assertIn("never reports Level 5", result["caps"][0]["text"])
        self.assertTrue(all(g["reading"] == "closed" for g in result["safety_gates"]))
        self.assertEqual(result["most_change"], [])
        self.assertNotIn("L5", quick_scan.render_markdown(result).split("## Safety gates")[0])

    def test_all_no(self):
        result = reading(answers("no"))
        self.assertEqual(ranges(result), {lid: (0, 0) for lid in LOOPS})
        self.assertEqual(result["caps"], [])
        self.assertTrue(all(g["reading"] == "open" for g in result["safety_gates"]))
        top = [item["id"] for item in result["most_change"]]
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0], "self-undo")  # it holds back all three loops
        self.assertIn("self-serve", top)

    def test_level_needs_every_lower_level(self):
        # everything yes except a Level 1 question: the loop reads 0, not 4
        result = reading(answers("yes", self_undo="no"))
        self.assertEqual(ranges(result), {lid: (0, 0) for lid in LOOPS})
        result = reading(answers("yes", notices_problems="no"))
        self.assertEqual(ranges(result)["fix"], (0, 0))
        self.assertEqual(ranges(result)["request"], (4, 4))

    def test_level_1_by_drafting(self):
        # the full framework's Level 1 is people >= 2 or product >= 2
        result = reading(answers("no", self_undo="yes", drafts_change="yes"))
        self.assertEqual(ranges(result)["request"], (1, 1))
        self.assertEqual(ranges(result)["expansion"], (1, 1))

    def test_unsure_widens_the_range(self):
        result = reading(answers("yes", request_capture="unsure"))
        self.assertEqual(ranges(result)["request"], (1, 4))
        self.assertEqual(result["loops"][0]["range"], "likely L1 to L4")
        self.assertEqual(ranges(result)["fix"], (4, 4))
        self.assertEqual(result["unsure"], ["request-capture"])
        self.assertEqual(result["most_change"][0]["id"], "request-capture")
        checks = {c["loop"]: c for c in result["next_checks"]}
        self.assertEqual(checks["Request → Release"]["level"], 2)
        self.assertEqual(checks["Request → Release"]["verb"], "Confirm")

    def test_all_unsure(self):
        result = reading(answers("unsure"))
        # high end would be 4, but unsure safety gates are not yes, so the cap holds it at 2
        self.assertEqual(ranges(result), {lid: (0, 2) for lid in LOOPS})
        self.assertTrue(all(loop["capped_by_safety_gates"] for loop in result["loops"]))
        self.assertTrue(all(g["reading"] == "unknown" for g in result["safety_gates"]))

    def test_safety_gate_cap(self):
        for gate in GATES:
            for value in ("no", "unsure"):
                result = reading(answers("yes", **{gate.replace("-", "_"): value}))
                self.assertEqual(ranges(result), {lid: (2, 2) for lid in LOOPS}, (gate, value))
                caps = [cap for cap in result["caps"] if cap["kind"] == "safety-gates"]
                self.assertEqual(len(caps), 1)
                name = next(q["gate"] for q in MODEL["questions"] if q["id"] == gate)
                self.assertIn(name, caps[0]["text"])
                self.assertEqual(result["loops"][0]["uncapped_range"], "likely L4")
                md = quick_scan.render_markdown(result)
                self.assertIn("held at L2 by safety gates", md)

    def test_cap_reported_only_when_it_bites(self):
        result = reading(answers("no", self_serve="yes", self_undo="yes"))
        self.assertEqual(ranges(result)["request"], (1, 1))
        self.assertFalse([cap for cap in result["caps"] if cap["kind"] == "safety-gates"])

    def test_gate_is_most_influential_when_it_holds_the_cap(self):
        result = reading(answers("yes", gate_backup_restored="unsure"))
        self.assertEqual(result["most_change"][0]["id"], "gate-backup-restored")

    def test_not_applicable_gates(self):
        # a gate that does not apply never caps
        result = reading(answers("yes", gate_customer_isolation="n/a"))
        self.assertEqual(ranges(result), {lid: (4, 4) for lid in LOOPS})
        readings = {g["id"]: g["reading"] for g in result["safety_gates"]}
        self.assertEqual(readings["gate-customer-isolation"], "not applicable")
        result = reading(answers("yes", gate_customer_isolation="n/a", gate_ai_limits="n/a",
                                 ships_pre_approved="no"))
        self.assertEqual(ranges(result), {lid: (3, 3) for lid in LOOPS})
        self.assertEqual(result["counts"]["n/a"], 2)
        self.assertEqual(result["caps"], [])

    def test_next_checks(self):
        result = reading(answers("no", self_serve="yes", self_undo="yes", notices_problems="yes"))
        checks = {c["loop"]: c for c in result["next_checks"]}
        self.assertEqual(checks["Issue → Fix"]["level"], 2)
        self.assertEqual(checks["Issue → Fix"]["verb"], "Toward")
        self.assertEqual(checks["Issue → Fix"]["check"], MODEL["challenges"]["fix"]["2"])
        result = reading(answers("yes"))
        self.assertTrue(all(c["level"] == 5 and "beyond a quick scan" in c["check"] for c in result["next_checks"]))


class TestValidation(RunMixin, unittest.TestCase):
    def errors(self, data):
        with self.assertRaises(quick_scan.QuickScanError) as ctx:
            quick_scan.validate(MODEL, data)
        return "\n".join(ctx.exception.errors)

    def test_unknown_id(self):
        ans = answers("yes")
        ans["made-up"] = "yes"
        self.assertIn("unknown question id 'made-up'", self.errors({"product": "X", "answers": ans}))

    def test_missing_id(self):
        ans = answers("yes")
        del ans["self-undo"]
        self.assertIn("missing self-undo", self.errors({"product": "X", "answers": ans}))

    def test_bad_values(self):
        message = self.errors({"product": "X", "answers": answers("yes", self_serve="maybe", self_undo="")})
        self.assertIn("answers.self-serve: 'maybe' is not one of", message)
        self.assertIn("answers.self-undo: not answered", message)
        self.assertIn("is not one of", self.errors({"product": "X", "answers": answers("yes", self_serve=True)}))

    def test_na_only_where_allowed(self):
        message = self.errors({"product": "X", "answers": answers("yes", self_serve="n/a")})
        self.assertIn("n/a is not allowed", message)

    def test_consistency(self):
        message = self.errors({"product": "X", "answers": answers("yes", gate_ai_limits="n/a")})
        self.assertIn("gate-ai-limits: cannot be n/a when ships-pre-approved is yes", message)
        quick_scan.validate(MODEL, {"product": "X", "answers": answers("yes", ships_pre_approved="no",
                                                                        gate_ai_limits="n/a")})

    def test_shape_errors(self):
        self.assertIn("product", self.errors({"answers": answers("yes")}))
        self.assertIn("Unknown top-level key 'extra'",
                      self.errors({"product": "X", "answers": answers("yes"), "extra": 1}))
        self.assertIn("answers: must be an object", self.errors({"product": "X", "answers": []}))
        self.assertIn("notes: unknown question id 'nope'",
                      self.errors({"product": "X", "answers": answers("yes"), "notes": {"nope": "x"}}))
        self.assertIn("must be a JSON object", self.errors([1, 2]))

    def test_values_are_normalised(self):
        _, clean, _ = quick_scan.validate(MODEL, {"product": "X", "answers": answers(" YES ")})
        self.assertEqual(set(clean.values()), {"yes"})

    def test_exit_code_2(self):
        ans = answers("yes")
        del ans["self-undo"]
        code, out, err = self.run_main(self.write({"product": "X", "answers": ans}))
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("error: answers: missing self-undo", err)
        code, _, err = self.run_main(self.write("{not json"))
        self.assertEqual(code, 2)
        self.assertIn("not valid JSON", err)
        code, _, err = self.run_main(os.path.join(self.tmp, "absent.json"))
        self.assertEqual(code, 2)
        code, _, err = self.run_main()
        self.assertEqual(code, 2)
        self.assertIn("--template", err)


class TestCommandLine(RunMixin, unittest.TestCase):
    def test_template_round_trip(self):
        code, out, _ = self.run_main("--template")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(list(data["answers"]), IDS)
        self.assertEqual(list(data["questions"]), IDS)
        code, _, err = self.run_main(self.write(data, "empty.json"))
        self.assertEqual(code, 2, "an unfilled template is not a valid answers file")
        self.assertIn("not answered", err)
        data["product"] = "Round trip"
        data["answers"] = {qid: "yes" for qid in data["answers"]}
        data["notes"] = {"self-serve": "admin guide"}
        code, out, err = self.run_main(self.write(data, "filled.json"), "--json")
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertEqual(result["product"], "Round trip")
        self.assertEqual({loop["high"] for loop in result["loops"]}, {4})

    def test_table_option(self):
        code, out, _ = self.run_main("--table")
        self.assertEqual(code, 0)
        self.assertEqual(out, quick_scan.render_table(MODEL) + "\n")

    def test_deterministic_output(self):
        path = self.write({"product": "Same", "answers": answers("unsure", self_serve="yes", gate_ai_limits="n/a",
                                                                 ships_pre_approved="no"),
                           "notes": {"self-serve": "a | b"}})
        first = [self.run_main(path), self.run_main(path, "--json")]
        second = [self.run_main(path), self.run_main(path, "--json")]
        self.assertEqual(first, second)
        md, js = first[0][1], first[1][1]
        self.assertTrue(md.startswith("> **Indicative quick scan, not an EVOLVE assessment"))
        self.assertIn("a \\| b", md)
        self.assertEqual(json.loads(js)["notice"], quick_scan.NOTICE)
        self.assertNotRegex(md, r"\b[A-Z]{3}-\d{2}\b")


if __name__ == "__main__":
    unittest.main()
