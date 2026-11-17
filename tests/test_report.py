"""Tests for skills/evolvable-software/scripts/report.py. Run with: python3 -m unittest discover -s tests"""

import contextlib
import copy
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
import report  # noqa: E402
import score  # noqa: E402

RUBRIC = os.path.join(SKILL, "references", "rubric.md")
PLAIN_PATH = os.path.join(SKILL, "references", "plain-language.md")
CRITERIA, ORDER, MODEL = score.load_rubric(RUBRIC)
PLAIN = report.load_plain(PLAIN_PATH)
ALL_FACETS = {"implemented": True, "tested": True, "operated": True}
TITLES = [title for _, title in report.SECTIONS]


def kinds_at(reach, main=(True, True, False)):
    """Kinds of change, all at one reach: two main kinds and one that is not, unless main says otherwise."""
    names = ("settings", "workflows", "reports")
    return [{"id": names[i], "name": f"Change the {names[i]}", "who": "admins", "main": m, "reach": reach,
             "evidence": f"docs/{names[i]}.md"} for i, m in enumerate(main)]


def product(value=3, facts=None, kinds=None):
    """An assessment with every criterion at one value, depth facets and inventories filled in.
    Kinds of change are self-serve when value is 2 or more and engineers only below that."""
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
    return {"product": "P", "date": "2026-01-01", "source": "repo@abc",
            "archetype": "configurable-application-platform",
            "scope_facts": {f: {"value": v, "evidence": "README"} for f, v in facts.items()},
            "change_kinds": kinds_at(1 if value >= 2 else 0) if kinds is None else kinds,
            "scores": scores}


def set_score(data, cid, value):
    entry = data["scores"][cid]
    entry["score"] = value
    if "inventory" in entry:
        entry["inventory"] = {k: value for k in entry["inventory"]}


def level_one():
    data = product(1, kinds=kinds_at(1))
    for cid in ("GOV-05", "DEL-11", "LRN-03", "EXP-02"):
        set_score(data, cid, 2)
    return data


def level_four():
    data = product(3)
    set_score(data, "GOV-05", 4)
    set_score(data, "DEL-11", 4)
    return data


def design():
    data = product(2)
    data["basis"] = "design"
    data["scores"]["MAL-01"]["grade"] = "D"
    return data


def proven():
    data = product(2)
    data["proven"] = {"request": {"level": 1, "evidence": "changelog shows settings changes"},
                      "fix": {"level": 2, "evidence": "incident records"},
                      "expansion": {"status": "not_evidenced", "searched": "release notes"}}
    return data


def no_ai():
    return product(2, facts={"ai_features": False, "ai_data_access": False, "ai_actions": False})


PRODUCTS = {
    "L0": (lambda: product(1), 0),
    "L1": (level_one, 1),
    "L2": (lambda: product(2), 2),
    "L3": (lambda: product(3), 3),
    "L4": (level_four, 4),
    "L5": (lambda: product(4), 5),
    "design": (design, 2),
    "proven": (proven, 2),
    "no AI features": (no_ai, 2),
    "AI features": (lambda: product(2), 2),
}


def build(data, plain=PLAIN):
    return report.build_report(data, CRITERIA, ORDER, MODEL, plain)


def section(rep, sid):
    return next(s for s in rep["sections"] if s["id"] == sid)


def text(rep, sid):
    return "\n".join(report.render_section(section(rep, sid)))


def body(rep):
    return "\n".join(report.body_text(rep))


def run(data, *args, plain=None):
    """(exit code, stdout, stderr) of report.main on a temporary assessment file."""
    tmp = tempfile.mkdtemp()
    try:
        path = os.path.join(tmp, "a.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        out, err = io.StringIO(), io.StringIO()
        extra = ["--plain", plain] if plain else []
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = report.main([path, *args, *extra])
        return code, out.getvalue(), err.getvalue()
    finally:
        shutil.rmtree(tmp)


def plain_with(old, new):
    """A temporary copy of plain-language.md with one replacement; returns (directory, path)."""
    with open(PLAIN_PATH, encoding="utf-8") as handle:
        content = handle.read()
    assert old in content, old
    tmp = tempfile.mkdtemp()
    path = os.path.join(tmp, "plain-language.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content.replace(old, new, 1))
    return tmp, path


class PlainLanguageTests(unittest.TestCase):
    def test_the_file_has_every_entry_the_report_needs(self):
        self.assertEqual(report.check_plain(PLAIN, CRITERIA, ORDER, MODEL), [])

    def test_parser_reads_sections_keys_and_fields(self):
        self.assertEqual(PLAIN["Levels"]["L1"]["Name"], "Configurable")
        self.assertEqual(PLAIN["Controls"]["Definition rollback"]["Name"],
                         "Undo for every change people and AI make in the product")
        self.assertEqual(set(PLAIN["Criteria"]), set(ORDER))
        self.assertTrue(all(PLAIN["Criteria"][c]["Gap"] for c in ORDER))

    def test_refuses_when_a_criterion_entry_is_missing(self):
        start = "### GOV-05\n"
        with open(PLAIN_PATH, encoding="utf-8") as handle:
            content = handle.read()
        block = content[content.index(start):content.index("### GOV-06\n")]
        tmp, path = plain_with(block, "")
        try:
            code, out, err = run(product(2), plain=path)
        finally:
            shutil.rmtree(tmp)
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("PLAIN LANGUAGE INCOMPLETE", err)
        self.assertIn("### GOV-05: missing", err)

    def test_refuses_when_a_control_or_field_is_missing(self):
        tmp, path = plain_with("### Release rollback\n", "### Release undo\n")
        try:
            code, _, err = run(product(2), plain=path)
        finally:
            shutil.rmtree(tmp)
        self.assertEqual(code, 2)
        self.assertIn("## Controls / ### Release rollback: missing", err)
        gap = "Gap: The product's own AI does not build accepted changes from start to finish, " \
              "so a person still builds or completes each one.\n"
        tmp, path = plain_with(gap, "")
        try:
            code, _, err = run(product(2), plain=path)
        finally:
            shutil.rmtree(tmp)
        self.assertEqual(code, 2)
        self.assertIn("### DEL-04: needs Gap", err)

    def test_every_kind_of_entry_is_required(self):
        sections = {s for s, _, _ in report.required_entries(CRITERIA, ORDER, MODEL)}
        self.assertEqual(sections, {"Levels", "Loops", "Parts", "Stages", "Controls", "Capabilities", "Scope facts",
                                    "Reach", "Recursion", "AI readiness", "Criteria"})


class BodyTests(unittest.TestCase):
    def test_levels_are_as_expected(self):
        for name, (make, level) in PRODUCTS.items():
            with self.subTest(name):
                data = make()
                self.assertEqual(score.validate(data, CRITERIA, ORDER, MODEL), [])
                self.assertEqual(section(build(data), "summary")["data"]["level"], level)

    def test_body_has_no_codes_or_banned_words(self):
        for name, (make, _) in PRODUCTS.items():
            with self.subTest(name):
                text_ = body(build(make()))
                self.assertIsNone(report.CODE.search(text_), report.CODE.findall(text_))
                self.assertIsNone(report.BANNED.search(text_), report.BANNED.findall(text_))

    def test_banned_pattern_catches_the_listed_words(self):
        for word in ("rollback", "Tenant", "tenants", "schema", "migrations", "CRUD", "DDL", "canary", "idempotent",
                     "telemetry", "deploy", "redeploy", "deployment", "pipeline", "provenance"):
            self.assertTrue(report.BANNED.search(f"a {word} here"), word)
        for word in ("middle", "undo", "release", "rolled back"):
            self.assertFalse(report.BANNED.search(f"a {word} here"), word)

    def test_every_section_is_present_and_in_order(self):
        for name, (make, _) in PRODUCTS.items():
            with self.subTest(name):
                code, out, _ = run(make())
                self.assertEqual(code, 0)
                headings = [line[3:] for line in out.splitlines() if line.startswith("## ")]
                self.assertEqual(headings, TITLES)

    def test_codes_appear_only_for_engineers(self):
        rep = build(product(2))
        engineers = text(rep, "engineers")
        self.assertIn("| AI builds accepted changes | DEL-04 | 2 |", engineers)
        self.assertIn("Built to SAL 2 (Assisted)", engineers)

    def test_guard_fails_loudly_on_a_defective_entry(self):
        plain = copy.deepcopy(PLAIN)
        plain["Criteria"]["ARC-09"]["Gap"] = "There is no rollback for data."
        with self.assertRaises(report.ReportDefect) as ctx:
            build(product(2), plain)
        self.assertIn("rollback", str(ctx.exception))
        plain["Criteria"]["ARC-09"]["Gap"] = "See ARC-09."
        with self.assertRaises(report.ReportDefect):
            build(product(2), plain)

    def test_guard_names_a_jargon_kind_name(self):
        data = product(1)
        data["change_kinds"][0]["name"] = "Deploy a new pipeline"
        code, out, err = run(data)
        self.assertEqual(code, 3)
        self.assertEqual(out, "")
        self.assertIn("REPORT DEFECT", err)
        self.assertIn("Deploy a new pipeline", err)

    def test_works_today_is_short_and_grouped(self):
        rep = build(product(3))
        items = [b for b in section(rep, "works")["blocks"] if b["type"] == "list"][0]["items"]
        self.assertLessEqual(len(items), 8)
        self.assertTrue(items[0].startswith("**Technical foundation:**"))
        self.assertIn("and ", items[0])
        self.assertIn("Nothing is yet rated strong", text(build(product(2)), "works"))


class SummaryTests(unittest.TestCase):
    def test_headline_in_words(self):
        summary = text(build(level_one()), "summary")
        self.assertIn("Built to Level 1, Configurable: the people running the product can make the changes they "
                      "need most without engineers, and can undo them. Not yet proven in operation.", summary)
        self.assertIn("In practice, someone running the product makes the change", summary)
        self.assertIn("The biggest thing holding it back is that ", summary)

    def test_top_level(self):
        summary = text(build(product(4)), "summary")
        self.assertIn("Built to Level 5, Self-directing", summary)
        self.assertIn("nothing holds it back", summary)

    def test_biggest_gap_is_the_build_path_in_words(self):
        data = product(1, kinds=kinds_at(0, main=(True, True, False)))
        data["change_kinds"][0]["reach"] = 1
        for cid in ("GOV-05", "DEL-11", "LRN-03"):  # undo and problem detection pass; only the build step holds
            set_score(data, cid, 2)
        rep = build(data)
        self.assertIn("is that not every main kind of change can be made by the people running the product: "
                      "Change the workflows.", text(rep, "summary"))


class WhereItStandsTests(unittest.TestCase):
    def test_each_loop_in_words(self):
        stands = text(build(product(2)), "stands")
        self.assertIn("**From request to release.** Can the product take a user's request", stands)
        self.assertIn("- Built to Level 2, Assisted. The product takes in requests", stands)
        self.assertIn("Held at this level by ", stands)
        self.assertIn("- Proven: not evidenced.", stands)

    def test_design_and_proven_are_never_mixed(self):
        design_rep = build(design())
        text_ = body(design_rep)
        self.assertIn("Designed for Level 2, Assisted", text_)
        self.assertIn("not comparable with a shipped reading", text(design_rep, "summary"))
        self.assertIn("not comparable with a shipped reading", text(design_rep, "stands"))
        self.assertNotIn("Built to", text_)
        self.assertNotIn("Proven:", text_)
        self.assertNotIn("Proven at", text_)
        self.assertIn("Not read. A design reading has no operating records", text(design_rep, "proven"))
        for make in (lambda: product(2), proven):
            shipped = body(build(make()))
            self.assertNotIn("Designed for", shipped)
            self.assertNotIn("not comparable", shipped)

    def test_proven_levels(self):
        rep = build(proven())
        self.assertIn("Proven in operation at Level 1, Configurable.", text(rep, "summary"))
        stands = text(rep, "stands")
        self.assertIn("- Proven at Level 1, Configurable.", stands)
        self.assertIn("- Proven at Level 2, Assisted.", stands)
        prov = text(rep, "proven")
        self.assertIn("From request to release: proven at Level 1, Configurable. It is built to Level 2.", prov)
        self.assertIn("From unmet need to new offering: not evidenced. The rater looked", prov)
        self.assertNotIn("Nobody observed", prov)

    def test_repository_alone_says_operation_was_not_observed(self):
        prov = text(build(product(2)), "proven")
        self.assertIn("Not yet proven in operation.", prov)
        self.assertIn("Nobody observed the product in operation", prov)


class KindsTests(unittest.TestCase):
    def test_table_and_summary(self):
        data = product(2)
        data["change_kinds"][1]["reach"] = 0
        rep = build(data)
        kinds = text(rep, "kinds")
        self.assertIn("| Kind of change | Who makes it | How far it has come | Main kind |", kinds)
        self.assertIn("| Change the settings | admins | Self-serve. The people running the product make this kind of "
                      "change themselves, without a release, and can undo it. | Yes |", kinds)
        self.assertIn("| Change the workflows | admins | Engineers only.", kinds)
        self.assertIn("| Change the reports | admins | Self-serve.", kinds)
        self.assertIn("1 of 2 main kinds are self-serve.", kinds)
        self.assertEqual(section(rep, "kinds")["data"]["main_self_serve"], 1)

    def test_pipes_in_kind_names_are_escaped(self):
        data = product(2)
        data["change_kinds"][0]["name"] = "Prices | discounts"
        self.assertIn("Prices \\| discounts", text(build(data), "kinds"))


class HoldsBackTests(unittest.TestCase):
    def test_gaps_are_deduplicated_and_ordered_by_loops_held(self):
        data = product(2)
        set_score(data, "ARC-06", 0)  # architecture: holds every loop at L1
        set_score(data, "LRN-05", 1)  # fix only
        rep = build(data)
        items = section(rep, "holds")["data"]["items"]
        keys = [i["key"] for i in items]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(keys[0], "ARC-06")
        self.assertEqual(len(items[0]["loops"]), 3)
        lrn05 = next(i for i in items if i["key"] == "LRN-05")
        self.assertEqual([l["loop"] for l in lrn05["loops"]], ["fix"])
        holds = text(rep, "holds")
        self.assertIn(PLAIN["Criteria"]["ARC-06"]["Gap"] + " Holds back all three loops.", holds)
        self.assertIn("**Work out the cause.** " + PLAIN["Criteria"]["LRN-05"]["Gap"], holds)

    def test_build_path_in_words(self):
        data = product(1)
        data["change_kinds"][0]["reach"] = 1
        holds = text(build(data), "holds")
        self.assertIn("Not every main kind of change can be made by the people running the product: "
                      "Change the workflows.", holds)
        self.assertIn(PLAIN["Criteria"]["EXP-02"]["Gap"], holds)

    def test_top_level_has_nothing(self):
        self.assertIn("Every loop is at the top level.", text(build(product(4)), "holds"))


class SafetyGateTests(unittest.TestCase):
    def test_failed_gates_say_why(self):
        gates = text(build(product(2)), "gates")
        backup = PLAIN["Controls"]["Tested backup and restore"]
        self.assertIn(f"| {backup['Name']} | Not yet | {backup['Why']} |", gates)
        self.assertIn("0 of 7 that apply have passed.", gates)

    def test_passed_and_not_applicable(self):
        data = product(3, facts={"multi_tenant": False})
        gates = text(build(data), "gates")
        apart = PLAIN["Controls"]["Tenant isolation"]["Name"]
        self.assertIn(f"| {apart} | Does not apply |  |", gates)
        self.assertIn("| Backups that are proven to restore | Passed |  |", gates)
        self.assertIn("6 of 6 that apply have passed.", gates)


class AITests(unittest.TestCase):
    def test_ai_features(self):
        ai = text(build(product(2)), "ai")
        self.assertIn("From request to release: AI does the work up to Level 2, Assisted.", ai)
        self.assertIn("How safe its AI features are to run for real customers: 2 out of 4.", ai)
        self.assertIn("Worse AI results block a release: not yet.", ai)
        self.assertIn("No AI delivery record.", ai)

    def test_no_ai_features(self):
        ai = text(build(no_ai()), "ai")
        self.assertIn("The product has no AI features, so the checks on AI features do not apply.", ai)
        self.assertNotIn("out of 4", ai)

    def test_low_levels_drive_nothing(self):
        self.assertIn("AI does none of the steps on its own yet.", text(build(level_one()), "ai"))

    def test_ai_delivery_says_whether_it_counts(self):
        data = product(2)
        data["ai_delivery"] = {"present": True, "qualifies": False, "evidence": "AGENTS.md"}
        ai = text(build(data), "ai")
        self.assertIn("not the product evolving itself. It is not installed, enforced and limited as part", ai)
        data["ai_delivery"]["qualifies"] = True
        self.assertIn("may credit it as the product's own way of changing", text(build(data), "ai"))


class RecursionTests(unittest.TestCase):
    def test_step_name_and_meaning(self):
        data = product(2)
        set_score(data, "LRN-10", 3)
        rec = text(build(data), "recursion")
        self.assertIn("**Results-driven** (step 3 of 4). " + PLAIN["Recursion"]["3"]["Meaning"], rec)

    def test_not_evidenced(self):
        data = product(2)
        data["scores"]["LRN-10"] = {"status": "not_evidenced", "searched": "src/"}
        self.assertIn("No evidence was found", text(build(data), "recursion"))


class ConfidenceTests(unittest.TestCase):
    def test_counts_check_first_coverage_and_one_rater(self):
        data = product(2)
        for cid in ORDER:
            if data["scores"][cid]["status"] == "assessed":
                data["scores"][cid]["confidence"] = "high"
        data["scores"]["DEL-05"]["confidence"] = "low"   # holds nothing at L2 → not listed
        set_score(data, "ARC-09", 2)
        data["scores"]["ARC-09"]["confidence"] = "low"   # holds the backup gate and the L3 architecture
        conf = text(build(data), "confidence")
        self.assertIn("with low confidence", conf)
        self.assertIn("Check these first.", conf)
        self.assertIn("Backups that are proven to restore: holds", conf)
        self.assertIn("the safety gate backups that are proven to restore", conf)
        self.assertIn("The reading answers 75 questions:", conf)
        self.assertIn("checked in the code", conf)
        self.assertIn("This is one rater's reading of the evidence.", conf)

    def test_not_recorded(self):
        self.assertIn("did not record how sure", text(build(product(2)), "confidence"))

    def test_alternate_and_opt_in_readings_that_change_a_level(self):
        data = product(2)
        data["scores"]["DEL-01"]["alt_score"] = 3
        data["scores"]["DEL-01"]["alt_note"] = "drafts specifications too"
        conf = text(build(data), "confidence")
        self.assertIn("Neither the higher readings", conf)  # one criterion alone does not move a loop here
        data = product(3)
        set_score(data, "GOV-05", 2)
        data["scores"]["GOV-05"]["available_score"] = 3
        data["scores"]["GOV-05"]["inventory"] = {"surface": 3}
        data["scores"]["GOV-05"]["score"] = 2
        self.assertEqual(score.validate(data, CRITERIA, ORDER, MODEL), [])
        conf = text(build(data), "confidence")
        self.assertIn("With settings that ship switched off turned on, From request to release would read "
                      "Level 3, Supervised", conf)
        self.assertIn("The overall level would be Level 3, Supervised.", conf)


class NextStepTests(unittest.TestCase):
    def test_challenges_for_the_headline_loops(self):
        nxt = text(build(product(1)), "next")
        self.assertIn("**From request to release, to Level 1, Configurable.**", nxt)
        self.assertIn("**From problem to fix, to Level 1, Configurable.**", nxt)
        self.assertNotIn("unmet need", nxt)
        self.assertIn("code change or new release", nxt)
        self.assertIn("blueprint.py", nxt)
        self.assertIn("--checklist 1", nxt)

    def test_challenge_words_are_made_plain(self):
        nxt = text(build(product(2)), "next")
        self.assertIn("customer organisations cannot reach each other's data", nxt)
        self.assertIn("the request-to-release check", nxt)
        self.assertIn("in real use", text(build(level_four()), "next"))
        self.assertIn("is at the top level", text(build(product(4)), "next"))

    def test_design_points_to_a_fresh_assessment(self):
        self.assertIn("fresh assessment of what ships", text(build(design()), "next"))


class CommandTests(unittest.TestCase):
    def test_refuses_an_invalid_assessment_like_the_scorer(self):
        data = product(2)
        del data["change_kinds"]
        code, out, _ = run(data)
        self.assertEqual(code, 2)
        self.assertTrue(out.startswith("VALIDATION FAILED"))
        self.assertIn("change_kinds: missing", out)

    def test_json_round_trip(self):
        for name in ("L1", "design", "proven"):
            with self.subTest(name):
                data = PRODUCTS[name][0]()
                code, out, _ = run(data, "--json")
                self.assertEqual(code, 0)
                payload = json.loads(out)
                self.assertEqual(payload, json.loads(json.dumps(build(data))))
                self.assertEqual([s["title"] for s in payload["sections"]], TITLES)
                code, markdown, _ = run(data)
                self.assertEqual(report.render(payload), markdown)

    def test_output_is_deterministic(self):
        data = proven()
        first, second = run(data), run(copy.deepcopy(data))
        self.assertEqual(first, second)
        self.assertEqual(run(data, "--json"), run(data, "--json"))


if __name__ == "__main__":
    unittest.main()
