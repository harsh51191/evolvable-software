"""Tests for skills/evolvable-software/scripts/blueprint.py. Run with: python3 -m unittest discover -s tests"""

import contextlib
import copy
import io
import json
import os
import re
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import test_score  # noqa: E402  (shared helpers: assessment, kinds_at)
from test_score import CRITERIA, MODEL, ORDER, REMEDIATION, SKILL, assessment, set_score  # noqa: E402

import blueprint  # noqa: E402  (test_score put the scripts directory on the path)
import score  # noqa: E402

PLAIN = blueprint.load_plain(os.path.join(SKILL, "references", "plain-language.md"))
REMEDY = score.load_remediation(REMEDIATION, CRITERIA)
GOAL = "More customer questions resolved without a person"
# The Brand AI Apps assessment the blueprint format was modelled on. It lives outside this repository
# (the product is private); set BLUEPRINT_EXAMPLE to its path to include it.
EXAMPLE = os.environ.get("BLUEPRINT_EXAMPLE", "/tmp/claude-0/-home-user-insight-canvas/"
                         "041b1db5-929e-5c5d-bba1-ab8dfef472ae/scratchpad/brandai/assessment-v07.json")


def brand_like():
    """A small stand-in for Brand AI Apps: answers self-serve, the catalogue engineers only, forms not main;
    no AI building changes yet, so it reads Level 0."""
    data = assessment(2)
    data["change_kinds"] = [
        {"id": "answers", "name": "What the assistant tells customers", "who": "brand owners", "main": True,
         "reach": 1, "evidence": "settings-service.ts"},
        {"id": "catalog", "name": "Products and prices the assistant shows", "who": "brand owners", "main": True,
         "reach": 0, "evidence": "catalog.json, no editing path"},
        {"id": "forms", "name": "Forms customers fill in", "who": "operators", "main": False, "reach": 0,
         "evidence": "forms.js drafts do not publish"},
    ]
    for cid in ("DEL-04", "LRN-05", "LRN-07", "EXP-05"):
        set_score(data, cid, 1 if cid != "DEL-04" else 0)
        if "ai" in data["scores"][cid]:
            data["scores"][cid]["ai"]["score"] = 0
    return data


def plan_for(data, target=None, route="overlay", goal=GOAL):
    assert not score.validate(data, CRITERIA, ORDER, MODEL), score.validate(data, CRITERIA, ORDER, MODEL)
    plan = blueprint.build(data, CRITERIA, ORDER, MODEL, REMEDY, PLAIN, goal, target, route)
    plan["loop_names"] = {l: PLAIN["Loops"][l]["Name"] for l in MODEL["loops"]}
    return plan


def run(data_or_path, *args):
    tmp = tempfile.mkdtemp()
    try:
        path = data_or_path
        if not isinstance(data_or_path, str):
            path = os.path.join(tmp, "a.json")
            with open(path, "w") as handle:
                json.dump(data_or_path, handle)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = blueprint.main([path, *args])
        return code, out.getvalue()
    finally:
        shutil.rmtree(tmp)


def reader_text(markdown):
    """The skeleton without its "For engineers" blocks: what a business reader sees."""
    return re.sub(r"#### For engineers\n.*?(?=\n#### |\n## )", "", markdown, flags=re.S)


def engineer_text(markdown):
    return "\n".join(re.findall(r"#### For engineers\n(.*?)(?=\n#### |\n## )", markdown, flags=re.S))


def criteria_named_at(level, data):
    """Every criterion a level's conditions, its build paths or its reach needs can ask for."""
    named = set()
    for cond in MODEL["conditions"].get(str(level), []):
        for loop in MODEL["loops"]:
            for alt in blueprint._alternatives(cond, loop, MODEL, score.fact_values(data)):
                named.update(a[1] for a in alt if a[0] == "c")
    needs = MODEL["reach_needs"].get(str(level))
    if needs:
        named.update(score._test_ids(needs))
    return named


class ClassificationTests(unittest.TestCase):
    def test_every_criterion_is_user_visible_or_a_gate_exactly_once(self):
        user, gate = blueprint.VISIBILITY["user"], blueprint.VISIBILITY["gate"]
        self.assertEqual(len(user), len(set(user)))
        self.assertEqual(len(gate), len(set(gate)))
        self.assertFalse(set(user) & set(gate))
        self.assertEqual(set(user) | set(gate), set(ORDER))

    def test_critical_controls_are_gates(self):
        for cond in MODEL["conditions"]["3"]:
            if cond.get("control"):
                for cid in score._test_ids(cond):
                    self.assertEqual(blueprint.CLASS_OF[cid], "gate", cid)

    def test_building_blocks_cover_every_criterion_once(self):
        ids = [c for block in blueprint.BLOCKS.values() for c in block]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), set(ORDER))
        self.assertEqual(len(blueprint.BLOCKS), 8)

    def test_ai_stages_are_ai_qualified_readings(self):
        self.assertTrue(set(blueprint.AI_STAGES) <= set(MODEL["ai_view"]["readings"]))

    def test_plain_language_covers_what_the_blueprint_needs(self):
        self.assertEqual(blueprint.check_plain(PLAIN, ORDER, MODEL), [])


class MilestoneTests(unittest.TestCase):
    def test_milestone_count_follows_target(self):
        data = brand_like()
        for target in range(1, 6):
            plan = plan_for(data, target)
            self.assertEqual([m["level"] for m in plan["milestones"]], list(range(1, target + 1)))
            self.assertEqual(len(plan["beyond"]), 5 - target)
        self.assertEqual(len(plan_for(data)["milestones"]), 2)  # default: two levels above today

    def test_default_target_stops_at_level_5(self):
        data = assessment(3)
        today = score.score_assessment(data, CRITERIA, ORDER, MODEL)["variants"]["default"]["sal"]["headline"]
        self.assertEqual(today, 3)
        self.assertEqual(plan_for(data)["target"], 5)
        with self.assertRaises(ValueError):  # already at Level 5: nothing to plan
            plan_for(assessment(4))

    def test_target_at_or_below_today_is_refused(self):
        data = brand_like()
        with self.assertRaises(ValueError):
            plan_for(assessment(2), 2)
        code, out = run(assessment(2), "--goal", GOAL, "--target", "1")
        self.assertEqual(code, 2)
        self.assertIn("--target must be above", out)
        self.assertEqual(run(data, "--goal", " ")[0], 2)

    def test_each_milestone_reaches_its_level_when_everything_lands(self):
        for data in (brand_like(), assessment(0), assessment(1)):
            plan = plan_for(data, 5)
            for m in plan["milestones"]:
                self.assertEqual(m["level_after"], m["level"], (m["level"], data["scores"]["DEL-04"]))

    def test_level_1_names_the_main_kinds_not_yet_self_serve(self):
        m1 = plan_for(brand_like(), 1)["milestones"][0]
        kinds = [i for i in m1["user_items"] if i["type"] == "kinds"]
        self.assertEqual(len(kinds), 1)
        self.assertEqual([k["id"] for k in kinds[0]["kinds"]], ["catalog"])
        self.assertEqual([k["id"] for k in kinds[0]["not_main"]], ["forms"])
        text = " ".join(m1["what_changes_for_users"])
        self.assertIn("Products and prices the assistant shows", text)
        self.assertNotIn("Forms customers fill in", text)
        self.assertIn("Products and prices the assistant shows", " ".join(m1["check_kinds"]))

    def test_kinds_follow_reach_each_level(self):
        plan = plan_for(brand_like(), 5)
        for m in plan["milestones"]:
            kinds = [i for i in m["user_items"] if i["type"] == "kinds"]
            self.assertEqual([i["reach"] for i in kinds], [m["level"]])
            self.assertEqual(kinds[0]["reach_name"], MODEL["reach"][m["level"]])

    def test_reach_needs_are_planned_with_the_kinds(self):
        m2 = plan_for(brand_like(), 2)["milestones"][1]
        ids = {i["id"]: i["needs"] for i in m2["user_items"] + m2["gate_items"] if i["type"] == "criterion"}
        self.assertGreaterEqual(ids.get("DEL-04", 0), 2)

    def test_size_is_the_largest_move(self):
        for m in plan_for(brand_like(), 5)["milestones"]:
            sizes = [REMEDY[i["id"]]["size"] for i in m["user_items"] + m["gate_items"] if i["type"] == "criterion"]
            expected = max(sizes, key=blueprint.SIZES.index) if sizes else None
            self.assertEqual(m["size"], expected)

    def test_moves_for_engineers_come_from_the_catalogue(self):
        for m in plan_for(brand_like(), 5)["milestones"]:
            for i in m["user_items"] + m["gate_items"]:
                if i["type"] == "criterion":
                    self.assertEqual(i["move"], REMEDY[i["id"]]["to4" if i["needs"] >= 4 else "to3"])
                    self.assertEqual(i["anchor"], CRITERIA[i["id"]]["anchors"][i["needs"]])


class ValueLeadsTests(unittest.TestCase):
    def test_user_visible_items_come_before_gates(self):
        plan = plan_for(assessment(0), 5)
        md = blueprint.render(plan)
        for m in plan["milestones"]:
            self.assertTrue(all(i["class"] == "user" for i in m["user_items"]))
            self.assertTrue(all(i["class"] == "gate" for i in m["gate_items"]))
        blocks = re.findall(r"#### For engineers\n(.*?)(?=\n#### )", md, flags=re.S)
        self.assertEqual(len(blocks), 5)
        for block in blocks:
            classes = re.findall(r"\((user|gate), block:", block)
            self.assertTrue(classes)
            self.assertEqual(classes, sorted(classes, key=lambda c: c != "user"))
        for part in md.split("\n## Milestone ")[1:]:
            gains = part.split("#### What changes for users")[1].split("####")[0]
            self.assertNotIn("Backups that are proven to restore", gains)

    def test_gates_never_appear_before_the_milestone_that_needs_them(self):
        for data in (assessment(0), assessment(1), brand_like()):
            plan = plan_for(data, 5)
            for m in plan["milestones"]:
                named = criteria_named_at(m["level"], data)
                for g in m["gate_items"]:
                    self.assertIn(g["id"], named, (m["level"], g["id"]))
                    if g.get("control"):
                        self.assertEqual(m["level"], 3, g)
            for row in plan["gates"]:
                self.assertIn(row["id"], criteria_named_at(row["level"], data))

    def test_critical_controls_join_the_level_3_milestone(self):
        plan = plan_for(brand_like(), 3)
        m3 = plan["milestones"][2]
        controls = {g["control"] for g in m3["gate_items"] if g.get("control")}
        failing = {c["control"] for c in plan["controls"] if c["status"] == "fail"}
        self.assertEqual(controls, failing)
        for m in plan["milestones"][:2]:
            self.assertFalse([g for g in m["gate_items"] if g.get("control")])
        self.assertTrue(all(c["first_milestone"] == 3 for c in plan["controls"] if c["status"] == "fail"))

    def test_every_milestone_names_a_user_gain_or_says_how_to(self):
        data = assessment(2)
        for cid in ORDER:  # only gate criteria hold this product back
            if blueprint.CLASS_OF[cid] == "user" and data["scores"][cid]["status"] == "assessed":
                set_score(data, cid, 4)
                if cid in MODEL["depth_capped"]:
                    data["scores"][cid]["facets"] = dict(test_score.ALL_FACETS)
        data["change_kinds"] = [dict(k, reach=5) for k in data["change_kinds"]]
        for cid in ("DEL-04", "LRN-07"):
            data["scores"][cid]["facets"] = dict(test_score.ALL_FACETS)
        for k in ("GOV-07",):
            data["scores"][k]["facets"] = dict(test_score.ALL_FACETS)
        plan = plan_for(data, 3)
        m = plan["milestones"][-1]
        self.assertFalse(m["user_items"])
        self.assertEqual(m["what_changes_for_users"], [blueprint.GAIN_TODO])
        self.assertIn("if there is none, mark this step as a gate", blueprint.render(plan))
        for m in plan_for(brand_like(), 5)["milestones"]:
            self.assertTrue(m["what_changes_for_users"])


class RiskTests(unittest.TestCase):
    def test_ai_risk_when_ai_enters_scope(self):
        data = assessment(1, facts={"ai_features": False, "ai_data_access": False, "ai_actions": False})
        plan = plan_for(data, 2)
        m1, m2 = plan["milestones"]
        self.assertFalse([r for r in m1["risks"] if "AI Readiness" in r])
        self.assertIn("DEL-04", m2["ai_stages_raised"])
        risks = " ".join(m2["risks"])
        self.assertIn("brings the AI Readiness checks into scope".lower(), risks.lower())
        self.assertIn("privacy", risks)
        self.assertIn("cost", risks)

    def test_no_scope_warning_when_ai_is_already_there(self):
        plan = plan_for(brand_like(), 2)
        risks = " ".join(plan["milestones"][1]["risks"])
        self.assertNotIn("Brings the AI Readiness checks into scope", risks)
        self.assertIn("already has AI features", risks)

    def test_gates_are_named_as_risks(self):
        m3 = plan_for(brand_like(), 3)["milestones"][2]
        risks = " ".join(m3["risks"])
        for g in m3["gate_items"]:
            name = PLAIN["Controls"][g["control"]]["Name"] if g.get("control") else g["name"]
            self.assertIn(name, risks)

    def test_level_4_brings_auto_apply_into_scope(self):
        data = brand_like()
        data["scope_facts"]["evolution_auto_apply"]["value"] = False
        data["scope_facts"]["agent_mutations"]["value"] = False
        for cid in ("GOV-10", "GOV-11"):
            data["scores"][cid] = {"status": "not_applicable", "rationale": "no self-change",
                                   "ai": {"status": "not_applicable", "rationale": "no self-change"}}
        m4 = plan_for(data, 4)["milestones"][3]
        self.assertIn(PLAIN["Criteria"]["GOV-10"]["Name"], " ".join(m4["risks"]))

    def test_overlay_route_flags_storage_changes(self):
        overlay = plan_for(assessment(0), 3, "overlay")
        incremental = plan_for(assessment(0), 3, "incremental")
        flagged = {i["id"] for m in overlay["milestones"] for i in m["gate_items"] + m["user_items"]
                   if i.get("overlay_flag")}
        self.assertIn("ARC-02", flagged)  # "Run migrations in CI ..."
        self.assertNotIn("DEL-05", flagged)
        self.assertFalse([i for m in incremental["milestones"] for i in m["gate_items"] + m["user_items"]
                          if i.get("overlay_flag")])
        self.assertIn("keyword rule", blueprint.render(overlay))


class OutputTests(unittest.TestCase):
    SECTIONS = ["## Goal", "## In one paragraph", "## What this does and does not change",
                "## Where it stands today", "## The destination", "## The progress map", "## Milestone 1",
                "## Safety gates", "## Beyond", "## How the level will be confirmed", "## Notes on the assessment"]
    MILESTONE = ["#### What changes for users", "#### Why this moves the product up", "#### The check",
                 "#### Risks and what it brings into scope", "#### People", "#### For engineers",
                 "#### Prompt for a coding agent", "#### Done when"]

    def test_sections_in_order(self):
        code, md = run(brand_like(), "--goal", GOAL)
        self.assertEqual(code, 0)
        positions = [md.index(s) for s in self.SECTIONS]
        self.assertEqual(positions, sorted(positions))
        for part in md.split("\n## Milestone ")[1:]:
            positions = [part.index(s) for s in self.MILESTONE]
            self.assertEqual(positions, sorted(positions))
        self.assertIn(GOAL, md)

    def test_reader_sections_have_no_criterion_codes(self):
        for data, target in ((brand_like(), 5), (assessment(0), 5), (assessment(1), 3)):
            md = blueprint.render(plan_for(data, target))
            self.assertEqual(re.findall(score.ID, reader_text(md)), [])

    def test_codes_appear_under_for_engineers(self):
        md = blueprint.render(plan_for(brand_like(), 3))
        eng = engineer_text(md)
        self.assertIn("`DEL-04`", eng)
        self.assertIn("`ARC-09`", eng)
        self.assertIn("critical control", eng)
        self.assertIn("block:", eng)  # building blocks only here
        for block in blueprint.BLOCKS:
            self.assertNotIn(f"block: {block}", reader_text(md))

    def test_done_when_names_an_automated_test_and_a_fresh_assessment(self):
        md = blueprint.render(plan_for(brand_like(), 2))
        self.assertEqual(md.count("An automated test performs the check"), 2)
        self.assertEqual(md.count("made without sight of this blueprint"), 3)  # two milestones and the confirmation

    def test_todo_markers_are_instructions(self):
        md = blueprint.render(plan_for(brand_like(), 2))
        for line in re.findall(r"TODO\(agent\):([^\n|]*)", md):
            self.assertGreater(len(line.strip()), 10, line)

    def test_deterministic(self):
        data = brand_like()
        first = run(data, "--goal", GOAL, "--target", "4")
        self.assertEqual(first, run(copy.deepcopy(data), "--goal", GOAL, "--target", "4"))
        j1 = run(data, "--goal", GOAL, "--json")
        self.assertEqual(j1, run(data, "--goal", GOAL, "--json"))

    def test_json_matches_markdown(self):
        data = brand_like()
        code, out = run(data, "--goal", GOAL, "--target", "3", "--json")
        self.assertEqual(code, 0)
        plan = json.loads(out)
        self.assertEqual(len(plan["milestones"]), 3)
        self.assertEqual(plan["goal"]["words"], GOAL)
        self.assertEqual(blueprint.render(plan), run(data, "--goal", GOAL, "--target", "3")[1])

    def test_invalid_assessment_is_refused(self):
        data = brand_like()
        del data["change_kinds"]
        code, out = run(data, "--goal", GOAL)
        self.assertEqual(code, 2)
        self.assertIn("VALIDATION FAILED", out)

    def test_design_basis_says_designed_for(self):
        data = brand_like()
        data["basis"] = "design"
        md = blueprint.render(plan_for(data, 2))
        self.assertIn("Designed for Level 0", md)
        self.assertNotIn("Built to Level", md)


@unittest.skipUnless(os.path.exists(EXAMPLE), "Brand AI Apps example assessment not available")
class BrandExampleTests(unittest.TestCase):
    def test_example_produces_a_valid_skeleton(self):
        code, md = run(EXAMPLE, "--goal", GOAL)
        self.assertEqual(code, 0, md)
        self.assertEqual(re.findall(score.ID, reader_text(md)), [])
        self.assertIn("## Milestone 1: Level 1, Configurable", md)
        self.assertIn("## Milestone 2: Level 2, Assisted", md)
        m1 = md.split("## Milestone 1")[1].split("## Milestone 2")[0]
        self.assertIn("Products and prices the assistant shows", m1.split("#### Why")[0])
        m2 = md.split("## Milestone 2")[1]
        self.assertIn("`DEL-04`", m2)
        self.assertIn("`LRN-05`", m2)
        code, out = run(EXAMPLE, "--goal", GOAL, "--json")
        plan = json.loads(out)
        self.assertEqual([m["level_after"] for m in plan["milestones"]], [1, 2])


if __name__ == "__main__":
    unittest.main()
