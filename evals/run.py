#!/usr/bin/env python3
"""Compare a rater's assessment of an evaluation case with the case's expected readings.

Usage:
  run.py <case-dir> <assessment.json> [--min 0.8] [--json] [--scorer PATH] [--no-levels]

<case-dir> holds expected.json and repo/, the fixture repository the rater was given.
Every expectation is printed as met or missed with the rater's value and evidence, then the
share met, overall and for the trap expectations (where a careless rater over-scores).
Exit status: 0 when the share met is at least --min, 1 below it, 2 when a file cannot be read.

Loop levels come from the bundled scorer (score.py --json). When the assessment does not
validate, or the scorer cannot run, the loop expectations are reported as unavailable and
left out of the share, never counted as met or missed.
"""

import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULT_SCORER = os.path.join(ROOT, "skills", "evolvable-software", "scripts", "score.py")
sys.path.insert(0, HERE)
from agreement import reading  # noqa: E402

LOOP_NAMES = {"request": "Request → Release", "fix": "Issue → Fix", "expansion": "Opportunity → Expansion"}
STATUS_WORDS = {"not_applicable": "not applicable", "not_evidenced": "not evidenced", "missing": "not in the file",
                "todo": "not scored"}


def load_json(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def in_range(value, bounds):
    return isinstance(value, int) and not isinstance(value, bool) and bounds[0] <= value <= bounds[1]


def span(bounds):
    return str(bounds[0]) if bounds[0] == bounds[1] else f"{bounds[0]} to {bounds[1]}"


def short(text, limit=110):
    text = " ".join(str(text or "").split())
    return text if len(text) <= limit else text[:limit - 1] + "…"


def item(section, ident, expected, observed, met, spec, evidence=""):
    return {"section": section, "id": ident, "expected": expected, "observed": observed, "met": met,
            "trap": bool(spec.get("trap")), "reason": spec.get("reason", ""), "files": spec.get("files", []),
            "evidence": short(evidence)}


def check_criteria(section, specs, entries):
    out = []
    for cid, spec in specs.items():
        r = reading(entries.get(cid))
        if r["status"] == "assessed":
            observed = str(r["score"])
        else:
            observed = STATUS_WORDS.get(r["status"], r["status"])
        if "range" in spec:
            met = r["status"] == "assessed" and in_range(r["score"], spec["range"])
            expected = span(spec["range"])
        else:
            met = r["status"] == spec["status"]
            expected = STATUS_WORDS.get(spec["status"], spec["status"])
        out.append(item(section, cid, expected, observed, met, spec, r.get("evidence", "")))
    return out


def kind_matches(kind, keywords):
    text = (str(kind.get("id", "")) + " " + str(kind.get("name", ""))).lower()
    return any(k.lower() in text for k in keywords)


def check_kinds(spec, data):
    out = []
    kinds = data.get("change_kinds")
    if not isinstance(kinds, list):
        kinds = None
    kinds = [k for k in kinds if isinstance(k, dict)] if kinds is not None else None
    if "main_count" in spec:
        s = spec["main_count"]
        if kinds is None:
            out.append(item("kinds", "main kinds", span(s["range"]), "change_kinds not recorded", False, s))
        else:
            count = sum(k.get("main") is True for k in kinds)
            out.append(item("kinds", "main kinds", span(s["range"]), str(count), in_range(count, s["range"]), s,
                            ", ".join(str(k.get("id")) for k in kinds if k.get("main") is True)))
    if "all_reach" in spec:
        s = spec["all_reach"]
        if kinds is None:
            out.append(item("kinds", "reach of every kind", span(s["range"]), "change_kinds not recorded", False, s))
        else:
            reaches = [k.get("reach") for k in kinds]
            met = bool(reaches) and all(in_range(x, s["range"]) for x in reaches)
            out.append(item("kinds", "reach of every kind", span(s["range"]),
                            ", ".join(f"{k.get('id')} {k.get('reach')}" for k in kinds), met, s))
    # Each rater kind belongs to the first expected kind whose keywords it contains.
    assigned = {i: [] for i in range(len(spec.get("kinds", [])))}
    for kind in kinds or []:
        for i, expected in enumerate(spec.get("kinds", [])):
            if kind_matches(kind, expected["keywords"]):
                assigned[i].append(kind)
                break
    for i, s in enumerate(spec.get("kinds", [])):
        label = s["label"]
        matched = assigned[i]
        if kinds is None or not matched:
            observed = "change_kinds not recorded" if kinds is None else "no kind listed matches " + \
                "/".join(s["keywords"])
            out.append(item("kinds", f"{label}: reach", span(s["reach"]), observed, False, s))
            if "main" in s:
                out.append(item("kinds", f"{label}: main", str(s["main"]).lower(), observed, False, s))
            continue
        observed = ", ".join(f"{k.get('id')} {k.get('reach')}" for k in matched)
        evidence = "; ".join(str(k.get("evidence", "")) for k in matched)
        out.append(item("kinds", f"{label}: reach", span(s["reach"]), observed,
                        all(in_range(k.get("reach"), s["reach"]) for k in matched), s, evidence))
        if "main" in s:
            mains = [k.get("main") is True for k in matched]
            met = any(mains) if s["main"] else not any(mains)
            out.append(item("kinds", f"{label}: main", str(s["main"]).lower(),
                            ", ".join(f"{k.get('id')} {str(k.get('main')).lower()}" for k in matched), met, s))
    return out


def run_scorer(scorer, assessment_path):
    """(loop levels, None) from score.py --json, or (None, why they are unavailable)."""
    if not scorer or not os.path.exists(scorer):
        return None, "scorer not found"
    try:
        done = subprocess.run([sys.executable, scorer, assessment_path, "--json"], capture_output=True,
                              text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, f"scorer did not run: {exc}"
    if done.returncode != 0:
        lines = [l.strip(" -") for l in (done.stdout + done.stderr).splitlines() if l.strip()]
        detail = "; ".join(lines[1:4]) if lines and lines[0].startswith("VALIDATION FAILED") else "; ".join(lines[:3])
        more = f" (and {len(lines) - 4} more)" if len(lines) > 4 else ""
        return None, "assessment does not validate: " + short(detail, 300) + more
    try:
        loops = json.loads(done.stdout)["sal"]["loops"]
        return {name: info["level"] for name, info in loops.items()}, None
    except (ValueError, KeyError, TypeError) as exc:
        return None, f"unexpected scorer output: {exc}"


def evaluate(case_dir, assessment_path, scorer=DEFAULT_SCORER, levels=True):
    expected = load_json(os.path.join(case_dir, "expected.json"))
    data = load_json(assessment_path)
    if not isinstance(data, dict):
        raise ValueError(f"{assessment_path}: not an assessment object")
    items = []
    if "archetype" in expected:
        s = expected["archetype"]
        items.append(item("archetype", "archetype", " or ".join(s["allowed"]), str(data.get("archetype")),
                          data.get("archetype") in s["allowed"], s))
    facts = data.get("scope_facts", {}) if isinstance(data.get("scope_facts"), dict) else {}
    for fact, s in expected.get("scope_facts", {}).items():
        entry = facts.get(fact)
        value = entry.get("value") if isinstance(entry, dict) else None
        items.append(item("scope facts", fact, str(s["value"]).lower(),
                          "not recorded" if value is None else str(value).lower(), value is s["value"], s,
                          entry.get("evidence", "") if isinstance(entry, dict) else ""))
    scores = data.get("scores", {}) if isinstance(data.get("scores"), dict) else {}
    items += check_criteria("criteria", expected.get("criteria", {}), scores)
    ai_entries = {cid: e["ai"] for cid, e in scores.items() if isinstance(e, dict) and "ai" in e}
    items += check_criteria("AI readings", expected.get("ai_readings", {}), ai_entries)
    if "change_kinds" in expected:
        items += check_kinds(expected["change_kinds"], data)
    unavailable = None
    if expected.get("loops"):
        found, unavailable = run_scorer(scorer, assessment_path) if levels else (None, "levels not computed (--no-levels)")
        for loop, s in expected["loops"].items():
            name = LOOP_NAMES.get(loop, loop)
            if found is None:
                items.append(item("loops", name, span(s["range"]), "unavailable", None, s))
            else:
                level = found.get(loop)
                items.append(item("loops", name, span(s["range"]), "not reported" if level is None else f"L{level}",
                                  in_range(level, s["range"]), s))
    counted = [i for i in items if i["met"] is not None]
    traps = [i for i in counted if i["trap"]]
    return {"case": expected.get("case", os.path.basename(os.path.abspath(case_dir))),
            "assessment": assessment_path, "items": items,
            "met": sum(i["met"] for i in counted), "counted": len(counted),
            "share": round(sum(i["met"] for i in counted) / len(counted), 3) if counted else 0.0,
            "traps_met": sum(i["met"] for i in traps), "traps": len(traps),
            "trap_share": round(sum(i["met"] for i in traps) / len(traps), 3) if traps else None,
            "unavailable": sum(i["met"] is None for i in items), "levels_unavailable_because": unavailable}


def render(result, minimum):
    lines = [f"# Evaluation case {result['case']}", "", f"Assessment: `{result['assessment']}`", ""]
    section = None
    for i in result["items"]:
        if i["section"] != section:
            section = i["section"]
            if lines[-1] != "":
                lines.append("")
            lines += [f"## {section[0].upper() + section[1:]}", "",
                      "| | Expectation | Expected | Rater | Rater's evidence | Why |", "|---|---|---|---|---|---|"]
        mark = "UNAVAILABLE" if i["met"] is None else "MET" if i["met"] else "MISSED"
        trap = " (trap)" if i["trap"] else ""
        why = i["reason"] + (f" See {', '.join(i['files'])}." if i["files"] else "")
        cells = [mark, i["id"] + trap, i["expected"], i["observed"], i["evidence"] or "–", why]
        lines.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
    lines += ["", "## Result", ""]
    lines.append(f"- Met: {result['met']} of {result['counted']} ({round(100 * result['share'])}%); "
                 f"pass mark {round(100 * minimum)}%.")
    if result["traps"]:
        lines.append(f"- Traps met: {result['traps_met']} of {result['traps']} "
                     f"({round(100 * result['trap_share'])}%).")
    if result["unavailable"]:
        lines.append(f"- Not counted: {result['unavailable']} loop expectations, because "
                     f"{result['levels_unavailable_because']}.")
    lines.append(f"- Verdict: {'PASS' if result['share'] >= minimum else 'FAIL'}.")
    return "\n".join(lines).lstrip("\n") + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compare an assessment of an evaluation case with expected.json.")
    parser.add_argument("case_dir")
    parser.add_argument("assessment")
    parser.add_argument("--min", type=float, default=0.8, help="pass mark as a share of expectations met (0.8)")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--scorer", default=DEFAULT_SCORER, help="path to score.py (default: the bundled one)")
    parser.add_argument("--no-levels", action="store_true", help="do not run the scorer for loop levels")
    args = parser.parse_args(argv)
    try:
        result = evaluate(args.case_dir, args.assessment, args.scorer, not args.no_levels)
    except (OSError, ValueError, KeyError) as exc:
        print(f"Cannot evaluate: {exc}", file=sys.stderr)
        return 2
    result["min"] = args.min
    result["passed"] = result["share"] >= args.min
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        sys.stdout.write(render(result, args.min))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
