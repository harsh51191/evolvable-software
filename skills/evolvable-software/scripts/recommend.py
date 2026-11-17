#!/usr/bin/env python3
"""Print the three next moves for a product, from its EVOLVE assessment.

A blueprint lays out the road to a target level. This answers the question an owner asks first: what
should we do next? It always gives exactly three moves, in this order:

1. For the people running the product: the main kind of change that is furthest behind, moved one step
   (engineers only to self-serve with undo; self-serve to drafted; drafted to carried). This is the move
   users notice, and under the v0.7 rules no AI lane lifts a product until it serves a main kind.
2. For the loop: the one stage that most holds the product's request or fix loop below the next level
   (turning requests into plans, noticing problems, explaining them, proposing fixes, and so on).
3. For safety: the one control the next level needs, or, when the next level needs none, the critical
   control nearest to passing, so the safety net is ready before autonomy grows.

Each move names what users get, the evidence it starts from, a measure of real-world effect to track,
a "done when" list and a prompt for a coding agent. Every move must ship on in the standard installation:
a feature behind an optional setting counts only toward the opt-in reading, never the level.

The choice is mechanical and documented here, so two people running it on the same assessment get the
same three moves. It never changes a score. Wording comes from references/plain-language.md.

Usage:
    recommend.py assessment.json [--json]
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import score  # noqa: E402
from blueprint import load_plain  # noqa: E402

DEFAULT_PLAIN = os.path.join(HERE, "..", "references", "plain-language.md")
DEFAULT_REMEDIATION = os.path.join(HERE, "..", "references", "remediation.md")

# Order in which the loop move is chosen: what users see first, then the delivery spine, then the rest.
PART_ORDER = {"stages": 0, "spine": 1, "architecture": 2, "governance": 3}
# Critical controls nearest to users first: undo is what people feel when a change goes wrong.
CONTROL_ORDER = ["GOV-05", "DEL-11", "ARC-09", "GOV-04", "ARC-02", "GOV-10", "ARC-05"]
CONTROL_OF = {"GOV-05": "Definition rollback", "DEL-11": "Release rollback", "ARC-02": "Safe migrations",
              "ARC-09": "Tested backup and restore", "ARC-05": "Tenant isolation",
              "GOV-04": "Security as infrastructure", "GOV-10": "Bounded self-change"}

# How to tell, in real use, that a move worked. A level is a reading; these are the effects it should have.
MEASURES = {
    "DEL-01": "Share of requests captured as a plan a person confirmed, and days from request to release.",
    "DEL-04": "Share of changes that start from a product draft, and how much people edit the drafts.",
    "DEL-05": "Share of changes stopped by an automatic check before release, and incidents that got past them.",
    "DEL-06": "Time to answer \"what exactly is running?\" during an incident.",
    "DEL-09": "Share of changes released to a small group first, and how many were stopped there.",
    "DEL-10": "Time from spotting a bad change to switching it off.",
    "DEL-11": "Time to go back to the previous release, and whether data still works after it.",
    "LRN-03": "Share of user-visible failures the product records with the part involved, and time to notice them.",
    "LRN-05": "Time from a problem being recorded to its cause being known.",
    "LRN-06": "Share of fixes that started from a product proposal, and how many of those proposals were accepted.",
    "LRN-07": "Candidate changes the product raised from its own use per month, and how many shipped.",
    "LRN-09": "Share of changes measured against how things were before, and how many were reversed on results.",
    "EXP-04": "Unmet needs the product recorded per month (failed searches, requests it could not handle).",
    "EXP-05": "Proposals for new capabilities with evidence, and how many were tried.",
    "GOV-04": "Share of changes scanned before merge, and security findings caught before release.",
    "GOV-05": "Share of change types with one-step undo, and time to reverse a bad change.",
    "GOV-07": "Share of changes routed by a written rule rather than case by case.",
    "GOV-10": "Self-made changes blocked by a limit, and how far any bad one spread.",
    "ARC-02": "Storage changes that needed downtime or lost data (should be none).",
    "ARC-05": "Cross-customer data access found in tests or incidents (should be none).",
    "ARC-09": "A restore drill passing on a schedule, and the time it takes.",
}


def _cid_needs(cond, ev, loop, model, facts):
    """Atomic (criterion, minimum, observed) needs a failing condition contains; Build paths excluded."""
    if "path" in cond or "any" in cond:
        return []
    when = cond.get("when")
    if when and not any(facts.get(f) is True for f in ([when] if isinstance(when, str) else when)):
        return []
    if "c" in cond:
        ok, value = ev._crit(cond["c"], cond["min"])
        return [] if ok else [(cond["c"], cond["min"], value)]
    if "rollback" in cond:
        out = []
        for item in model["rollback"]:
            if item.get("when") and facts.get(item["when"]) is not True:
                continue
            ok, value = ev._crit(item["c"], cond["rollback"])
            if not ok:
                out.append((item["c"], cond["rollback"], value))
        return out
    if "every" in cond:
        out = []
        for ids in model["areas"][cond["every"]].values():
            for cid in ids:
                ok, value = ev._crit(cid, cond["min"])
                if not ok:
                    out.append((cid, cond["min"], value))
        return out
    if "all" in cond:
        return [n for sub in cond["all"] for n in _cid_needs(sub, ev, loop, model, facts)]
    return []


def _failing(level, loops, ev, model, facts):
    """Failing atomic needs at a level, across the given loops, with their part and stage."""
    out = []
    for cond in model["conditions"].get(str(level), []):
        for loop in loops:
            if cond.get("loop") not in (None, loop):
                continue
            ok, _, _ = ev.test(cond, loop)
            if ok:
                continue
            for cid, minimum, value in _cid_needs(cond, ev, loop, model, facts):
                out.append({"c": cid, "min": minimum, "value": value, "part": cond["part"],
                            "stage": cond["stage"], "loop": loop, "control": cond.get("control")})
    return out


def _gap(need):
    value = need["value"] if isinstance(need["value"], int) else 0
    return need["min"] - value


def _evidence(data, cid, limit=420):
    entry = data["scores"].get(cid, {})
    text = entry.get("evidence") or entry.get("rationale") or ""
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + " …"


def _criterion_move(kind, need, data, criteria, plain, remediation, model):
    cid = need["c"]
    entry = plain["Criteria"][cid]
    target = need["min"]
    anchor = criteria[cid]["anchors"][target]
    fix = (remediation.get(cid) or {}).get("to3") if target >= 3 else None
    control = CONTROL_OF.get(cid)
    title = plain["Controls"][control]["Name"] if control and kind == "safety" else entry["Name"]
    why = plain["Controls"][control]["Why"] if control else entry["Gap"]
    question = entry["Question"]
    if target >= 3:
        gain = "It can answer yes to: " + question[0].lower() + question[1:]
        shown = f"In the running product: {question[0].lower() + question[1:]} Yes, shown on a demo or test installation."
    else:
        # Below 3 the rubric asks for a first step, not the full answer; say exactly that step.
        gain = f"A first step towards \"{entry['Name'].lower()}\": {anchor[0].lower() + anchor[1:]}"
        shown = f"Shown on a demo or test installation, or in the product's own documentation: {anchor}"
    return {
        "kind": kind, "criterion": cid, "gain": gain, "from": need["value"], "to": target, "title": title,
        "today": entry["Gap"], "why": why, "question": entry["Question"],
        "evidence": _evidence(data, cid), "target_anchor": anchor, "how": fix,
        "loop": need.get("loop"), "stage": need.get("stage"), "control": control,
        "measure": MEASURES.get(cid, f"The gap closes: \"{entry['Gap']}\" no longer holds in a fresh assessment."),
        "done_when": [
            shown,
            f"A fresh assessment scores {cid} at {target} or more: \"{anchor}\"",
            "It is on in the standard installation, with no optional setting or extra licence needed.",
            "An automated test performs the check and runs in CI.",
        ],
    }


def _people_move(data, sal, plain, model):
    """The main kind furthest behind, moved one reach step; None when no main kind can move cheaply."""
    kinds = data.get("change_kinds") or []
    main = [k for k in kinds if k.get("main") is True]
    if not main:
        return None
    lowest = min(k["reach"] for k in main)
    level = min(sal["loops"][l]["level"] for l in model["headline"])
    nxt = min(level + 1, 5)
    ahead = False
    if lowest == 0:
        # Level 1 needs every main kind self-serve with undo.
        kind, target = next(k for k in main if k["reach"] == 0), 1
    elif max(k["reach"] for k in main) < 2:
        # The product build path needs a main kind it drafts; start with the first-listed main kind.
        kind, target = main[0], 2
    elif lowest < 2:
        # One main kind is drafted already; extend drafting to the next main kind still self-serve only.
        kind, target = next(k for k in main if k["reach"] == lowest), 2
    else:
        # Every main kind is drafted: carrying one end to end is the Level 3 build path.
        kind = max(main, key=lambda k: k["reach"])
        target = min(kind["reach"] + 1, 5)
        ahead = target > nxt
    others = [k["name"] for k in main if k is not kind and k["reach"] < target]
    reach = plain["Reach"]
    needs = {1: "a supported way for them to make it in the running product, and undo that restores the earlier behaviour",
             2: "the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it",
             3: "the product building, checking and releasing this change end to end (DEL-04 3), with a person approving",
             4: "a written policy under which it ships without a person and is undone automatically (GOV-07 3)",
             5: "the product choosing when to make it, within policy (LRN-07 3)"}[target]
    return {
        "kind": "people", "ahead": ahead, "change_kind": kind["id"], "name": kind["name"], "who": kind["who"],
        "from": kind["reach"], "to": target,
        "title": {1: f"Let {kind['who']} change \"{kind['name']}\" themselves, with undo",
                  2: f"Have the product draft \"{kind['name']}\" changes",
                  3: f"Have the product carry \"{kind['name']}\" changes end to end",
                  4: f"Let routine \"{kind['name']}\" changes ship under written rules",
                  5: f"Let the product choose when to change \"{kind['name']}\""}[target],
        "today": f"{reach[str(kind['reach'])]['Name']}. {reach[str(kind['reach'])]['Meaning']}",
        "gain": reach[str(target)]["Meaning"],
        "evidence": kind.get("evidence", ""), "needs": needs, "others": others,
        "measure": (f"Share of \"{kind['name']}\" changes made without an engineer, days from request to live, "
                    f"and engineer tickets for it per month." if target == 1 else
                    f"Share of \"{kind['name']}\" changes that start from the product's own draft or build, "
                    f"how much people edit them, and days from request to live."),
        "done_when": [
            f"{kind['who'][0].upper() + kind['who'][1:]} can do this in the running product: {needs}.",
            ("They make one such change and then undo it, and the earlier behaviour is back."
             if target == 1 else "A person can stop, edit or reject what the product prepared, and undo it after release."),
            "It is on in the standard installation, with no optional setting or extra licence needed.",
            f"A fresh assessment lists \"{kind['name']}\" at reach {target} ({reach[str(target)]['Name']}).",
            "An automated test performs the change and its undo, and runs in CI.",
        ],
    }


def _apply(data, move, model):
    """A copy of the assessment with one move landed, as a fresh assessment would find it."""
    import copy
    out = copy.deepcopy(data)

    def lift(cid, target):
        entry = out["scores"].get(cid)
        if not entry or entry.get("status") == "not_applicable":
            return
        old = entry.get("score") if entry.get("status") == "assessed" else 0
        if (old or 0) >= target:
            return
        entry.update(status="assessed", score=target, grade=entry.get("grade", "A") if entry.get("status") == "assessed" else "A")
        entry.setdefault("evidence", "planned")
        if target >= 3:
            entry["facets"] = {"implemented": True, "tested": True, "operated": False}
        if cid in model["inventories"]:
            surfaces = model["inventories"][cid] or ["surface"]
            entry["inventory"] = {s: max(target, (entry.get("inventory") or {}).get(s, 0)) for s in
                                  (entry.get("inventory") or {s: 0 for s in surfaces})}
        entry.pop("alt_score", None)
        if "ai" in entry and isinstance(entry["ai"], dict) and entry["ai"].get("status") == "assessed" \
                and cid in ("DEL-01", "DEL-04", "LRN-05", "LRN-06", "LRN-07", "LRN-08", "EXP-05"):
            pass

    if move["kind"] == "people":
        for kind in out["change_kinds"]:
            if kind["id"] == move["change_kind"]:
                kind["reach"] = move["to"]
        if move["to"] >= 2:
            lift("DEL-04", min(move["to"], 3))
        if move["to"] >= 4:
            lift("GOV-07", 3)
        if move["to"] >= 5:
            lift("LRN-07", 3)
    else:
        lift(move["criterion"], move["to"])
    return out


def _level_after(data, moves, criteria, order, model):
    landed = data
    for move in moves:
        landed = _apply(landed, move, model)
    errors = score.validate(landed, criteria, order, model)
    result = score.score_assessment(landed, criteria, order, model)
    sal = result["variants"]["default"]["sal"]
    level = min(sal["loops"][l]["level"] for l in model["headline"])
    return level, errors, sal


def Evaluator_for(data, variant, model):
    return score.Evaluator(data, variant["effective"], variant["capabilities"], model)


def _prompt(move, data):
    source = data.get("source", "the repository")
    lines = [f"You are working in {source}. Read the code before changing it.",
             f"Goal for users: {move['gain']}",
             f"Today: {move['today']}"]
    if move.get("evidence"):
        lines.append(f"Where it stands in the code (from the assessment): {move['evidence']}")
    if move["kind"] == "people":
        lines.append(f"Build {move['needs']}, for this kind of change: {move['name']} (made by {move['who']}).")
    else:
        lines.append(f"Raise this to: {move['target_anchor']}")
        if move.get("how"):
            lines.append(f"A known way to get there: {move['how']}")
    lines += ["Ship it on by default in the standard installation; do not hide it behind an optional setting.",
              "Change existing stored data only through the product's own migration path, and keep every change reversible.",
              "Done when:"] + [f"- {d}" for d in move["done_when"]] + [
              "Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong."]
    return "\n".join(lines)


def recommend(data, criteria, order, model, plain, remediation):
    result = score.score_assessment(data, criteria, order, model)
    default = result["variants"]["default"]
    sal = default["sal"]
    facts = score.fact_values(data)
    ev = score.Evaluator(data, default["effective"], default["capabilities"], model)
    level = min(sal["loops"][l]["level"] for l in model["headline"])
    nxt = min(level + 1, len(model["levels"]) - 1)
    headline_loops = [l for l in model["headline"] if sal["loops"][l]["level"] == level]

    moves = []
    people = _people_move(data, sal, plain, model)
    if people:
        moves.append(people)

    # Loop move: a stage need at the next level, never the Build path (move 1) or a safety control (move 3).
    needs = [n for n in _failing(nxt, headline_loops, ev, model, facts)
             if n["c"] not in CONTROL_OF and n["stage"] not in ("Roll back",)]
    needs.sort(key=lambda n: (PART_ORDER[n["part"]], _gap(n), model["headline"].index(n["loop"]), order.index(n["c"])))
    if not needs:  # nothing but Build and safety holds the next level; look one level further
        needs = [n for n in _failing(min(nxt + 1, 5), [l for l in model["headline"]], ev, model, facts)
                 if n["c"] not in CONTROL_OF and n["stage"] != "Roll back"]
        needs.sort(key=lambda n: (PART_ORDER[n["part"]], _gap(n), order.index(n["c"])))
    later = False
    if needs and needs[0]["min"] > nxt:
        later = True
    if needs:
        move = _criterion_move("loop", needs[0], data, criteria, plain, remediation, model)
        move["later"] = later
        moves.append(move)

    # Safety move: a control the next level needs; otherwise the Level 3 control nearest to passing.
    safety = [n for n in _failing(nxt, headline_loops, ev, model, facts) if n["c"] in CONTROL_OF]
    ahead = False
    if not safety:
        safety = [n for n in _failing(3, headline_loops, ev, model, facts) if n["c"] in CONTROL_OF]
        ahead = True
    seen, unique = set(), []
    for n in safety:
        if n["c"] not in seen:
            seen.add(n["c"])
            unique.append(n)
    unique.sort(key=lambda n: (_gap(n), CONTROL_ORDER.index(n["c"])))
    if unique:
        move = _criterion_move("safety", unique[0], data, criteria, plain, remediation, model)
        move["ahead"] = ahead
        move["also"] = [plain["Controls"][CONTROL_OF[n["c"]]]["Name"] for n in unique[1:]]
        moves.append(move)

    for move in moves:
        move["prompt"] = _prompt(move, data)
    for move in moves:
        move["level_alone"] = _level_after(data, [move], criteria, order, model)[0]
    after, after_errors, after_sal = _level_after(data, moves, criteria, order, model)
    # The rest of the way: keep landing the next need until the next level is reached.
    rest, landed = [], data
    for move in moves:
        landed = _apply(landed, move, model)
    for _ in range(25):
        res = score.score_assessment(landed, criteria, order, model)["variants"]["default"]
        lsal = res["sal"]
        if min(lsal["loops"][l]["level"] for l in model["headline"]) >= nxt:
            break
        lev = Evaluator_for(landed, res, model)
        pending = _failing(nxt, model["headline"], lev, model, score.fact_values(landed))
        pending.sort(key=lambda n: (PART_ORDER[n["part"]], order.index(n["c"])))
        if pending:
            step = _criterion_move("rest", pending[0], landed, criteria, plain, remediation, model)
        else:
            step = _people_move(landed, lsal, plain, model)
            if not step:
                break
        rest.append(step)
        landed = _apply(landed, step, model)
    still = []
    if after < nxt:
        for l in model["headline"]:
            if after_sal["loops"][l]["level"] == after:
                for b in after_sal["loops"][l]["blockers"]:
                    still.append(f"{b['stage']} ({b['needs']}, has {b['observed']})")
    return {"product": data.get("product"), "source": data.get("source"), "date": data.get("date"),
            "headline": score.result_headline(result, model), "level": level, "next": nxt,
            "level_name": model["levels"][level], "next_name": model["levels"][nxt],
            "kinds": result["kinds"], "moves": moves, "level_after": after, "still_needed": sorted(set(still)),
            "rest": [{"title": s["title"], "code": s.get("criterion") or s.get("change_kind"), "from": s["from"],
                      "to": s["to"]} for s in rest],
            "simulation_errors": after_errors}


def render(rec, plain):
    out = [f"# {rec['product']}: the next three moves", "",
           f"From the EVOLVE assessment of {rec['date']} ({rec['source']}). Advice only: it never changes a score. "
           "Each move must ship on in the standard installation, and counts only when a fresh assessment finds it.", "",
           f"**Today:** {rec['headline']}", "",
           f"**Next level:** {rec['next']}, {rec['next_name']}. {plain['Levels']['L' + str(rec['next'])]['Product']}", "",
           ]
    if rec["level_after"] >= rec["next"]:
        out += [f"**With all three moves the product reads Level {rec['level_after']}**, checked by re-running the scorer "
                "with each move landed.", ""]
    else:
        out += [f"**With all three moves the product still reads Level {rec['level_after']}.** The rest of the way to "
                f"Level {rec['next']}, in order: " + "; ".join(r["title"] for r in rec["rest"]) + ".", ""]
    out += ["| # | Move | What users get | Level with this move alone | Track in real use |", "|---|---|---|---:|---|"]
    labels = {"people": "For the people running it", "loop": "For the loop", "safety": "For safety"}
    for i, m in enumerate(rec["moves"], 1):
        gain = m["gain"]
        out.append(f"| {i} | **{m['title']}** ({labels[m['kind']]}) | {gain} | {m['level_alone']} | {m['measure']} |")
    for i, m in enumerate(rec["moves"], 1):
        out += ["", f"## {i}. {m['title']}", "", f"*{labels[m['kind']]}.*", ""]
        out.append(f"**Today.** {m['today']}")
        if m["kind"] == "people":
            out.append(f"\n**What users get.** {m['gain']} Made by: {m['who']}.")
            if m.get("ahead"):
                out.append(f"\nThe next level does not need this; it prepares the build path for Level {m['to']}.")
            if m["others"]:
                out.append(f"\n**Next in line.** {'; '.join(m['others'])}.")
        else:
            out.append(f"\n**What users get.** {m['gain']}")
            out.append(f"\n**Why it matters.** {m['why']}")
            if m["kind"] == "loop" and m.get("later"):
                out.append(f"\nMove 1 alone gives the next level; this is what then holds the loop at Level {rec['next']}.")
            if m["kind"] == "safety" and m.get("ahead"):
                out.append("\nThe next level does not need it yet, but Level 3 does, and it is the control nearest to passing.")
            if m["kind"] == "safety" and m.get("also"):
                out.append(f"\n**Also failing for Level 3.** {'; '.join(m['also'])}.")
        if m.get("evidence"):
            out.append(f"\n**Evidence.** {m['evidence']}")
        out.append(f"\n**Track in real use.** {m['measure']}")
        out.append("\n**Done when:**\n")
        out += [f"- [ ] {d}" for d in m["done_when"]]
        out += ["", "<details><summary>Prompt for a coding agent</summary>", "", "```text", m["prompt"], "```", "",
                "</details>"]
    out += ["", "## For engineers", ""]
    if rec["rest"]:
        out.append("After the three moves, the rest of the way to Level " + str(rec["next"]) + ": " +
                   "; ".join(f"`{r['code']}` {r['from']} → {r['to']}" for r in rec["rest"]) + ".")
        out.append("")
    for i, m in enumerate(rec["moves"], 1):
        if m["kind"] == "people":
            out.append(f"{i}. Change kind `{m['change_kind']}` reach {m['from']} → {m['to']}.")
        else:
            out.append(f"{i}. `{m['criterion']}` {m['from']} → {m['to']} ({m['loop']} loop, {m['stage']}"
                       f"{', control: ' + m['control'] if m.get('control') else ''}).")
    return "\n".join(out) + "\n"


def make(path, rubric=score.DEFAULT_RUBRIC, plain_path=DEFAULT_PLAIN, remediation_path=DEFAULT_REMEDIATION):
    criteria, order, model = score.load_rubric(rubric)
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    errors = score.validate(data, criteria, order, model)
    if errors:
        raise SystemExit("Assessment does not validate:\n - " + "\n - ".join(errors))
    plain = load_plain(plain_path)
    remediation = score.load_remediation(remediation_path, criteria)
    return recommend(data, criteria, order, model, plain, remediation), plain


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("assessment")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rec, plain = make(args.assessment)
    if args.json:
        print(json.dumps(rec, indent=2, ensure_ascii=False))
    else:
        print(render(rec, plain), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
