#!/usr/bin/env python3
"""EVOLVE quick scan: an indicative range per loop from about twenty yes/no/unsure answers.

Usage:
  quick_scan.py ANSWERS.json [--json] [--questions PATH]
  quick_scan.py --template [--questions PATH]
  quick_scan.py --table [--questions PATH]

The questions, the level each one supports, the safety gates and the follow-up
checks are read from the json quick-scan block in references/quick-scan.md.

Answers file:
  {"product": "Name",
   "answers": {"<question id>": "yes" | "no" | "unsure" | "n/a", ...},
   "notes": {"<question id>": "text", ...}}        (notes optional)

Every question must be answered. "n/a" is allowed only on questions that say
when it applies. A "questions" key, as printed by --template, is ignored.

Reading the answers:
  - the low end of each loop's range treats "unsure" as no; the high end treats it as yes;
  - a level is reached only when every question for it and every lower level is yes;
  - any applicable safety gate that is not "yes" holds every loop at Level 2;
  - the quick scan never reports Level 5.

The result is indicative. It is not an EVOLVE assessment and must not be
published as a level. Exit code 2 means the answers file is invalid.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_QUESTIONS = os.path.normpath(os.path.join(HERE, "..", "references", "quick-scan.md"))

NOTICE = (
    "Indicative quick scan, not an EVOLVE assessment: do not publish it as a level. "
    "Only a full assessment, with evidence for every criterion, gives a level."
)
VALUES = ("yes", "no", "unsure", "n/a")
TOP_KEYS = ("product", "answers", "notes", "questions")
TABLE_START = "<!-- quick-scan-table:start -->"
TABLE_END = "<!-- quick-scan-table:end -->"
ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")


class QuickScanError(Exception):
    """The question file or the answers file is invalid. Carries a list of messages."""

    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("\n".join(self.errors))


# ---------------------------------------------------------------- the model

def load_model(path=DEFAULT_QUESTIONS):
    """Load and check the json quick-scan block from the question file."""
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    block = re.search(r"```json quick-scan\n(.*?)\n```", text, re.S)
    if not block:
        raise QuickScanError(["No json quick-scan block in " + path])
    model = json.loads(block.group(1))
    check_model(model)
    return model


def requirement_ids(item):
    return list(item["any"]) if isinstance(item, dict) else [item]


def check_model(model):
    errors = []
    ids = [q["id"] for q in model["questions"]]
    known = set(ids)
    if len(ids) != len(known):
        errors.append("Duplicate question ids")
    for q in model["questions"]:
        if not ID_PATTERN.match(q["id"]):
            errors.append("Bad question id: " + q["id"])
        for field in ("section", "question", "where", "maps_to"):
            if not q.get(field):
                errors.append("Question %s has no %s" % (q["id"], field))
    used = set()
    max_level = model["max_level"]
    for loop in model["loops"]:
        for level, items in loop["levels"].items():
            if not 1 <= int(level) <= max_level:
                errors.append("Loop %s has a level outside 1 to %d" % (loop["id"], max_level))
            for item in items:
                for qid in requirement_ids(item):
                    if qid not in known:
                        errors.append("Loop %s level %s names unknown question %s" % (loop["id"], level, qid))
                    used.add(qid)
        for level in range(1, max_level + 1):
            if str(level) not in model["challenges"].get(loop["id"], {}):
                errors.append("No follow-up check for %s at level %d" % (loop["id"], level))
    for q in model["questions"]:
        if q.get("gate"):
            used.add(q["id"])
    for qid in ids:
        if qid not in used:
            errors.append("Question %s is used by no loop and is not a safety gate" % qid)
    for rule in model.get("consistency", []):
        for qid in (rule["when"], rule["id"]):
            if qid not in known:
                errors.append("Consistency rule names unknown question " + qid)
    if errors:
        raise QuickScanError(errors)


def questions_by_id(model):
    return {q["id"]: q for q in model["questions"]}


def gates(model):
    return [q for q in model["questions"] if q.get("gate")]


# ---------------------------------------------------------------- validation

def validate(model, data):
    """Return (product, answers, notes) or raise QuickScanError listing every problem."""
    errors = []
    if not isinstance(data, dict):
        raise QuickScanError(["The answers file must be a JSON object with product and answers"])
    qmap = questions_by_id(model)
    order = [q["id"] for q in model["questions"]]
    for key in sorted(data):
        if key not in TOP_KEYS:
            errors.append("Unknown top-level key %r (allowed: %s)" % (key, ", ".join(TOP_KEYS)))
    product = data.get("product")
    if not isinstance(product, str) or not product.strip():
        errors.append("product: give the product's name")
        product = ""
    raw = data.get("answers")
    answers = {}
    if not isinstance(raw, dict):
        errors.append("answers: must be an object mapping each question id to yes, no, unsure or n/a")
        raw = {}
    for qid in sorted(raw):
        if qid not in qmap:
            errors.append("answers: unknown question id %r" % qid)
            continue
        value = raw[qid]
        norm = value.strip().lower() if isinstance(value, str) else value
        if norm == "":
            errors.append("answers.%s: not answered (use yes, no, unsure or n/a)" % qid)
        elif norm not in VALUES:
            errors.append("answers.%s: %r is not one of yes, no, unsure, n/a" % (qid, value))
        elif norm == "n/a" and not qmap[qid].get("allows_na"):
            errors.append("answers.%s: n/a is not allowed; this question always applies" % qid)
        else:
            answers[qid] = norm
    missing = [qid for qid in order if qid not in raw]
    if missing:
        errors.append("answers: missing %s" % ", ".join(missing))
    for rule in model.get("consistency", []):
        if answers.get(rule["when"]) == rule["is"] and answers.get(rule["id"]) == rule["not"]:
            errors.append("answers.%s: cannot be %s when %s is %s. %s"
                          % (rule["id"], rule["not"], rule["when"], rule["is"], rule["why"]))
    notes = data.get("notes", {})
    if not isinstance(notes, dict):
        errors.append("notes: must be an object mapping question ids to text")
        notes = {}
    for qid in sorted(notes):
        if qid not in qmap:
            errors.append("notes: unknown question id %r" % qid)
        elif not isinstance(notes[qid], str):
            errors.append("notes.%s: must be text" % qid)
    if "questions" in data and not isinstance(data["questions"], dict):
        errors.append("questions: must be an object (it is ignored)")
    if errors:
        raise QuickScanError(errors)
    clean_notes = {qid: notes[qid].strip() for qid in order if isinstance(notes.get(qid), str) and notes[qid].strip()}
    return product.strip(), {qid: answers[qid] for qid in order}, clean_notes


# ---------------------------------------------------------------- reading

def truth(answers, unsure_as_yes):
    """True where a question counts as yes. n/a counts as met: it does not apply."""
    yes = {"yes", "n/a"} | ({"unsure"} if unsure_as_yes else set())
    return {qid: value in yes for qid, value in answers.items()}


def item_met(item, met):
    return any(met[qid] for qid in requirement_ids(item))


def raw_level(model, loop, met):
    level = 0
    for n in range(1, model["max_level"] + 1):
        if all(item_met(item, met) for item in loop["levels"].get(str(n), [])):
            level = n
        else:
            break
    return level


def gates_pass(model, answers):
    return all(answers[q["id"]] in ("yes", "n/a") for q in gates(model))


def loop_levels(model, answers):
    """{loop id: (low, high, raw_low, raw_high)}; raw ignores the safety-gate cap."""
    capped = not gates_pass(model, answers)
    cap = model["gate_cap"]
    out = {}
    for unsure_as_yes, slot in ((False, 0), (True, 1)):
        met = truth(answers, unsure_as_yes)
        for loop in model["loops"]:
            raw = raw_level(model, loop, met)
            level = min(raw, cap) if capped else raw
            out.setdefault(loop["id"], [None, None, None, None])
            out[loop["id"]][slot] = level
            out[loop["id"]][slot + 2] = raw
    return {lid: tuple(v) for lid, v in out.items()}


def range_text(low, high):
    return "likely L%d" % low if low == high else "likely L%d to L%d" % (low, high)


def names_text(model, low, high):
    names = model["level_names"]
    return names[low] if low == high else "%s to %s" % (names[low], names[high])


def blockers(model, loop, answers, low):
    """Questions that stand between a loop's low end and its next level."""
    nxt = low + 1
    if nxt > model["max_level"]:
        return []
    met = truth(answers, False)
    found = []
    for item in loop["levels"].get(str(nxt), []):
        if not item_met(item, met):
            found.append(requirement_ids(item)[0])  # the usual route of an either-or requirement
    if nxt > model["gate_cap"] and not gates_pass(model, answers):
        found.extend(q["id"] for q in gates(model) if answers[q["id"]] not in ("yes", "n/a"))
    return found


def most_change(model, answers, levels, count=3):
    """The answers whose change would move the ranges most."""
    order = [q["id"] for q in model["questions"]]
    loops = model["loops"]
    blocked = {}
    for loop in loops:
        for qid in blockers(model, loop, answers, levels[loop["id"]][0]):
            blocked.setdefault(qid, []).append(loop["id"])
    ranked = []
    for index, qid in enumerate(order):
        if answers[qid] not in ("no", "unsure"):
            continue
        as_yes = loop_levels(model, dict(answers, **{qid: "yes"}))
        as_no = loop_levels(model, dict(answers, **{qid: "no"}))
        changes = []
        swing = 0
        for loop in loops:
            y, n = as_yes[loop["id"]], as_no[loop["id"]]
            delta = (y[0] - n[0]) + (y[1] - n[1])
            swing += delta
            if delta:
                changes.append({"loop": loop["id"], "if_yes": [y[0], y[1]], "if_no": [n[0], n[1]]})
        held = blocked.get(qid, [])
        if swing <= 0 and not held:
            continue
        ranked.append((-swing, -len(held), 0 if answers[qid] == "unsure" else 1, index, qid, changes, held))
    ranked.sort(key=lambda r: r[:4])
    qmap = questions_by_id(model)
    loop_names = {loop["id"]: loop["name"] for loop in loops}
    result = []
    for _, _, _, _, qid, changes, held in ranked[:count]:
        if changes:
            parts = ["%s: %s if yes, %s if no" % (loop_names[c["loop"]],
                                                    range_text(*c["if_yes"]).replace("likely ", ""),
                                                    range_text(*c["if_no"]).replace("likely ", ""))
                     for c in changes]
            reason = "; ".join(parts)
        else:
            reason = ("Stands between %s and the next level, together with other answers that are not yes"
                      % join_names([loop_names[lid] for lid in held]))
        result.append({"id": qid, "question": qmap[qid]["question"], "answer": answers[qid],
                       "reason": reason, "changes": changes, "blocks_next_level": held})
    return result


def join_names(names):
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def scan(model, product, answers, notes=None):
    """The full reading as a dict. Deterministic for a given model and answers."""
    notes = notes or {}
    levels = loop_levels(model, answers)
    cap = model["gate_cap"]
    top = model["max_level"]
    loops = []
    for loop in model["loops"]:
        low, high, raw_low, raw_high = levels[loop["id"]]
        loops.append({
            "id": loop["id"], "name": loop["name"], "low": low, "high": high,
            "range": range_text(low, high), "meaning": names_text(model, low, high),
            "capped_by_safety_gates": raw_high > high,
            "uncapped_range": range_text(raw_low, raw_high) if raw_high > high else None,
        })
    gate_rows = []
    reading = {"yes": "closed", "no": "open", "unsure": "unknown", "n/a": "not applicable"}
    for q in gates(model):
        gate_rows.append({"id": q["id"], "gate": q["gate"], "answer": answers[q["id"]],
                          "reading": reading[answers[q["id"]]]})
    not_yes = [g for g in gate_rows if g["answer"] in ("no", "unsure")]
    caps = []
    capped_loops = [l["name"] for l in loops if l["capped_by_safety_gates"]]
    if capped_loops:
        caps.append({
            "kind": "safety-gates", "loops": capped_loops,
            "text": ("Held at Level %d: %s would otherwise read higher, but %s %s not yes. The framework "
                     "holds every loop at Level %d until every applicable safety gate passes."
                     % (cap, join_names(capped_loops), join_names(['"%s"' % g["gate"] for g in not_yes]),
                        "is" if len(not_yes) == 1 else "are", cap)),
        })
    top_loops = [l["name"] for l in loops if l["high"] == top]
    if top_loops:
        caps.append({
            "kind": "level-5", "loops": top_loops,
            "text": ("Stops at Level %d: the quick scan never reports Level 5. Level 5 needs records of the "
                     "product choosing, shipping and measuring its own changes over a period of real "
                     "operation, which only a full assessment can check." % top),
        })
    checks = []
    for loop in loops:
        nxt = loop["low"] + 1
        if nxt > top:
            text = model["level5_check"]
            checks.append({"loop": loop["name"], "level": top + 1, "check": text})
        else:
            verb = "Confirm" if nxt <= loop["high"] else "Toward"
            checks.append({"loop": loop["name"], "level": nxt, "verb": verb,
                           "check": model["challenges"][loop["id"]][str(nxt)]})
    unsure = [qid for qid, value in answers.items() if value == "unsure"]
    counts = {value: sum(1 for v in answers.values() if v == value) for value in VALUES}
    return {
        "notice": NOTICE,
        "product": product,
        "counts": counts,
        "loops": loops,
        "caps": caps,
        "safety_gates": gate_rows,
        "most_change": most_change(model, answers, levels),
        "next_checks": checks,
        "always_checks": list(model["always_checks"]),
        "unsure": unsure,
        "answers": [{"id": qid, "answer": answers[qid], "note": notes.get(qid, "")} for qid in answers],
    }


# ---------------------------------------------------------------- output

def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def render_markdown(result):
    lines = ["> **%s**" % NOTICE, "", "# Quick scan: %s" % result["product"], ""]
    c = result["counts"]
    lines.append("%d questions answered: %d yes, %d no, %d unsure, %d not applicable."
                 % (sum(c.values()), c["yes"], c["no"], c["unsure"], c["n/a"]))
    lines += ["", "## Indicative range", "",
              "The low end counts every unsure answer as no; the high end counts it as yes.", "",
              "| Loop | Indicative range | What that means |", "|---|---|---|"]
    for loop in result["loops"]:
        rng = loop["range"] + (" (held at L2 by safety gates)" if loop["capped_by_safety_gates"] else "")
        lines.append("| %s | %s | %s |" % (loop["name"], rng, loop["meaning"]))
    if result["caps"]:
        lines.append("")
        for cap in result["caps"]:
            lines.append("- " + cap["text"])
    lines += ["", "## Safety gates", "",
              "A gate is closed when the safeguard is in place, open when it is missing, and unknown when unsure.", "",
              "| Safety gate | Looks | Answer |", "|---|---|---|"]
    for gate in result["safety_gates"]:
        lines.append("| %s | %s | %s |" % (gate["gate"], gate["reading"], gate["answer"]))
    lines += ["", "## Answers that would most change the range", ""]
    if result["most_change"]:
        for i, item in enumerate(result["most_change"], 1):
            lines.append("%d. **%s** (`%s`, answered %s). %s." % (i, item["question"], item["id"],
                                                                 item["answer"], item["reason"]))
    else:
        lines.append("None: no single answer would move any range.")
    lines += ["", "## What a full assessment would check next", ""]
    for check in result["next_checks"]:
        if check.get("verb"):
            lines.append("- **%s, %s L%d:** %s" % (check["loop"], check["verb"].lower(), check["level"], check["check"]))
        else:
            lines.append("- **%s, beyond L4:** %s" % (check["loop"], check["check"]))
    if result["unsure"]:
        lines.append("- **Settle the unsure answers:** %s." % ", ".join("`%s`" % qid for qid in result["unsure"]))
    for text in result["always_checks"]:
        lines.append("- " + text)
    lines += ["", "## Answers", "", "| Id | Answer | Note |", "|---|---|---|"]
    for row in result["answers"]:
        lines.append("| `%s` | %s | %s |" % (row["id"], row["answer"], cell(row["note"])))
    lines += ["", "_%s_" % NOTICE, ""]
    return "\n".join(lines)


def render_table(model):
    """The question tables for references/quick-scan.md, generated from the json block."""
    lines = []
    section = None
    for number, q in enumerate(model["questions"], 1):
        if q["section"] != section:
            if section is not None:
                lines.append("")
            section = q["section"]
            lines += ["### " + section, "",
                      "| # | Id | Question | Where to look | Maps to |", "|---:|---|---|---|---|"]
        maps = q["maps_to"]
        if q.get("allows_na"):
            maps += " Answer n/a when: " + q["allows_na"]
        lines.append("| %d | `%s` | %s | %s | %s |" % (number, q["id"], cell(q["question"]),
                                                    cell(q["where"]), cell(maps)))
    return "\n".join(lines)


def template(model):
    return {
        "product": "",
        "answers": {q["id"]: "" for q in model["questions"]},
        "notes": {},
        "questions": {q["id"]: q["question"] + (" (n/a allowed when: %s)" % q["allows_na"] if q.get("allows_na") else "")
                      for q in model["questions"]},
    }


def dumps(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="EVOLVE quick scan: an indicative range, never a level.")
    parser.add_argument("answers", nargs="?", help="answers JSON file")
    parser.add_argument("--json", action="store_true", help="print the reading as JSON")
    parser.add_argument("--template", action="store_true", help="print an empty answers file")
    parser.add_argument("--table", action="store_true", help="print the question tables for quick-scan.md")
    parser.add_argument("--questions", default=DEFAULT_QUESTIONS, help="path to quick-scan.md")
    args = parser.parse_args(argv)
    try:
        model = load_model(args.questions)
    except (OSError, ValueError, KeyError, QuickScanError) as exc:
        sys.stderr.write("error: cannot load questions from %s: %s\n" % (args.questions, exc))
        return 2
    if args.template:
        sys.stdout.write(dumps(template(model)))
        return 0
    if args.table:
        sys.stdout.write(render_table(model) + "\n")
        return 0
    if not args.answers:
        parser.print_usage(sys.stderr)
        sys.stderr.write("error: give an answers file, or --template to start one\n")
        return 2
    try:
        with open(args.answers, encoding="utf-8") as handle:
            data = json.load(handle)
    except OSError as exc:
        sys.stderr.write("error: cannot read %s: %s\n" % (args.answers, exc))
        return 2
    except ValueError as exc:
        sys.stderr.write("error: %s is not valid JSON: %s\n" % (args.answers, exc))
        return 2
    try:
        product, answers, notes = validate(model, data)
    except QuickScanError as exc:
        for message in exc.errors:
            sys.stderr.write("error: %s\n" % message)
        return 2
    result = scan(model, product, answers, notes)
    sys.stdout.write(dumps(result) if args.json else render_markdown(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
