#!/usr/bin/env python3
"""Print the skeleton of an EVOLVE blueprint (v0.7, spec section 9).

Usage:
  blueprint.py ASSESSMENT.json --goal "<owner's goal>" [--target LEVEL]
               [--route overlay|incremental|re-platform] [--json]

The skeleton follows references/blueprint-template.md. Every part that can be computed from the
assessment, the rubric's scoring model, references/remediation.md and references/plain-language.md is
filled in; everything else is marked `TODO(agent): ...` with an instruction. Reader text comes from
plain-language.md and never names a criterion code; codes appear only under "For engineers".

How milestones are built (deterministic, stdlib only, no network):
  * One milestone per level from today's headline level + 1 up to --target (default: two levels above
    today, at most 5).
  * A milestone holds every condition of its level that the headline loops do not meet yet, evaluated on
    the state after the earlier milestones. A condition with alternatives keeps one: the people path
    (kinds of change) first, then the alternative that needs the fewest new items, then the first in
    the model. The others are listed under "For engineers".
  * Every main kind of change below the milestone's reach (level 1 Self-serve, level 2 Drafted, ...) is a
    user-visible item, with the criteria the model's reach_needs require for that reach.
  * Value leads: user-visible items come first, gates after. Each criterion is classified in VISIBILITY
    below. Critical controls are level-3 conditions, so they join the first milestone at level 3.
  * Size: the largest remediation size among the milestone's criteria (S < M < L).
  * Overlay route: a move is flagged as needing a design decision when its remediation text names one of
    OVERLAY_WORDS (a keyword rule: it can flag a move that only adds new storage beside the product).
"""

import argparse
import copy
import itertools
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score  # noqa: E402
from score import (ModelError, aggregate, checklist, load_remediation, load_rubric,  # noqa: E402
                   loop_levels, score_assessment, validate, Evaluator)

DEFAULT_PLAIN = os.path.join(HERE, "..", "references", "plain-language.md")
ROUTES = ("overlay", "incremental", "re-platform")
DEFAULT_ROUTE = "overlay"
SIZES = ("S", "M", "L")
TOP = 5
TODO = "TODO(agent): "
GAIN_TODO = TODO + "describe the gain a user can see; if there is none, mark this step as a gate."

# The stages whose AI-qualified reading says how much AI does the work. Raising one of them while the
# product has no AI features brings the AI Readiness checks into scope.
AI_STAGES = ("DEL-01", "DEL-04", "LRN-05", "LRN-06", "LRN-07", "EXP-05")

# Overlay keyword rule: a move whose text names any of these may change how existing data is stored.
OVERLAY_WORDS = ("migration", "table", "column", "DDL", "store", "storage", "index mapping", "data model",
                 "schema and data")


def _ids(cap, *ranges):
    out = []
    for item in ranges:
        lo, hi = item if isinstance(item, tuple) else (item, item)
        out += [f"{cap}-{n:02d}" for n in range(lo, hi + 1)]
    return out


# Every criterion is either user-visible (it gives the people using or running the product a gain they
# can see: kinds of change, intake, drafting, diagnosis, proposals, measurement, new offerings) or a gate
# (a check, safeguard or foundation that must hold before more autonomy, with no gain of its own).
VISIBILITY = {
    "user": (_ids("MAL", (1, 13), (15, 20)) + ["DEL-01", "DEL-04", "DEL-09", "DEL-10"]
             + _ids("LRN", (1, 7), (9, 10)) + ["GOV-02", "GOV-03", "GOV-06", "GOV-07"] + _ids("EXP", (2, 6))),
    "gate": (_ids("ARC", (1, 9)) + ["DEL-02", "DEL-03"] + _ids("DEL", (5, 8)) + ["DEL-11", "MAL-14", "LRN-08",
             "GOV-01", "GOV-04", "GOV-05"] + _ids("GOV", (8, 11)) + ["EXP-01"] + _ids("AIR", (1, 8))),
}
CLASS_OF = {cid: cls for cls, ids in VISIBILITY.items() for cid in ids}

# The eight building blocks of an evolution system. Internal grouping only (spec section 9, rule 11):
# shown under "For engineers", never in reader text.
BLOCKS = {
    "Definition model": _ids("MAL", (1, 5), (7, 10), 16) + ["ARC-01"] + _ids("EXP", (1, 3)),
    "Contracts and extensions": _ids("MAL", 6, (11, 15), (17, 20)) + ["DEL-02", "DEL-03"],
    "Change ledger": ["GOV-02"] + _ids("GOV", (5, 8)) + ["ARC-02", "ARC-09", "AIR-07"],
    "Sensing": _ids("LRN", (1, 4), (9, 10)) + ["EXP-04", "AIR-08"],
    "Evolution engine": ["DEL-01", "DEL-04"] + _ids("LRN", (5, 7)) + ["EXP-05", "AIR-05"],
    "Governed release": _ids("DEL", (5, 11)) + ["EXP-06", "AIR-06"],
    "Guardrails": ["GOV-01", "GOV-03", "GOV-04"] + _ids("GOV", (9, 11)) + ["LRN-08", "ARC-05", "AIR-04"],
    "Runtime foundation": ["ARC-03", "ARC-04"] + _ids("ARC", (6, 8)) + _ids("AIR", (1, 3)),
}
BLOCK_OF = {cid: block for block, ids in BLOCKS.items() for cid in ids}

ROUTE_TEXT = {
    "overlay": "The work is built beside the product and joined at its existing extension points. Existing "
               "stored data and core logic stay as they are; any step that would change how existing data is "
               "stored is flagged for a decision first.",
    "incremental": "The product's core is changed part by part. Existing data is moved over safely in steps, "
                   "and interfaces other software uses keep working.",
    "re-platform": "A new core is built and the existing data is moved onto it. This is the largest route; use "
                   "it only when the other routes cannot reach the goal.",
}
SCOPE_TEXT = ("This plan does not redesign the product's journeys or screens. It lets users' requests and the "
              "product's own data drive change, with people deciding what ships.")
CONFIRM_TEXT = ("A level counts only when a new assessment, made without sight of this blueprint, finds the "
                "evidence, and the level's challenge passes on the running product. A pull request, a prompt "
                "or this plan never changes a level.")


# ---------------------------------------------------------------- plain language

def load_plain(path):
    """plain-language.md as {section: {key: {field: text}}}."""
    out, section, key = {}, None, None
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if line.startswith("## "):
                section, key = line[3:].strip(), None
                out.setdefault(section, {})
            elif line.startswith("### ") and section:
                key = line[4:].strip()
                out[section][key] = {}
            elif key and re.match(r"^[A-Z][a-z]+: ", line):
                field, text = line.split(": ", 1)
                out[section][key][field] = text.strip()
    return out


def check_plain(plain, order, model):
    """Names of the entries the blueprint needs that plain-language.md lacks."""
    missing = []
    need = [("Criteria", c, ("Name", "Question", "Gap")) for c in order]
    need += [("Levels", f"L{n}", ("Name", "Product", "People")) for n in range(len(model["levels"]))]
    need += [("Loops", l, ("Name",)) for l in model["loops"]]
    need += [("Reach", str(n), ("Name", "Meaning")) for n in range(len(model["reach"]))]
    need += [("Recursion", str(n), ("Name", "Meaning")) for n in range(len(model["recursion"]))]
    need += [("Controls", c["control"], ("Name", "Why")) for c in model["conditions"]["3"] if c.get("control")]
    need += [("Scope facts", f, ("Name",)) for f in model["scope_facts"]]
    for gate in model.get("ai_view", {}).get("gates", []):
        need.append(("AI readiness", gate["gate"], ("Name",)))
    for section, key, fields in need:
        entry = plain.get(section, {}).get(key, {})
        missing += [f"{section} {key} {f}" for f in fields if not entry.get(f)]
    return missing


# ---------------------------------------------------------------- planning

def _alternatives(cond, loop, model, facts):
    """A condition as alternatives, each a list of atoms: ("c", id, min) or ("kinds", reach)."""
    if "c" in cond:
        return [[("c", cond["c"], cond["min"])]]
    if "path" in cond:
        alts = []
        for alt in model["build_paths"][loop][cond["path"]]:
            if "kinds" in alt:
                alts.append([("kinds", 1)])
            elif "cap" in alt:
                alts.append([("c", c, cond["min"]) for ids in model["areas"][alt["cap"]].values() for c in ids])
            else:
                atoms = [("c", alt["c"], cond["min"])]
                if "with" in alt:
                    atoms.append(("c", alt["with"]["c"], alt["with"]["min"]))
                alts.append(atoms)
        return alts
    if "rollback" in cond:
        return [[("c", r["c"], cond["rollback"]) for r in model["rollback"]
                 if not r.get("when") or facts.get(r["when"]) is True]]
    if "every" in cond:
        return [[("c", c, cond["min"]) for ids in model["areas"][cond["every"]].values() for c in ids]]
    if "any" in cond:
        return [alt for sub in cond["any"] for alt in _alternatives(sub, loop, model, facts)]
    if "all" in cond:
        parts = [_alternatives(sub, loop, model, facts) for sub in cond["all"]]
        return [[a for alt in combo for a in alt] for combo in itertools.product(*parts)]
    raise ModelError(f"Unrecognised condition: {cond}")


class State:
    """The assessment as it would read after earlier milestones land: raised values and kinds."""

    def __init__(self, data, values, model, criteria):
        self.data, self.values, self.model, self.criteria = copy.deepcopy(data), dict(values), model, criteria

    def met(self, atom):
        if atom[0] == "kinds":
            return all(k.get("reach", 0) >= atom[1] for k in self.data["change_kinds"] if k.get("main") is True)
        if self.data["scores"][atom[1]]["status"] == "not_applicable" or self.values.get(atom[1]) is None:
            return True
        return self.values[atom[1]] >= atom[2]

    def evaluator(self):
        caps = aggregate(self.values, self.criteria, self.model)["capabilities"]
        return Evaluator(self.data, self.values, caps, self.model)

    def raise_to(self, atom):
        if atom[0] == "kinds":
            for k in self.data["change_kinds"]:
                if k.get("main") is True:
                    k["reach"] = max(k.get("reach", 0), atom[1])
        elif self.values.get(atom[1]) is not None:
            self.values[atom[1]] = max(self.values[atom[1]], atom[2])

    def levels(self):
        caps = aggregate(self.values, self.criteria, self.model)["capabilities"]
        return loop_levels(self.data, self.values, caps, self.model)


def _choose(alts, state, chosen):
    """The people path first, then the fewest new unmet atoms, then model order."""
    def key(indexed):
        i, alt = indexed
        new = [a for a in alt if not state.met(a) and a[:2] not in chosen]
        return (0 if any(a[0] == "kinds" for a in alt) else 1, len(new), i)
    return min(enumerate(alts), key=key)[1]


def _atom_key(atom):
    return atom[:2]


def plan_level(level, state, model, loops):
    """The unmet atoms for one level across the given loops, with where each comes from."""
    ev, facts = state.evaluator(), score.fact_values(state.data)
    items, alternatives = {}, []

    def add(atom, origin):
        k = _atom_key(atom)
        item = items.setdefault(k, {"atom": atom, "origins": []})
        if atom[0] == "c" and atom[2] > item["atom"][2]:
            item["atom"] = atom
        if atom[0] == "kinds" and atom[1] > item["atom"][1]:
            item["atom"] = atom
        if origin not in item["origins"]:
            item["origins"].append(origin)

    for loop in loops:
        for cond in model["conditions"].get(str(level), []):
            if cond.get("loop") not in (None, loop):
                continue
            ok, _, observed = ev.test(cond, loop)
            if ok or observed == "n/a":
                continue
            alts = _alternatives(cond, loop, model, facts)
            pick = _choose(alts, state, set(items))
            origin = {"loop": loop, "stage": cond["stage"], "part": cond["part"], "control": cond.get("control")}
            for atom in pick:
                if not state.met(atom):
                    add(atom, origin)
            others = [a for a in alts if a is not pick]
            if others:
                alternatives.append({"loop": loop, "stage": cond["stage"],
                                     "chosen": [list(a) for a in pick], "others": [[list(a) for a in alt]
                                                                                  for alt in others]})
    return items, alternatives


def build_plan(data, criteria, order, model, remediation, plain, result, goal, target, route):
    default = result["variants"]["default"]
    sal = default["sal"]
    today = sal["headline"]
    facts = score.fact_values(data)
    headline_loops = list(model["headline"])
    other_loops = [l for l in model["loops"] if l not in headline_loops]
    state = State(data, default["effective"], model, criteria)
    gate_status = {c["control"]: c["status"] for c in sal["controls"]}
    ai_in_scope = facts.get("ai_features") is True
    ai_scope_from = None
    optional_seen = set()
    levels_out = []
    control_of = {}
    for cond in model["conditions"]["3"]:
        if cond.get("control"):
            for atom_list in _alternatives(cond, None, model, facts):
                for atom in atom_list:
                    control_of[atom[1]] = cond["control"]
    ai_gates = []
    ai_view = result["variants"]["default"].get("ai_readiness") or {}
    for gate in ai_view.get("gates", []):
        if gate.get("status") == "fail":
            ai_gates.append(plain["AI readiness"][gate["gate"]]["Name"])

    for level in range(today + 1, TOP + 1):
        items, alternatives = plan_level(level, state, model, headline_loops)
        reach = min(level, len(model["reach"]) - 1)
        main_below = [k for k in state.data["change_kinds"] if k.get("main") is True and k.get("reach", 0) < reach]
        if main_below:
            items.setdefault(("kinds", reach), {"atom": ("kinds", reach), "origins": []})
            needs = model.get("reach_needs", {}).get(str(reach))
            if needs:
                pick = _choose(_alternatives(needs, None, model, facts), state, set(items))
                for atom in pick:
                    if not state.met(atom):
                        it = items.setdefault(_atom_key(atom), {"atom": atom, "origins": []})
                        if atom[0] == "c" and atom[2] > it["atom"][2]:
                            it["atom"] = atom
                        it["origins"].append({"loop": None, "stage": "Kinds of change", "part": "reach",
                                              "control": None, "reach": reach})
        # The third loop is optional: list its unmet atoms at this level and below, once.
        optional = []
        for loop in other_loops:
            for lvl in range(1, level + 1):
                opt, _ = plan_level(lvl, state, model, [loop])
                for k, it in sorted(opt.items(), key=lambda kv: _sort_key(kv[1]["atom"], order)):
                    seen = (k, it["atom"][-1])
                    if k in items or seen in optional_seen or it["atom"][0] == "kinds":
                        continue
                    optional_seen.add(seen)
                    optional.append(_criterion_item(it["atom"], it["origins"], data, criteria, remediation,
                                                    plain, model, default, route, control_of, optional=True))
        kinds_before = {k["id"]: k.get("reach", 0) for k in state.data["change_kinds"]}
        for it in items.values():
            state.raise_to(it["atom"])
        after = state.levels()
        built = []
        for k, it in sorted(items.items(), key=lambda kv: _sort_key(kv[1]["atom"], order)):
            if it["atom"][0] == "kinds":
                built.append(_kinds_item(it["atom"][1], data, kinds_before, plain, model))
            else:
                built.append(_criterion_item(it["atom"], it["origins"], data, criteria, remediation, plain,
                                             model, default, route, control_of))
        user = [i for i in built if i["class"] == "user"]
        gates = [i for i in built if i["class"] == "gate"]
        sizes = [i["size"] for i in built if i.get("size") in SIZES]
        size = max(sizes, key=SIZES.index) if sizes else None
        ai_raised = [i for i in built if i.get("id") in AI_STAGES]
        risks = []
        if ai_raised:
            if not ai_in_scope:
                ai_in_scope, ai_scope_from = True, level
                checks = [plain["Criteria"][c]["Name"] for c in order if criteria[c]["ai_check"]]
                risks.append("Brings the AI Readiness checks into scope: the product gains AI features, so "
                             "these checks start to apply: " + "; ".join(checks) + ".")
            elif ai_scope_from and ai_scope_from < level:
                risks.append(f"Gives AI a larger part; the AI Readiness checks are in scope from milestone "
                             f"{ai_scope_from - today}.")
            else:
                text = "The product already has AI features, and this milestone gives AI a larger part."
                if ai_gates:
                    text += " These AI safety gates do not pass yet: " + "; ".join(ai_gates) + "."
                risks.append(text)
            risks.append(TODO + "privacy: say which product data the AI will read, whether it includes "
                         "personal data, where it is sent, and how long it is kept.")
            risks.append(TODO + "cost: estimate what the AI costs per change and per month, who pays, and the "
                         "spending limit that stops it.")
            if facts.get("agent_mutations") is not True:
                risks.append("If the product's own AI will change its settings, rules or data, then "
                             f"\"{plain['Scope facts']['agent_mutations']['Name']}\" becomes true, and "
                             f"\"{plain['Controls']['Bounded self-change']['Name']}\" applies from Level 3.")
        if level >= 4 and facts.get("evolution_auto_apply") is not True:
            risks.append(f"From this milestone \"{plain['Scope facts']['evolution_auto_apply']['Name']}\" "
                         f"becomes true, which brings \"{plain['Criteria']['GOV-10']['Name']}\" and "
                         f"\"{plain['Criteria']['GOV-11']['Name']}\" into scope.")
        for g in gates:
            why = plain["Controls"][g["control"]]["Why"] if g.get("control") else g["gap"]
            if g.get("control"):
                risks.append(f"Touches a safety gate: {plain['Controls'][g['control']]['Name']}. {why}")
            else:
                risks.append(f"Touches a gate: {g['name']}. {why}")
        flagged = [i for i in built if i.get("overlay_flag")]
        if flagged:
            risks.append(f"{len(flagged)} engineering step(s) may change how existing data is stored. Under the "
                         "overlay route each needs a design decision before work starts (see For engineers).")
        risks.append(TODO + "add the risks specific to this product, and what this milestone brings into scope.")
        level_name = model["levels"][level]
        moving = [k for i in user if i["type"] == "kinds" for k in i["kinds"]] or \
            [k for k in data["change_kinds"] if k.get("main") is True]
        whos = list(dict.fromkeys(k.get("who") for k in moving if k.get("who")))
        reach_name = model["reach"][reach]
        people = {
            "who_changes": ("; ".join(whos) or TODO + "name who needs to make these changes")
                           + f". At this level the reach is {reach_name}: "
                           + plain["Reach"][str(reach)]["Meaning"],
            "who_approves": TODO + ("name the role that approves each change before it reaches users."
                                    if level <= 3 else "name the role that approves changes outside the "
                                    "written rules, and who reviews the automatic decisions."),
            "who_sets_policy": (TODO + "name who writes and signs off the rules for what ships without a "
                                "person, and how often they are reviewed.") if level >= 4 else
                               "Not needed yet: nothing ships without a person before Level 4.",
            "roles": TODO + "say what changes in day-to-day roles (who stops doing what, who starts doing what).",
        }
        challenge = {l: model["challenges"][str(level)][l] for l in headline_loops}
        main_names = [k["name"] for k in data["change_kinds"] if k.get("main") is True]
        levels_out.append({
            "number": level - today, "level": level, "level_name": level_name,
            "title": f"Level {level}, {level_name}",
            "level_after": after["headline"], "level_after_name": after["headline_name"],
            "loops_after": {l: after["loops"][l]["level"] for l in model["loops"]},
            "why": plain["Levels"][f"L{level}"]["Product"],
            "what_changes_for_users": [_user_line(i) for i in user] or [GAIN_TODO],
            "gain_todo": None if user else GAIN_TODO,
            "user_items": user, "gate_items": gates, "alternatives": alternatives,
            "optional": optional,
            "check": challenge, "check_kinds": main_names if level == 1 else [],
            "size": size, "risks": risks, "people": people,
            "ai_stages_raised": [i["id"] for i in ai_raised],
        })

    milestones = [m for m in levels_out if m["level"] <= target]
    beyond = [m for m in levels_out if m["level"] > target]
    gates_table = []
    seen_controls = set()
    for m in milestones:
        for g in m["gate_items"]:
            gates_table.append({"name": plain["Controls"][g["control"]]["Name"] if g.get("control") else g["name"],
                                "why": plain["Controls"][g["control"]]["Why"] if g.get("control")
                                else g["gap"], "control": g.get("control"), "milestone": m["number"],
                                "level": m["level"], "id": g["id"]})
            if g.get("control"):
                seen_controls.add(g["control"])
    controls = []
    for c in sal["controls"]:
        first = next((m["number"] for m in milestones for g in m["gate_items"] if g.get("control") == c["control"]),
                     None)
        controls.append({"control": c["control"], "name": plain["Controls"][c["control"]]["Name"],
                         "why": plain["Controls"][c["control"]]["Why"], "status": c["status"],
                         "first_milestone": first})
    return milestones, beyond, gates_table, controls


def _sort_key(atom, order):
    if atom[0] == "kinds":
        return (0, 0, 0)
    return (1 if CLASS_OF[atom[1]] == "user" else 2, order.index(atom[1]), 0)


def _kinds_item(reach, data, before, plain, model):
    kinds = [k for k in data["change_kinds"] if k.get("main") is True and before.get(k["id"], 0) < reach]
    rest = [k for k in data["change_kinds"] if not k.get("main") and k.get("reach", 0) < reach]
    return {"type": "kinds", "class": "user", "reach": reach, "reach_name": model["reach"][reach],
            "meaning": plain["Reach"][str(reach)]["Meaning"],
            "kinds": [{"id": k["id"], "name": k["name"], "who": k.get("who"), "from": before.get(k["id"], 0),
                       "from_name": model["reach"][before.get(k["id"], 0)]} for k in kinds],
            "not_main": [{"id": k["id"], "name": k["name"], "reach": k.get("reach", 0)} for k in rest]}


def _overlay_words(text):
    return [w for w in OVERLAY_WORDS if re.search(r"\b" + re.escape(w), text, re.I)]


def _criterion_item(atom, origins, data, criteria, remediation, plain, model, default, route, control_of,
                    optional=False):
    cid, need = atom[1], atom[2]
    rem = remediation.get(cid, {})
    move = rem.get("to4" if need >= 4 else "to3", "")
    words = _overlay_words(" ".join([rem.get("to3", ""), rem.get("to4", "") if need >= 4 else ""]))
    control = next((o["control"] for o in origins if o.get("control")), None)
    entry = data["scores"][cid]
    item = {"type": "criterion", "id": cid, "class": CLASS_OF[cid], "block": BLOCK_OF[cid],
            "title": criteria[cid]["title"], "name": plain["Criteria"][cid]["Name"],
            "question": plain["Criteria"][cid]["Question"], "gap": plain["Criteria"][cid]["Gap"],
            "now": default["effective"].get(cid), "status": entry["status"], "needs": need,
            "confidence": entry.get("confidence"),
            "anchor": criteria[cid]["anchors"][need], "move": move, "size": rem.get("size") or None,
            "requires": rem.get("requires", []), "control": control,
            "origins": [{k: v for k, v in o.items() if v is not None} for o in origins],
            "depth_capped": cid in model["depth_capped"] and need >= 3,
            "inventory": (model["inventories"].get(cid) or []) if cid in model["inventories"] and need >= 3 else [],
            "overlay_flag": route == "overlay" and bool(words), "overlay_words": words if route == "overlay" else [],
            "optional": optional}
    return item


def _user_line(item):
    if item["type"] == "kinds":
        names = "; ".join(f"{k['name']} ({k['who']}, today {k['from_name']})" for k in item["kinds"])
        return f"Kinds of change that become {item['reach_name']}: {names}. {item['meaning']}"
    return f"{item['name']}. Today: {item['gap']}"


# ---------------------------------------------------------------- the skeleton

def build(data, criteria, order, model, remediation, plain, goal, target=None, route=DEFAULT_ROUTE):
    result = score_assessment(data, criteria, order, model)
    default = result["variants"]["default"]
    sal = default["sal"]
    today = sal["headline"]
    if today >= TOP:
        raise ValueError(f"The product is already at Level {TOP}; there is nothing to plan.")
    target = min(TOP, today + 2) if target is None else target
    if not today < target <= TOP:
        raise ValueError(f"--target must be above today's level ({today}) and at most {TOP}.")
    if route not in ROUTES:
        raise ValueError(f"--route must be one of {', '.join(ROUTES)}.")
    milestones, beyond, gates, controls = build_plan(data, criteria, order, model, remediation, plain, result,
                                                     goal, target, route)
    basis = result["basis"]
    kinds = [{"id": k["id"], "name": k["name"], "who": k.get("who"), "main": k.get("main") is True,
              "reach": k["reach"], "reach_name": model["reach"][k["reach"]],
              "meaning": plain["Reach"][str(k["reach"])]["Meaning"]} for k in data["change_kinds"]]
    proven = result["proven"]
    ev = Evaluator(data, default["effective"], default["capabilities"], model)
    working, holding = [], []
    for loop in model["headline"]:
        info = sal["loops"][loop]
        if info["level"] >= TOP:
            continue
        for cond in model["conditions"].get(str(info["level"] + 1), []):
            if cond.get("loop") not in (None, loop):
                continue
            ok, _, observed = ev.test(cond, loop)
            if observed == "n/a":
                continue
            for alt in _alternatives(cond, loop, model, score.fact_values(data))[:1] if ok else []:
                for atom in alt:
                    if atom[0] == "c":
                        name = plain["Criteria"][atom[1]]["Name"]
                        if name not in working:
                            working.append(name)
    for m in milestones[:1]:
        holding = [_user_line(i) if i["class"] == "user" else f"{i['name']}. Today: {i['gap']}"
                   for i in m["user_items"] + m["gate_items"]]
    recursion = result["recursion"]
    rec_score = recursion["score"]
    conf = result["confidence"]
    check = checklist(data, criteria, model, default, target)
    today_text = {
        "basis": basis,
        "claim": "Designed for" if basis == "design" else "Built to",
        "level": today, "level_name": sal["headline_name"],
        "level_text": plain["Levels"][f"L{today}"]["Product"],
        "people_text": plain["Levels"][f"L{today}"]["People"],
        "loops": [{"loop": l, "name": plain["Loops"][l]["Name"], "level": sal["loops"][l]["level"],
                   "level_name": sal["loops"][l]["name"]} for l in model["loops"]],
        "kinds": kinds, "kinds_text": result["kinds"]["text"],
        "proven": ("Not applicable: a design reading says what the product is designed for, not what it has "
                   "been seen to do." if basis == "design" else
                   "not evidenced. " + score.PROVEN_NOTE if proven["headline"] is None else
                   f"Proven at Level {proven['headline']} ({proven['headline_name']}): operating records show "
                   "real changes going through the loop at that level."),
        "recursion": None if rec_score is None else {
            "name": plain["Recursion"][str(rec_score)]["Name"], "meaning": plain["Recursion"][str(rec_score)]["Meaning"]},
        "working": working, "holding_back": holding,
    }
    goal_kinds = [k["name"] for k in data["change_kinds"]]
    plan = {
        "product": data.get("product"), "date": data.get("date"), "source": data.get("source"),
        "framework_version": model.get("version"), "route": route, "route_text": ROUTE_TEXT[route],
        "target": target, "target_name": model["levels"][target],
        "goal": {"words": goal,
                 "measure": TODO + "name the measure that shows progress toward this goal, with today's value "
                            "and where it comes from.",
                 "kinds": TODO + "name the kinds of change that serve this goal, from: " + "; ".join(goal_kinds)
                          + ". Add a kind the assessment missed only with evidence."},
        "paragraph": {"computed": _paragraph(today_text, target, model, milestones),
                      "todo": TODO + "write one paragraph a product owner can follow: what the product does, "
                              "what already works toward the goal, what is missing, and what this plan adds. "
                              "No codes, no jargon."},
        "scope": {"text": SCOPE_TEXT, "route": ROUTE_TEXT[route],
                  "todo": TODO + "say in this product's words what stays as it is (journeys, screens, data) "
                          "and what the plan adds."},
        "today": today_text,
        "destination": [{"level": n, "name": model["levels"][n], "people": plain["Levels"][f"L{n}"]["People"],
                         "today": n == today,
                         "story": TODO + "what happens at this stage, told through one example that serves the "
                                  "goal."} for n in range(today, TOP + 1)],
        "milestones": milestones,
        "gates": gates, "controls": controls,
        "beyond": [{"level": m["level"], "name": m["level_name"], "people": plain["Levels"][f"L{m['level']}"]["People"],
                    "challenge": model["challenges"][str(m["level"])]["request"],
                    "needs": [i["name"] for i in m["user_items"] if i["type"] == "criterion"]
                             + [f"Kinds of change become {i['reach_name']}" for i in m["user_items"]
                                if i["type"] == "kinds"] + [i["name"] for i in m["gate_items"]],
                    "example": TODO + "one example of this level for this product."} for m in beyond],
        "confirm": {"text": CONFIRM_TEXT,
                    "challenges": {l: model["challenges"][str(target)][l] for l in model["headline"]},
                    "met_today": {l: {"met": sum(i["met"] for i in check[l]["items"]),
                                      "total": len(check[l]["items"])} for l in model["headline"]},
                    "command": f"python3 skills/evolvable-software/scripts/score.py <assessment.json> "
                               f"--checklist {target}"},
        "notes": {"headline": score.result_headline(result, model),
                  "basis_note": score.DESIGN_NOTE if basis == "design" else None,
                  "confidence": conf["criteria"] if conf["recorded"] else None,
                  "check_first": [plain["Criteria"][c["id"]]["Name"] for c in conf["check_first"]],
                  "not_evidenced": [plain["Criteria"][c]["Name"] for c in order
                                    if data["scores"][c]["status"] == "not_evidenced"],
                  "todo": TODO + "say what was re-checked for this blueprint, what was carried forward, and any "
                          "reading you think is wrong."},
    }
    return plan


def _paragraph(today, target, model, milestones):
    loops = ", ".join(f"{l['name'].lower()} at Level {l['level']}" for l in today["loops"])
    return (f"{today['claim']} Level {today['level']} ({today['level_name']}): {today['level_text']} "
            f"Loops: {loops}. {today['kinds_text'].capitalize()}. This plan takes it to Level {target} "
            f"({model['levels'][target]}) in {len(milestones)} milestone{'s' if len(milestones) != 1 else ''}.")


# ---------------------------------------------------------------- markdown

def _cell(text):
    return re.sub(r"\s+", " ", str(text)).replace("|", "\\|")


def _size_text(m):
    kinds = [i for i in m["user_items"] if i["type"] == "kinds"]
    if not kinds:
        return m["size"] or TODO + "size this milestone (S, M or L)"
    extra = TODO + "size making " + "; ".join(k["name"] for i in kinds for k in i["kinds"]) + \
        f" {kinds[0]['reach_name']}, and keep the larger size"
    return f"{m['size']} or more ({extra})" if m["size"] else extra


def _engineer_lines(item, route):
    if item["type"] == "kinds":
        lines = [f"- `change_kinds` to reach {item['reach']} ({item['reach_name']}): "
                 + ", ".join(f"`{k['id']}` {k['from']} → {item['reach']}" for k in item["kinds"]) + "."]
        if item["reach"] == 1:
            lines.append("  - Evidence: a supported path in the running product, with no deploy, and undo. A "
                         "path with no undo is reach 0.")
        else:
            lines.append(f"  - Consistency check: reach {item['reach']} needs the criteria the model's "
                         f"`reach_needs` names (listed in this milestone when unmet).")
        if item["not_main"]:
            lines.append("  - Not required (not main): " + ", ".join(f"`{k['id']}` reach {k['reach']}"
                                                                   for k in item["not_main"]) + ".")
        return lines
    origins = "; ".join(
        f"{o['loop']} {o['stage']}" if o.get("loop") else f"{o['stage']} reach {o.get('reach')}"
        for o in item["origins"]) or "optional"
    now = "not evidenced (0)" if item["status"] == "not_evidenced" else item["now"]
    lines = [f"- `{item['id']}` {item['title']} ({item['class']}, block: {item['block']}) · now {now} → "
             f"{item['needs']} · for: {origins} · size {item['size'] or '–'} · requires: "
             f"{', '.join(item['requires']) or 'none'}" + (f" · critical control: {item['control']}"
                                                           if item.get("control") else "")
             + (f" · confidence {item['confidence']}" if item.get("confidence") else "")]
    lines.append(f"  - Move: {item['move'] or TODO + 'no remediation entry; plan the move from the rubric.'}")
    lines.append(f"  - The next assessment must find: {item['anchor']}")
    if item["depth_capped"]:
        lines.append("  - Depth cap: a 3 or 4 needs the `tested` facet (automated tests in scope).")
    if item["inventory"]:
        lines.append("  - Inventory: every surface at the target: " + ", ".join(item["inventory"]) + ".")
    if item["overlay_flag"]:
        lines.append("  - Overlay route: needs a design decision; the move mentions "
                     + ", ".join(f"\"{w}\"" for w in item["overlay_words"])
                     + ". Find a variant that adds new parts beside the product, or choose the incremental "
                       "route for this step.")
    return lines


def render(plan):
    L = []
    add = L.append
    t = plan["today"]
    add(f"# {plan['product']}: evolution blueprint")
    add("")
    add(f"EVOLVE {plan['framework_version']} blueprint skeleton, from the assessment of {plan['date']} "
        f"({plan['source']}). Route: {plan['route']}. Target: Level {plan['target']} ({plan['target_name']}). "
        "Advice only: it never changes a score. Replace every `TODO(agent)` line, then delete this sentence.")
    add("")
    add("## Goal")
    add("")
    add(f"- **In the owner's words:** {plan['goal']['words']}")
    add(f"- **Measure that shows progress:** {plan['goal']['measure']}")
    add(f"- **Kinds of change that serve it:** {plan['goal']['kinds']}")
    add("")
    add("## In one paragraph")
    add("")
    add(plan["paragraph"]["computed"])
    add("")
    add(plan["paragraph"]["todo"])
    add("")
    add("## What this does and does not change")
    add("")
    add(f"{plan['scope']['text']} {plan['scope']['route']}")
    add("")
    add(plan["scope"]["todo"])
    add("")
    add("## Where it stands today")
    add("")
    add(f"**{t['claim']} Level {t['level']} ({t['level_name']}).** {t['level_text']} For the people using it: "
        f"{t['people_text']}")
    add("")
    for l in t["loops"]:
        add(f"- {l['name']}: Level {l['level']} ({l['level_name']})")
    add("")
    add(f"**Kinds of change.** {t['kinds_text'].capitalize()}.")
    add("")
    add("| Kind of change | Who makes it | Main | How far it has come |")
    add("|---|---|---|---|")
    for k in t["kinds"]:
        add(f"| {_cell(k['name'])} | {_cell(k['who'])} | {'yes' if k['main'] else 'no'} | "
            f"{k['reach_name']}: {_cell(k['meaning'])} |")
    add("")
    add(f"**Designed, built and proven.** {t['claim']} Level {t['level']} ({t['level_name']}). "
        f"Proven: {t['proven']}")
    if t["recursion"]:
        add("")
        add(f"**Do its checks improve?** {t['recursion']['name']}: {t['recursion']['meaning']}")
    if t["working"]:
        add("")
        add("**Already in place for the next level:** " + "; ".join(t["working"]) + ".")
    if t["holding_back"]:
        add("")
        add("**What holds it back:**")
        add("")
        for line in t["holding_back"]:
            add(f"- {line}")
    add("")
    add(TODO + "describe in the product's own words what works today for the people using and running it.")
    add("")
    add("## The destination")
    add("")
    add("| Stage | What it means for people | For this product |")
    add("|---|---|---|")
    for d in plan["destination"]:
        label = f"Today: Level {d['level']} ({d['name']})" if d["today"] else f"Level {d['level']} ({d['name']})"
        add(f"| {label} | {_cell(d['people'])} | {d['story']} |")
    add("")
    add("## The progress map")
    add("")
    add("| # | Milestone | What users get | Level after it | Check | Size | Measure it should move |")
    add("|---|---|---|---|---|---|---|")
    for m in plan["milestones"]:
        gets = "; ".join(
            (f"{', '.join(k['name'] for k in i['kinds'])} become {i['reach_name']}" if i["type"] == "kinds"
             else i["name"]) for i in m["user_items"]) or "Gate only"
        add(f"| {m['number']} | {m['title']} | {_cell(gets)} | Level {m['level_after']} ({m['level_after_name']}) "
            f"| The Level {m['level']} check in milestone {m['number']} | {_cell(_size_text(m))} | "
            f"{TODO}the measure from the goal this moves |")
    add("")
    for m in plan["milestones"]:
        add(f"## Milestone {m['number']}: {m['title']}")
        add("")
        add(TODO + "give this milestone a short name that says what users gain.")
        add("")
        add("#### What changes for users")
        add("")
        for line in m["what_changes_for_users"]:
            add(f"- {line}" if not line.startswith(TODO) else line)
        if not m["gain_todo"]:
            add("")
            add(TODO + "rewrite these as the gain a user of this product will see, with one concrete example.")
        add("")
        add("#### Why this moves the product up")
        add("")
        add(f"At Level {m['level']} ({m['level_name']}): {m['why']} After this milestone the product reads Level "
            f"{m['level_after']} ({m['level_after_name']}), if every step lands and a fresh assessment finds it.")
        add("")
        add("#### The check")
        add("")
        for loop, text in m["check"].items():
            add(f"- **{plan['loop_names'][loop]}.** {text}")
        if m["check_kinds"]:
            add(f"- **Main kinds of change to try:** {'; '.join(m['check_kinds'])}.")
        add("")
        add(TODO + "turn this into steps a person can follow on the live product or its demo, naming the screens "
            "and the data to use.")
        add("")
        add("#### Risks and what it brings into scope")
        add("")
        for r in m["risks"]:
            add(r if r.startswith(TODO) else f"- {r}")
        add("")
        add("#### People")
        add("")
        p = m["people"]
        add(f"- **Who makes the change:** {p['who_changes']}")
        add(f"- **Who approves:** {p['who_approves']}")
        add(f"- **Who sets the rules for what ships without a person:** {p['who_sets_policy']}")
        add(f"- **What changes in roles:** {p['roles']}")
        add("")
        add("#### For engineers")
        add("")
        for i in m["user_items"] + m["gate_items"]:
            L.extend(_engineer_lines(i, plan["route"]))
        for a in m["alternatives"]:
            fmt = lambda alt: " and ".join(f"{x[1]} ≥ {x[2]}" if x[0] == "c" else f"main kinds reach ≥ {x[1]}"
                                           for x in alt)
            add(f"- Alternative for {a['loop']} {a['stage']}: chosen {fmt(a['chosen'])}; also possible: "
                + "; or ".join(fmt(o) for o in a["others"]) + ".")
        if m["optional"]:
            add("- Optional, for the third loop (not in the headline level):")
            for i in m["optional"]:
                add(f"  - `{i['id']}` {i['title']} · now {i['now']} → {i['needs']} · size {i['size'] or '–'}: "
                    f"{i['move']}")
        if plan["route"] == "overlay":
            add("- Overlay rule: a move is flagged when its remediation text mentions "
                + ", ".join(f"\"{w}\"" for w in OVERLAY_WORDS) + ". It is a keyword rule and can flag a move "
                "that only adds new storage beside the product; decide each flag.")
        add(f"- Evidence checklist: `score.py <assessment.json> --checklist {m['level']}`.")
        add(TODO + "name the files, tables, services and patterns from the assessment's evidence that each step "
            "builds on, and what must stay untouched.")
        add("")
        add("#### Prompt for a coding agent")
        add("")
        add("```text")
        add(TODO + "write a self-contained prompt for Claude Code or Codex, run in this product's repository. It "
            "must name the files and patterns to follow, deliver the changes below, say what must not change, "
            "add the automated test that performs the check, and finish by listing the files changed and "
            "showing the tests passing.")
        add("")
        add("Changes to deliver:")
        for i in m["user_items"] + m["gate_items"]:
            if i["type"] == "kinds":
                add(f"- Make these kinds of change {i['reach_name']}: "
                    + "; ".join(k["name"] for k in i["kinds"]) + f". {i['meaning']}")
            else:
                add(f"- {i['name']}: {i['question']}")
        add(f"Route: {plan['route']}. {plan['route_text']}")
        add("```")
        add("")
        add("#### Done when")
        add("")
        for i in m["user_items"] + m["gate_items"]:
            if i["type"] == "kinds":
                for k in i["kinds"]:
                    add(f"- [ ] {k['name']} is {i['reach_name']} for {k['who']}: {i['meaning']}")
            else:
                add(f"- [ ] Yes to: {i['question']}")
        add(f"- [ ] The check above passes on the running product.")
        add(f"- [ ] An automated test performs the check. {TODO}name the test file and test, and make it run in CI.")
        add(f"- [ ] A fresh assessment, made without sight of this blueprint, finds the evidence listed under For "
            f"engineers, and the scorer reports Level {m['level']}.")
        add("")
    add("## Safety gates")
    add("")
    add("Each gate is attached to the first milestone that needs it.")
    add("")
    if plan["gates"]:
        add("| Gate | Why it matters | Needed from |")
        add("|---|---|---|")
        for g in plan["gates"]:
            kind = "Safety gate: " if g["control"] else ""
            add(f"| {kind}{_cell(g['name'])} | {_cell(g['why'])} | Milestone {g['milestone']} (Level {g['level']}) |")
    else:
        add("No milestone in this plan needs a gate.")
    add("")
    add("The safety gates every product needs from Level 3:")
    add("")
    for c in plan["controls"]:
        if c["status"] == "n/a":
            state = "does not apply to this product"
        elif c["status"] == "pass":
            state = "passes today"
        elif c["first_milestone"]:
            state = f"does not pass yet; milestone {c['first_milestone']}"
        else:
            state = "does not pass yet; needed at Level 3, after this plan"
        add(f"- **{c['name']}:** {state}. {c['why']}")
    add("")
    add("## Beyond")
    add("")
    if not plan["beyond"]:
        add("This plan reaches Level 5. Nothing lies beyond it.")
        add("")
    for b in plan["beyond"]:
        add(f"### Level {b['level']}: {b['name']}")
        add("")
        add(f"{b['people']} The check: {b['challenge']}")
        add("")
        if b["needs"]:
            add("It needs: " + "; ".join(b["needs"]) + ".")
            add("")
        add(b["example"])
        add("")
    add("## How the level will be confirmed")
    add("")
    add(plan["confirm"]["text"])
    add("")
    for loop, text in plan["confirm"]["challenges"].items():
        met = plan["confirm"]["met_today"][loop]
        add(f"- **{plan['loop_names'][loop]}, Level {plan['target']}.** {text} Today {met['met']} of "
            f"{met['total']} items the assessment must find are in place.")
    add("")
    add(f"The full list for engineers: `{plan['confirm']['command']}`.")
    add("")
    add("## Notes on the assessment")
    add("")
    n = plan["notes"]
    add(f"- Assessed {plan['date']} at {plan['source']}.")
    add(f"- Scorer headline: {n['headline']}.")
    if n["basis_note"]:
        add(f"- {n['basis_note']}")
    if n["confidence"]:
        c = n["confidence"]
        add(f"- How sure the reading is: {c['high']} high, {c['medium']} medium, {c['low']} low.")
    else:
        add("- The assessment records no confidence for its readings.")
    if n["check_first"]:
        add("- Check these first (low confidence, and they hold back a level or a safety gate): "
            + "; ".join(n["check_first"]) + ".")
    if n["not_evidenced"]:
        add("- Not evidenced, so counted as missing: " + "; ".join(n["not_evidenced"]) + ".")
    add("")
    add(n["todo"])
    return "\n".join(L).rstrip() + "\n"


# ---------------------------------------------------------------- entry point

def make(path, goal, target=None, route=DEFAULT_ROUTE, rubric=score.DEFAULT_RUBRIC,
         remediation_path=score.DEFAULT_REMEDIATION, plain_path=DEFAULT_PLAIN):
    """(plan, errors) for an assessment file."""
    criteria, order, model = load_rubric(rubric)
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    errors = validate(data, criteria, order, model)
    if errors:
        return None, errors
    plain = load_plain(plain_path)
    missing = check_plain(plain, order, model)
    if missing:
        return None, ["plain-language.md lacks: " + ", ".join(missing)]
    remediation = load_remediation(remediation_path, criteria)
    plan = build(data, criteria, order, model, remediation, plain, goal, target, route)
    plan["loop_names"] = {l: plain["Loops"][l]["Name"] for l in model["loops"]}
    return plan, []


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print the skeleton of an EVOLVE blueprint.")
    parser.add_argument("assessment")
    parser.add_argument("--goal", required=True, help="the owner's goal, in their own words")
    parser.add_argument("--target", type=int, choices=range(1, TOP + 1), metavar="LEVEL",
                        help="the level to plan to (default: two levels above today, at most 5)")
    parser.add_argument("--route", choices=ROUTES, default=DEFAULT_ROUTE)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--rubric", default=score.DEFAULT_RUBRIC)
    parser.add_argument("--remediation", default=score.DEFAULT_REMEDIATION)
    parser.add_argument("--plain", default=DEFAULT_PLAIN)
    args = parser.parse_args(argv)
    if not args.goal.strip():
        print("--goal needs the owner's goal in their own words.")
        return 2
    try:
        plan, errors = make(args.assessment, args.goal.strip(), args.target, args.route, args.rubric,
                            args.remediation, args.plain)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read {args.assessment}: {exc}")
        return 2
    except ValueError as exc:
        print(str(exc))
        return 2
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(" -", error)
        return 2
    if args.json:
        print(json.dumps(plan, indent=2, ensure_ascii=False, default=list))
    else:
        print(render(plan), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
