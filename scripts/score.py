#!/usr/bin/env python3
"""Validate, score, profile, and prescribe an MSR assessment.

Usage:
  score.py SCORES.json [--json] [--quiet] [--rubric PATH]
  score.py SCORES.json --prescribe [--target 3|4] [--json] [--remediation PATH]

Every scoring choice (indexes, profiles, closed-loop floors, bands, archetype
exclusions, caps) is read from the msr-model block in references/rubric.md.

Criterion entry fields:
  status          assessed | not_evidenced | not_applicable
  score           0..4, the level in the default configuration (assessed)
  grade           A | B | C (assessed)
  evidence        text (assessed)
  alt_score       0..4, an adjacent level that is also defensible (optional)
  available_score 0..4, the level with shipped opt-in settings enabled (optional)
  single_entity   true | false (optional)
  incident        true | false (optional)
  searched        text (not_evidenced)
  rationale       text (not_applicable)
  if_applicable   0..4, the score it would get if counted (not_applicable, optional)
"""

import argparse
import json
import os
import re
import sys
from decimal import ROUND_HALF_UP, Decimal
from statistics import mean

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RUBRIC = os.path.join(HERE, "..", "references", "rubric.md")
DEFAULT_REMEDIATION = os.path.join(HERE, "..", "references", "remediation.md")

STATUSES = ("assessed", "not_evidenced", "not_applicable")
PLACEHOLDERS = {"", "not evaluated yet", "todo", "tbd", "n/a", "na", "none", "-"}
VARIANTS = ("default", "alternate", "available", "assessed_only", "all_applicable")


class ModelError(SystemExit):
    pass


def r1(value):
    """Round half up to one decimal, for display only."""
    if value is None:
        return None
    return float(Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def load_rubric(path):
    criteria, order, titles = {}, [], {}
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    for line in text.splitlines():
        dimension = re.match(r"^## Dimension ([A-Z]): (.+)$", line.strip())
        if dimension:
            titles[dimension.group(1)] = dimension.group(2).strip()
        criterion = re.match(r"^### ([A-Z])(\d+) (.+)$", line.strip())
        if criterion:
            cid = criterion.group(1) + criterion.group(2)
            if cid in criteria:
                raise ModelError(f"Rubric defines {cid} twice: {path}")
            criteria[cid] = {"dim": criterion.group(1), "title": criterion.group(3).strip()}
            order.append(cid)
    if not criteria:
        raise ModelError("Rubric has no criterion headings: " + path)
    block = re.search(r"```json msr-model\n(.*?)\n```", text, re.S)
    if not block:
        raise ModelError("Rubric has no msr-model block: " + path)
    model = json.loads(block.group(1))
    dims = {c["dim"] for c in criteria.values()}
    for group in ("indexes", "profiles"):
        for name, members in model[group].items():
            unknown = set(members) - dims
            if unknown:
                raise ModelError(f"{group} '{name}' names unknown dimensions: {sorted(unknown)}")
    used = {d for members in model["indexes"].values() for d in members}
    used |= {d for members in model["profiles"].values() for d in members}
    unused = dims - used
    if unused:
        raise ModelError(f"Dimensions in no index or profile: {sorted(unused)}")
    for floor in model["closed_loop_floors"]:
        unknown = set(floor["any_of"]) - set(criteria)
        if unknown:
            raise ModelError(f"closed-loop floor names unknown criteria: {sorted(unknown)}")
    return criteria, order, titles, model


def load_remediation(path, criteria):
    remediation, current = {}, None
    with open(path, encoding="utf-8") as handle:
        lines = handle.readlines()
    for raw in lines:
        line = raw.rstrip("\n")
        heading = re.match(r"^### ([A-Z]\d+)\s*$", line.strip())
        if heading:
            current = heading.group(1)
            remediation[current] = {"to3": "", "to4": "", "requires": [], "helps": [], "size": ""}
            continue
        if not current:
            continue
        for prefix, field in (("To 3:", "to3"), ("To 4:", "to4"), ("Size:", "size")):
            if line.startswith(prefix):
                remediation[current][field] = line[len(prefix):].strip()
        for prefix, field in (("Requires:", "requires"), ("Helps:", "helps")):
            if line.startswith(prefix):
                body = line[len(prefix):].strip()
                ids = [] if body.lower().startswith("none") else re.findall(r"\b([A-Z]\d+)\b", body)
                unknown = [i for i in ids if i not in criteria]
                if unknown:
                    raise ModelError(f"Remediation {current} {prefix} names unknown criteria: {unknown}")
                remediation[current][field] = ids
    return remediation


def _is_int_score(value):
    return isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 4


def _text(entry, key):
    return str(entry.get(key) or "").strip()


def validate(data, criteria, order, model):
    errors = []
    if not isinstance(data, dict):
        return ["scores file must be a JSON object"]
    exclusions = model["archetype_exclusions"]
    archetype = data.get("archetype")
    if archetype not in exclusions:
        errors.append("archetype must be one of: " + ", ".join(sorted(exclusions)))
    scores = data.get("scores")
    if not isinstance(scores, dict):
        return errors + ["'scores' must be an object keyed by criterion id"]
    allowed_na = exclusions.get(archetype, [])
    for cid in order:
        if cid not in scores:
            errors.append(f"{cid}: missing")
            continue
        entry = scores[cid]
        if not isinstance(entry, dict):
            errors.append(f"{cid}: entry must be an object, got {type(entry).__name__}")
            continue
        status = entry.get("status")
        if status == "todo":
            errors.append(f"{cid}: not yet assessed")
            continue
        if status not in STATUSES:
            errors.append(f"{cid}: status must be one of {', '.join(STATUSES)}, got {status!r}")
            continue
        for flag in ("single_entity", "incident"):
            if flag in entry and not isinstance(entry[flag], bool):
                errors.append(f"{cid}: {flag} must be true or false, got {entry[flag]!r}")
        for key in ("alt_score", "available_score", "if_applicable"):
            if key in entry and not _is_int_score(entry[key]):
                errors.append(f"{cid}: {key} must be an integer 0..4, got {entry[key]!r}")
        if status == "assessed":
            if not _is_int_score(entry.get("score")):
                errors.append(f"{cid}: score must be an integer 0..4, got {entry.get('score')!r}")
            if str(entry.get("grade", "")).upper() not in ("A", "B", "C"):
                errors.append(f"{cid}: grade must be A, B or C, got {entry.get('grade')!r}")
            if _text(entry, "evidence").lower() in PLACEHOLDERS:
                errors.append(f"{cid}: assessed criteria need evidence")
            if _is_int_score(entry.get("available_score")) and _is_int_score(entry.get("score")) \
                    and entry["available_score"] < entry["score"]:
                errors.append(f"{cid}: available_score cannot be below score")
        elif status == "not_evidenced":
            if _text(entry, "searched").lower() in PLACEHOLDERS:
                errors.append(f"{cid}: not_evidenced needs the searched scope")
        else:
            if _text(entry, "rationale").lower() in PLACEHOLDERS:
                errors.append(f"{cid}: not_applicable needs a rationale")
            if allowed_na != "*" and cid not in allowed_na:
                errors.append(f"{cid}: archetype '{archetype}' may not exclude {cid} "
                              f"(allowed: {', '.join(allowed_na) or 'none'})")
    for unknown in sorted(set(scores) - set(order)):
        errors.append(f"{unknown}: not in rubric")
    return errors


def effective_scores(data, order, model, variant):
    """Return ({criterion: value or None}, [cap flags]) for one variant."""
    caps = model["caps"]
    values, flags = {}, []
    for cid in order:
        entry = data["scores"][cid]
        status = entry["status"]
        if status == "not_applicable":
            values[cid] = entry.get("if_applicable") if variant == "all_applicable" else None
            continue
        if status == "not_evidenced":
            if variant == "assessed_only":
                values[cid] = None
            elif variant == "alternate" and "alt_score" in entry:
                values[cid] = entry["alt_score"]
            else:
                values[cid] = 0
            continue
        value = entry["score"]
        if variant == "alternate" and "alt_score" in entry:
            value = entry["alt_score"]
        if variant == "available" and "available_score" in entry:
            value = entry["available_score"]
        if str(entry["grade"]).upper() == "C" and value > caps["grade_c_max"]:
            flags.append(f"{cid}: grade C caps {value} -> {caps['grade_c_max']}")
            value = caps["grade_c_max"]
        if entry.get("single_entity") is True and value > caps["single_entity_max"]:
            flags.append(f"{cid}: single-entity caps {value} -> {caps['single_entity_max']}")
            value = caps["single_entity_max"]
        if entry.get("incident") is True and value > 0:
            new = max(0, value - caps["incident_penalty"])
            flags.append(f"{cid}: incident deduction {value} -> {new}")
            value = new
        values[cid] = value
    return values, flags


def aggregate(values, criteria, model):
    by_dim = {}
    for cid, value in values.items():
        if value is not None:
            by_dim.setdefault(criteria[cid]["dim"], []).append(value)
    dims = {d: mean(v) for d, v in by_dim.items()}

    def over(members):
        present = [dims[d] for d in members if d in dims]
        return mean(present) if present else None

    return {
        "dimension_means": dims,
        "indexes": {name: over(m) for name, m in model["indexes"].items()},
        "profiles": {name: over(m) for name, m in model["profiles"].items()},
    }


def closed_loop(values, model):
    stages, candidate = [], True
    for floor in model["closed_loop_floors"]:
        best = max((values.get(c) for c in floor["any_of"] if values.get(c) is not None), default=None)
        passed = best is not None and best >= floor["min"]
        candidate = candidate and passed
        stages.append({"stage": floor["stage"], "criteria": floor["any_of"], "min": floor["min"],
                       "best": best, "passed": passed})
    return candidate, stages


def band(value, model):
    if value is None:
        return "not scored"
    for limit, label in model["bands"]:
        if limit is None or value < limit:
            return label
    return model["bands"][-1][1]


def score_assessment(data, criteria, order, model):
    result = {"variants": {}, "flags": []}
    for variant in VARIANTS:
        values, flags = effective_scores(data, order, model, variant)
        agg = aggregate(values, criteria, model)
        loop, stages = closed_loop(values, model)
        result["variants"][variant] = {"effective": values, "closed_loop_candidate": loop,
                                       "closed_loop": stages, **agg}
        if variant == "default":
            result["flags"] = flags
    coverage = {s: 0 for s in STATUSES}
    grades = {"A": 0, "B": 0, "C": 0}
    for cid in order:
        entry = data["scores"][cid]
        coverage[entry["status"]] += 1
        if entry["status"] == "assessed":
            grades[str(entry["grade"]).upper()] += 1
    result["coverage"], result["grades"] = coverage, grades
    ranges = {}
    for name in model["indexes"]:
        vals = [result["variants"][v]["indexes"][name] for v in ("default", "alternate")]
        vals = [v for v in vals if v is not None]
        ranges[name] = [min(vals), max(vals)] if vals else None
    result["ranges"] = ranges
    return result


def rounded(obj):
    if isinstance(obj, float):
        return r1(obj)
    if isinstance(obj, dict):
        return {k: rounded(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [rounded(v) for v in obj]
    return obj


def cell(text):
    return re.sub(r"\s+", " ", str(text)).replace("|", "\\|")


def fmt(value):
    return "–" if value is None else f"{r1(value):.1f}"


def schedule(order, values, remediation, target, exclude=()):
    build = [c for c in order if c not in exclude and values.get(c) is not None and values[c] < target]
    missing = [c for c in build if c not in remediation]
    if missing:
        raise ModelError("Remediation catalogue has no entry for: " + ", ".join(missing))
    pending, done, slices = list(build), set(), []
    while pending:
        ready = [c for c in pending
                 if all(r not in pending or r in done for r in remediation[c]["requires"])]
        if not ready:
            raise ModelError("Dependency cycle among: " + ", ".join(sorted(pending)))
        slices.append(ready)
        done.update(ready)
        pending = [c for c in pending if c not in done]
    return build, slices


def render_markdown(data, criteria, order, titles, model, result):
    d = result["variants"]["default"]
    lines = [f"# MSR assessment: {cell(data.get('product'))}", "",
             f"Framework {model['version']}. Date {cell(data.get('date'))}. Source {cell(data.get('source'))}. "
             f"Archetype **{data.get('archetype')}**.", ""]
    cov, grades = result["coverage"], result["grades"]
    lines += [f"Coverage: {cov['assessed']} assessed, {cov['not_evidenced']} not evidenced, "
              f"{cov['not_applicable']} not applicable. Grades: {grades['A']} A, {grades['B']} B, {grades['C']} C.", "",
              "## Indexes", "",
              "| Index | Default | Band | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |",
              "|---|---:|---|---|---:|---:|---:|"]
    for name in model["indexes"]:
        value = d["indexes"][name]
        rng = result["ranges"][name]
        rng_text = "–" if rng is None else (fmt(rng[0]) if r1(rng[0]) == r1(rng[1]) else f"{fmt(rng[0])}–{fmt(rng[1])}")
        lines.append(f"| {name} | {fmt(value)} | {band(value, model)} | {rng_text} | "
                     f"{fmt(result['variants']['available']['indexes'][name])} | "
                     f"{fmt(result['variants']['assessed_only']['indexes'][name])} | "
                     f"{fmt(result['variants']['all_applicable']['indexes'][name])} |")
    lines += ["", "## Profiles", "", "| Profile | Default | With opt-in settings |", "|---|---:|---:|"]
    for name in model["profiles"]:
        lines.append(f"| {name} | {fmt(d['profiles'][name])} | {fmt(result['variants']['available']['profiles'][name])} |")
    avail = result["variants"]["available"]
    lines += ["", "## Closed loop", "",
              f"Closed-loop candidate: **{'yes' if d['closed_loop_candidate'] else 'no'}** by default, "
              f"**{'yes' if avail['closed_loop_candidate'] else 'no'}** with opt-in settings. "
              "This is a minimum-mechanism signal, not a production-readiness or outcome claim.", "",
              "| Stage | Criteria | Needs | Default | With opt-in settings |", "|---|---|---:|---:|---:|"]
    for stage, stage_avail in zip(d["closed_loop"], avail["closed_loop"]):
        mark = lambda s: f"{'–' if s['best'] is None else s['best']} {'pass' if s['passed'] else 'fail'}"
        lines.append(f"| {stage['stage']} | {', '.join(stage['criteria'])} | {stage['min']} | {mark(stage)} | {mark(stage_avail)} |")
    if result["flags"]:
        lines += ["", "Caps and deductions applied:", ""] + [f"- {f}" for f in result["flags"]]
    lines += ["", "## Dimension means", "", "| Dimension | Default |", "|---|---:|"]
    for dim in sorted(d["dimension_means"]):
        lines.append(f"| {dim} {cell(titles.get(dim, ''))} | {fmt(d['dimension_means'][dim])} |")
    lines += ["", "## Criteria", "",
              "| Criterion | Status | Score | Alternate | Opt-in | Grade | Evidence, search scope or rationale |",
              "|---|---|---:|---:|---:|---|---|"]
    for cid in order:
        entry = data["scores"][cid]
        status = entry["status"]
        value = d["effective"][cid]
        text = entry.get("evidence") or entry.get("searched") or entry.get("rationale") or ""
        lines.append(f"| {cid} {cell(criteria[cid]['title'])} | {status} | "
                     f"{'excluded' if value is None else value} | {entry.get('alt_score', '')} | "
                     f"{entry.get('available_score', '')} | {entry.get('grade', '-') if status == 'assessed' else '-'} | "
                     f"{cell(text)} |")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate, score and prescribe an MSR assessment.")
    parser.add_argument("scores")
    parser.add_argument("--rubric", default=DEFAULT_RUBRIC)
    parser.add_argument("--remediation", default=DEFAULT_REMEDIATION)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--quiet", action="store_true", help="print only the index summary")
    parser.add_argument("--prescribe", action="store_true")
    parser.add_argument("--target", type=int, choices=(3, 4), default=3)
    args = parser.parse_args(argv)

    criteria, order, titles, model = load_rubric(args.rubric)
    try:
        with open(args.scores, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read {args.scores}: {exc}")
        return 2
    errors = validate(data, criteria, order, model)
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(" -", error)
        return 2
    result = score_assessment(data, criteria, order, model)
    default = result["variants"]["default"]

    if args.prescribe:
        remediation = load_remediation(args.remediation, criteria)
        investigate = [c for c in order if data["scores"][c]["status"] == "not_evidenced"]
        build, slices = schedule(order, default["effective"], remediation, args.target, exclude=investigate)
        projected = {c: (None if v is None else max(v, args.target)) for c, v in default["effective"].items()}
        projected_idx = aggregate(projected, criteria, model)["indexes"]
        out = {"product": data.get("product"), "target": args.target, "investigate_first": investigate,
               "slices": [[{"id": c, "title": criteria[c]["title"], "from": default["effective"][c],
                            "size": remediation[c]["size"], "requires": remediation[c]["requires"],
                            "helps": remediation[c]["helps"],
                            "move": remediation[c]["to3" if args.target == 3 else "to4"]} for c in sl]
                          for sl in slices],
               "current": rounded(default["indexes"]), "projected_ceiling": rounded(projected_idx)}
        if args.json:
            print(json.dumps(out, indent=2))
            return 0
        print(f"# MSR prescription: {cell(out['product'])} to level {args.target}\n")
        if investigate:
            print("## Investigate first\n")
            print("These criteria are not evidenced. Establish whether the capability exists before planning work: "
                  + ", ".join(f"{c} {criteria[c]['title']}" for c in investigate) + ".\n")
        print(f"{len(build)} assessed criteria are below {args.target}. Items in a slice can proceed in parallel after earlier slices.\n")
        for number, sl in enumerate(out["slices"], 1):
            print(f"## Slice {number}\n\n| Criterion | Now | Size | Requires | Helps | Move |\n|---|---:|---|---|---|---|")
            for item in sl:
                print(f"| {item['id']} {cell(item['title'])} | {item['from']} | {item['size']} | "
                      f"{', '.join(item['requires']) or 'none'} | {', '.join(item['helps']) or '–'} | {cell(item['move'])} |")
            print()
        print("## Projected ceilings if every move lands\n\n| Index | Now | Ceiling |\n|---|---:|---:|")
        for name in model["indexes"]:
            print(f"| {name} | {fmt(default['indexes'][name])} | {fmt(projected_idx[name])} |")
        print("\nCeilings, not delivery forecasts. Re-estimate every size for the assessed software.")
        return 0

    payload = {"product": data.get("product"), "date": data.get("date"), "source": data.get("source"),
               "archetype": data.get("archetype"), "framework_version": model["version"],
               "coverage": result["coverage"], "grades": result["grades"],
               "indexes": rounded(default["indexes"]),
               "bands": {k: band(v, model) for k, v in default["indexes"].items()},
               "ranges": rounded(result["ranges"]),
               "profiles": rounded(default["profiles"]),
               "dimension_means": rounded(default["dimension_means"]),
               "closed_loop_candidate": default["closed_loop_candidate"],
               "closed_loop": default["closed_loop"],
               "flags": result["flags"],
               "effective_scores": default["effective"],
               "variants": {v: {"indexes": rounded(result["variants"][v]["indexes"]),
                                "profiles": rounded(result["variants"][v]["profiles"]),
                                "closed_loop_candidate": result["variants"][v]["closed_loop_candidate"]}
                            for v in VARIANTS if v != "default"},
               "criteria_in_rubric": len(order)}
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0
    if args.quiet:
        for name in model["indexes"]:
            print(f"{name}: {fmt(default['indexes'][name])} ({band(default['indexes'][name], model)})")
        print(f"closed-loop candidate: {'yes' if default['closed_loop_candidate'] else 'no'}")
        return 0
    print(render_markdown(data, criteria, order, titles, model, result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
