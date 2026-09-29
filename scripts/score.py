#!/usr/bin/env python3
"""Validate, score, profile, and prescribe an MSR assessment.

Usage:
  score.py <scores.json> [--rubric PATH] [--json] [--quiet]
  score.py <scores.json> --prescribe [--target 3|4] [--remediation PATH] [--json]

Each criterion uses one status:
  assessed       score 0..4, grade A/B/C, and evidence
  not_evidenced  searched scope; treated as 0 and counted as uncertainty
  not_applicable rationale; excluded from denominators
"""

import json
import os
import re
import sys
from statistics import mean


HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RUBRIC = os.path.join(HERE, "..", "references", "rubric.md")
DEFAULT_REMEDIATION = os.path.join(HERE, "..", "references", "remediation.md")

ARCHETYPES = {
    "configurable-application-platform",
    "agent-runtime",
    "developer-platform",
    "focused-application",
    "other",
}

MALLEABILITY = list("ABCDEFG") + ["I", "K", "N", "O"]
SELF_EVOLUTION = ["F", "J", "M"]
FACTORY = ["H", "L"]

PROFILES = {
    "Change Surface": list("ABCDO"),
    "Governance": ["E", "F"],
    "Factory": ["H", "L"],
    "Learning Loop": ["J", "M"],
    "Agent Interface": ["K"],
    "Extension Surface": ["I", "N"],
    "Operational Scalability": ["G"],
}

CLOSED_LOOP_FLOORS = ["F1", "F2", "F3", "J2", "M1", "M4", "L1"]


def band(value):
    if value is None:
        return "not scored"
    if value < 1.5:
        return "code-bound"
    if value < 2.5:
        return "engineer-configurable"
    if value <= 3.2:
        return "admin-configurable"
    return "generative and policy-gated"


def load_rubric(path):
    criteria = {}
    order = []
    dimension_titles = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            dimension = re.match(r"^## Dimension ([A-Z]): (.+)$", line.strip())
            if dimension:
                dimension_titles[dimension.group(1)] = dimension.group(2).strip()
            criterion = re.match(r"^### ([A-Z])(\d+) (.+)$", line.strip())
            if criterion:
                criterion_id = criterion.group(1) + criterion.group(2)
                criteria[criterion_id] = {
                    "dim": criterion.group(1),
                    "title": criterion.group(3).strip(),
                }
                order.append(criterion_id)
    if not criteria:
        raise SystemExit("Rubric has no criterion headings: " + path)
    return criteria, order, dimension_titles


def load_remediation(path):
    remediation = {}
    current = None
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            heading = re.match(r"^### ([A-Z]\d+)\s*$", line.strip())
            if heading:
                current = heading.group(1)
                remediation[current] = {
                    "to3": "",
                    "to4": "",
                    "requires": [],
                    "size": "",
                }
                continue
            if not current:
                continue
            for prefix, field in (("To 3:", "to3"), ("To 4:", "to4"), ("Size:", "size")):
                if line.startswith(prefix):
                    remediation[current][field] = line[len(prefix):].strip()
            if line.startswith("Requires:"):
                body = line[len("Requires:"):].strip()
                remediation[current]["requires"] = (
                    []
                    if body.lower().startswith("none")
                    else re.findall(r"\b([A-Z]\d+)\b", body.split(".")[0])
                )
    return remediation


def dimension_means(effective, criteria):
    dimensions = {}
    for criterion_id, value in effective.items():
        if value is not None:
            dimensions.setdefault(criteria[criterion_id]["dim"], []).append(value)
    return {dimension: round(mean(values), 1) for dimension, values in dimensions.items()}


def mean_for_dimensions(dimension_scores, dimensions):
    values = [dimension_scores[dimension] for dimension in dimensions if dimension in dimension_scores]
    return round(mean(values), 1) if values else None


def schedule_gaps(order, effective, remediation, target):
    gaps = [criterion for criterion in order if effective.get(criterion) is not None and effective[criterion] < target]
    missing = [criterion for criterion in gaps if criterion not in remediation]
    if missing:
        raise SystemExit("Remediation catalogue has no entry for: " + ", ".join(missing))

    scheduled = set()
    slices = []
    remaining = list(gaps)
    at_target = {
        criterion
        for criterion in order
        if effective.get(criterion) is not None and effective[criterion] >= target
    }
    excluded = {criterion for criterion in order if effective.get(criterion) is None}

    while remaining:
        ready = [
            criterion
            for criterion in remaining
            if all(
                requirement in at_target
                or requirement in scheduled
                or requirement in excluded
                for requirement in remediation[criterion]["requires"]
            )
        ]
        if not ready:
            ready = list(remaining)
        slices.append(ready)
        scheduled.update(ready)
        remaining = [criterion for criterion in remaining if criterion not in scheduled]
    return gaps, slices


def validate_and_score(data, criteria, order):
    errors = []
    flags = []
    effective = {}
    display = {}
    coverage = {"assessed": 0, "not_evidenced": 0, "not_applicable": 0}

    archetype = data.get("archetype")
    if archetype not in ARCHETYPES:
        errors.append("archetype must be one of: " + ", ".join(sorted(ARCHETYPES)))

    scores = data.get("scores", {})
    for criterion_id in order:
        if criterion_id not in scores:
            errors.append(f"{criterion_id}: missing")
            continue

        entry = scores[criterion_id]
        status = entry.get("status", "assessed")
        if status not in coverage:
            errors.append(f"{criterion_id}: unknown status {status!r}")
            continue
        coverage[status] += 1

        if status == "not_applicable":
            rationale = str(entry.get("rationale") or "").strip()
            if not rationale:
                errors.append(f"{criterion_id}: not_applicable requires rationale")
            effective[criterion_id] = None
            display[criterion_id] = rationale
            continue

        if status == "not_evidenced":
            searched = str(entry.get("searched") or "").strip()
            if not searched:
                errors.append(f"{criterion_id}: not_evidenced requires searched scope")
            effective[criterion_id] = 0
            display[criterion_id] = searched
            continue

        score = entry.get("score")
        grade = str(entry.get("grade", "")).upper()
        evidence = str(entry.get("evidence") or "").strip()
        if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 4:
            errors.append(f"{criterion_id}: score must be an integer 0..4, got {score!r}")
            continue
        if grade not in ("A", "B", "C"):
            errors.append(f"{criterion_id}: grade must be A, B or C, got {grade!r}")
            continue
        if not evidence:
            errors.append(f"{criterion_id}: assessed score {score} requires evidence")
            continue

        value = score
        if grade == "C" and value > 2:
            flags.append(f"{criterion_id}: grade C caps {value} -> 2")
            value = 2
        if entry.get("single_entity") and value > 2:
            flags.append(f"{criterion_id}: single-entity caps {value} -> 2")
            value = 2
        if entry.get("incident") and value > 0:
            flags.append(f"{criterion_id}: incident -1 ({value} -> {value - 1})")
            value -= 1
        effective[criterion_id] = value
        display[criterion_id] = evidence

    for unknown in sorted(set(scores) - set(order)):
        errors.append(f"{unknown}: not in rubric")

    return errors, flags, effective, display, coverage


def main(argv):
    if len(argv) < 2 or argv[1].startswith("-"):
        print(__doc__)
        return 1

    input_path = argv[1]
    rubric_path = argv[argv.index("--rubric") + 1] if "--rubric" in argv else DEFAULT_RUBRIC
    remediation_path = (
        argv[argv.index("--remediation") + 1]
        if "--remediation" in argv
        else DEFAULT_REMEDIATION
    )
    as_json = "--json" in argv
    quiet = "--quiet" in argv

    criteria, order, dimension_titles = load_rubric(rubric_path)
    with open(input_path, encoding="utf-8") as handle:
        data = json.load(handle)

    errors, flags, effective, display, coverage = validate_and_score(data, criteria, order)
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(" -", error)
        return 2

    dimensions = dimension_means(effective, criteria)
    indexes = {
        "malleability": mean_for_dimensions(dimensions, MALLEABILITY),
        "self_evolution": mean_for_dimensions(dimensions, SELF_EVOLUTION),
        "factory_readiness": mean_for_dimensions(dimensions, FACTORY),
    }
    profiles = {
        name: mean_for_dimensions(dimensions, profile_dimensions)
        for name, profile_dimensions in PROFILES.items()
    }
    closed_loop_candidate = all(
        effective.get(criterion) is not None and effective.get(criterion, 0) >= 2
        for criterion in CLOSED_LOOP_FLOORS
    )

    if "--prescribe" in argv:
        target = int(argv[argv.index("--target") + 1]) if "--target" in argv else 3
        if target not in (3, 4):
            raise SystemExit("--target must be 3 or 4")
        remediation = load_remediation(remediation_path)
        gaps, slices = schedule_gaps(order, effective, remediation, target)
        projected = {
            criterion: None if value is None else max(value, target)
            for criterion, value in effective.items()
        }
        projected_dimensions = dimension_means(projected, criteria)
        projected_indexes = {
            "malleability": mean_for_dimensions(projected_dimensions, MALLEABILITY),
            "self_evolution": mean_for_dimensions(projected_dimensions, SELF_EVOLUTION),
            "factory_readiness": mean_for_dimensions(projected_dimensions, FACTORY),
        }
        output = {
            "product": data.get("product"),
            "archetype": data.get("archetype"),
            "target": target,
            "gaps": len(gaps),
            "coverage": coverage,
            "slices": [
                [
                    {
                        "id": criterion,
                        "title": criteria[criterion]["title"],
                        "from": effective[criterion],
                        "size": remediation[criterion]["size"],
                        "requires": remediation[criterion]["requires"],
                        "move": remediation[criterion]["to3" if target == 3 else "to4"],
                    }
                    for criterion in slice_items
                ]
                for slice_items in slices
            ],
            "current": indexes,
            "projected": projected_indexes,
        }
        if as_json:
            print(json.dumps(output, indent=2))
            return 0

        print(f"# MSR prescription: {output['product']} to level {target}\n")
        print(f"{len(gaps)} applicable criteria are below {target}. Items inside a slice can proceed in parallel after prior slices.\n")
        for number, slice_items in enumerate(slices, 1):
            print(f"## Slice {number}\n")
            print("| Criterion | Now | Size | Requires | Move |\n|---|---:|---|---|---|")
            for criterion in slice_items:
                item = remediation[criterion]
                requirements = ", ".join(item["requires"]) or "none"
                move = item["to3" if target == 3 else "to4"]
                print(f"| {criterion} {criteria[criterion]['title']} | {effective[criterion]} | {item['size']} | {requirements} | {move} |")
            print()

        print("## Projected indexes if every move lands\n")
        print("| Index | Now | Projected |\n|---|---:|---:|")
        labels = {
            "malleability": "Malleability",
            "self_evolution": "Self-Evolution",
            "factory_readiness": "Factory Readiness",
        }
        for key, label in labels.items():
            print(f"| {label} | {indexes[key]} ({band(indexes[key])}) | {projected_indexes[key]} ({band(projected_indexes[key])}) |")
        print("\nProjected scores are ceilings, not delivery forecasts.")
        return 0

    result = {
        "product": data.get("product"),
        "date": data.get("date"),
        "source": data.get("source"),
        "archetype": data.get("archetype"),
        "coverage": coverage,
        "dimension_means": dimensions,
        "profiles": profiles,
        "effective_scores": effective,
        "malleability_index": indexes["malleability"],
        "self_evolution_index": indexes["self_evolution"],
        "factory_readiness_index": indexes["factory_readiness"],
        "band_malleability": band(indexes["malleability"]),
        "band_self_evolution": band(indexes["self_evolution"]),
        "band_factory": band(indexes["factory_readiness"]),
        "closed_loop_candidate": closed_loop_candidate,
        "closed_loop_floors": CLOSED_LOOP_FLOORS,
        "flags": flags,
        "criteria_in_rubric": len(order),
    }
    if as_json:
        print(json.dumps(result, indent=2))
        return 0

    if not quiet:
        print(f"# MSR assessment: {result['product']} ({result['date']}, {result['source']})\n")
        print(f"Archetype: **{result['archetype']}**\n")
        print("| Criterion | Status | Score | Grade | Evidence or rationale |\n|---|---|---:|---|---|")
        for criterion in order:
            entry = data["scores"][criterion]
            status = entry.get("status", "assessed")
            value = effective[criterion]
            score = "excluded" if value is None else str(value)
            grade = str(entry.get("grade", "" if status == "assessed" else "-")).upper() or "-"
            print(f"| {criterion} {criteria[criterion]['title']} | {status} | {score} | {grade} | {display[criterion]} |")

        print("\n## Profiles\n")
        print("| Profile | Score |\n|---|---:|")
        for name, value in profiles.items():
            print(f"| {name} | {value if value is not None else 'not scored'} |")

        print("\n## Dimension Means\n")
        print("| Dimension | Mean |\n|---|---:|")
        for dimension in sorted(dimensions):
            print(f"| {dimension} {dimension_titles.get(dimension, '')} | {dimensions[dimension]} |")

    print(f"\n**Malleability Index** {indexes['malleability']} ({band(indexes['malleability'])})")
    print(f"**Self-Evolution Index** {indexes['self_evolution']} ({band(indexes['self_evolution'])})")
    print(f"**Factory Readiness Index** {indexes['factory_readiness']} ({band(indexes['factory_readiness'])})")
    print(f"**Closed-loop candidate:** {'yes' if closed_loop_candidate else 'no'} (minimum mechanism signal only; operational validation required)")
    print(
        "**Coverage:** "
        f"{coverage['assessed']} assessed, "
        f"{coverage['not_evidenced']} not evidenced, "
        f"{coverage['not_applicable']} not applicable."
    )
    if flags:
        print("\nRules applied:")
        for flag in flags:
            print(" -", flag)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
