#!/usr/bin/env python3
"""Compare two or more EVOLVE assessments of the same product.

Usage:
  agreement.py A.json B.json [C.json ...] [--json] [--criteria ID,ID,...] [--labels a,b,...]

Reports, overall and per capability (the three-letter prefix of each criterion id):
criteria both raters assessed, exact agreement, agreement within one level, ranges that
overlap (score to alt_score), mean absolute difference, and criteria where one rater says
not applicable or not evidenced and the other assessed. Also: scope-fact disagreements,
the critical-control criteria listed separately, kinds of change, and the AI-qualified
readings compared the same way as scores. With three or more raters it adds "all the same"
and "all within one".

Tolerates older assessments without the v0.7 fields (change_kinds, confidence, basis) and
abbreviated files that hold only some criteria: a criterion missing from a file is counted
as "not in both files", never as a disagreement. Standard library only, deterministic.
"""

import argparse
import itertools
import json
import os
import re
import sys

CRITICAL = ("GOV-05", "DEL-11", "ARC-02", "ARC-09", "ARC-05", "GOV-04", "GOV-10", "LRN-08")
CAPABILITY_ORDER = ("ARC", "DEL", "MAL", "LRN", "GOV", "EXP", "AIR")
GENERIC_STEMS = {"assessment", "result", "scores", "input"}
STOPWORDS = {"and", "the", "for", "with", "from", "into", "that", "this", "what", "who", "new", "own", "its",
             "their", "change", "changes", "changing", "kind", "kinds"}
SHORT = {"assessed": None, "not_applicable": "n/a", "not_evidenced": "n/e", "missing": "–", "todo": "todo"}


# ----------------------------------------------------------------------------- loading

def load(path):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("scores", {}), dict):
        raise ValueError(f"{path}: not an assessment (expected an object with a 'scores' object)")
    return data


def default_labels(paths):
    stems = [os.path.splitext(os.path.basename(p))[0] for p in paths]
    if len(set(stems)) == len(stems) and not GENERIC_STEMS & set(stems):
        return stems
    labels = []
    for path in paths:
        parent = os.path.basename(os.path.dirname(os.path.abspath(path)))
        labels.append(f"{parent}/{os.path.splitext(os.path.basename(path))[0]}")
    return labels


def capability(cid):
    return cid.split("-", 1)[0]


def sort_key(cid):
    cap = capability(cid)
    rank = CAPABILITY_ORDER.index(cap) if cap in CAPABILITY_ORDER else len(CAPABILITY_ORDER)
    number = re.findall(r"\d+", cid)
    return rank, cap, int(number[0]) if number else 0, cid


def reading(entry):
    """Normalise one score or AI entry to {status, score, alt, evidence, confidence}."""
    if entry is None:
        return {"status": "missing"}
    if not isinstance(entry, dict):
        return {"status": "todo"}
    status = entry.get("status", "todo")
    out = {"status": status if status in ("assessed", "not_applicable", "not_evidenced") else "todo"}
    if out["status"] == "assessed":
        score = entry.get("score")
        if not isinstance(score, int) or isinstance(score, bool):
            return {"status": "todo"}
        out["score"] = score
        alt = entry.get("alt_score")
        out["alt"] = alt if isinstance(alt, int) and not isinstance(alt, bool) and alt > score else score
    text = entry.get("evidence") or entry.get("rationale") or entry.get("searched") or ""
    out["evidence"] = text if isinstance(text, str) else json.dumps(text)
    if entry.get("confidence"):
        out["confidence"] = entry["confidence"]
    return out


def readings(data, ai=False):
    out = {}
    for cid, entry in data.get("scores", {}).items():
        if ai:
            if isinstance(entry, dict) and "ai" in entry:
                out[cid] = reading(entry["ai"])
        else:
            out[cid] = reading(entry)
    return out


def fact_value(data, fact):
    entry = data.get("scope_facts", {}).get(fact)
    if isinstance(entry, dict):
        value = entry.get("value")
    else:
        value = entry
    return value if isinstance(value, bool) else None


def show(r):
    """Short text for one reading: the score, '2 (alt 3)', 'n/a', 'n/e' or '–'."""
    if r["status"] == "assessed":
        return str(r["score"]) + (f" (alt {r['alt']})" if r["alt"] != r["score"] else "")
    return SHORT.get(r["status"], r["status"])


# ----------------------------------------------------------------------------- maths

def pair_stats(ra, rb, ids):
    """Agreement between two raters over the given criterion ids."""
    stats = {"in_both_files": 0, "both_assessed": 0, "exact": 0, "within_one": 0, "ranges_overlap": 0,
             "mean_abs_diff": None, "both_not_applicable": 0, "both_not_evidenced": 0,
             "not_applicable_vs_assessed": [], "not_evidenced_vs_assessed": [], "not_applicable_vs_not_evidenced": [],
             "not_in_both_files": 0, "differ": []}
    diffs = []
    for cid in ids:
        a, b = ra.get(cid, {"status": "missing"}), rb.get(cid, {"status": "missing"})
        if a["status"] in ("missing", "todo") or b["status"] in ("missing", "todo"):
            if a["status"] != "missing" or b["status"] != "missing":
                stats["not_in_both_files"] += 1
            continue
        stats["in_both_files"] += 1
        pair = {a["status"], b["status"]}
        if pair == {"assessed"}:
            stats["both_assessed"] += 1
            diff = abs(a["score"] - b["score"])
            diffs.append(diff)
            stats["exact"] += diff == 0
            stats["within_one"] += diff <= 1
            stats["ranges_overlap"] += max(a["score"], b["score"]) <= min(a["alt"], b["alt"])
            if diff:
                stats["differ"].append(cid)
        elif pair == {"not_applicable"}:
            stats["both_not_applicable"] += 1
        elif pair == {"not_evidenced"}:
            stats["both_not_evidenced"] += 1
        elif pair == {"assessed", "not_applicable"}:
            stats["not_applicable_vs_assessed"].append(cid)
        elif pair == {"assessed", "not_evidenced"}:
            stats["not_evidenced_vs_assessed"].append(cid)
        else:
            stats["not_applicable_vs_not_evidenced"].append(cid)
    if diffs:
        stats["mean_abs_diff"] = round(sum(diffs) / len(diffs), 2)
    return stats


def group_stats(all_readings, ids):
    """For three or more raters: criteria every rater assessed, all the same, all within one."""
    out = {"all_assessed": 0, "all_same": 0, "all_within_one": 0, "status_differs": []}
    for cid in ids:
        rs = [r.get(cid, {"status": "missing"}) for r in all_readings]
        statuses = {r["status"] for r in rs}
        if statuses & {"missing", "todo"}:
            continue
        if statuses == {"assessed"}:
            scores = [r["score"] for r in rs]
            out["all_assessed"] += 1
            out["all_same"] += max(scores) == min(scores)
            out["all_within_one"] += max(scores) - min(scores) <= 1
        elif len(statuses) > 1:
            out["status_differs"].append(cid)
    return out


def by_capability(ids, fn):
    caps = []
    for cid in ids:
        if capability(cid) not in caps:
            caps.append(capability(cid))
    return {cap: fn([c for c in ids if capability(c) == cap]) for cap in caps}


def differences(labels, all_readings, ids):
    """Criteria where any two raters differ in status or score, with every rater's reading."""
    out = []
    for cid in ids:
        rs = [r.get(cid, {"status": "missing"}) for r in all_readings]
        present = [r for r in rs if r["status"] not in ("missing", "todo")]
        if len(present) < 2:
            continue
        keys = {(r["status"], r.get("score")) for r in present}
        if len(keys) > 1:
            scores = [r["score"] for r in present if r["status"] == "assessed"]
            out.append({"id": cid, "readings": {l: show(r) for l, r in zip(labels, rs)},
                        "spread": (max(scores) - min(scores)) if len(scores) > 1 else None,
                        "critical": cid in CRITICAL})
    return out


def tokens(text):
    return {w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(w) > 2 and w not in STOPWORDS}


def kinds_of(data):
    kinds = data.get("change_kinds")
    if not isinstance(kinds, list):
        return None
    out = []
    for k in kinds:
        if isinstance(k, dict):
            reach = k.get("reach")
            out.append({"id": str(k.get("id", "")), "name": str(k.get("name", "")), "main": k.get("main") is True,
                        "reach": reach if isinstance(reach, int) and not isinstance(reach, bool) else None})
    return out


def match_kinds(ka, kb):
    """Pair kinds by equal id, then equal name, then shared words (Jaccard >= 0.5). Deterministic."""
    pairs, used_a, used_b = [], set(), set()

    def take(i, j, how):
        pairs.append((i, j, how))
        used_a.add(i)
        used_b.add(j)

    for i, a in enumerate(ka):
        for j, b in enumerate(kb):
            if j not in used_b and i not in used_a and a["id"] and a["id"] == b["id"]:
                take(i, j, "id")
    for i, a in enumerate(ka):
        for j, b in enumerate(kb):
            if j not in used_b and i not in used_a and a["name"] and \
                    " ".join(sorted(tokens(a["name"]))) == " ".join(sorted(tokens(b["name"]))):
                take(i, j, "name")
    candidates = []
    for i, a in enumerate(ka):
        for j, b in enumerate(kb):
            ta, tb = tokens(a["id"].replace("-", " ") + " " + a["name"]), tokens(b["id"].replace("-", " ") + " " + b["name"])
            if ta and tb:
                score = len(ta & tb) / len(ta | tb)
                if score >= 0.5:
                    candidates.append((-score, i, j))
    for _neg, i, j in sorted(candidates):
        if i not in used_a and j not in used_b:
            take(i, j, "words")
    return sorted(pairs)


def kinds_pair(ka, kb):
    if ka is None or kb is None:
        return {"compared": False, "note": "change_kinds not recorded by "
                + ("either rater" if ka is None and kb is None else "one rater") + " (pre-v0.7 file)"}
    matched = []
    for i, j, how in match_kinds(ka, kb):
        a, b = ka[i], kb[j]
        matched.append({"a": a["id"], "b": b["id"], "how": how, "reach_a": a["reach"], "reach_b": b["reach"],
                        "main_a": a["main"], "main_b": b["main"]})
    with_reach = [m for m in matched if m["reach_a"] is not None and m["reach_b"] is not None]
    used_a = {m["a"] for m in matched}
    used_b = {m["b"] for m in matched}
    return {"compared": True, "count_a": len(ka), "count_b": len(kb),
            "main_a": sum(k["main"] for k in ka), "main_b": sum(k["main"] for k in kb),
            "matched": matched, "reach_exact": sum(m["reach_a"] == m["reach_b"] for m in with_reach),
            "reach_within_one": sum(abs(m["reach_a"] - m["reach_b"]) <= 1 for m in with_reach),
            "main_agree": sum(m["main_a"] == m["main_b"] for m in matched),
            "only_a": [k["id"] for k in ka if k["id"] not in used_a],
            "only_b": [k["id"] for k in kb if k["id"] not in used_b]}


# ----------------------------------------------------------------------------- report

def compare(paths, labels=None, criteria=None):
    docs = [load(p) for p in paths]
    labels = labels or default_labels(paths)
    if len(labels) != len(paths):
        raise ValueError("give one label per file")
    if len(set(labels)) != len(labels):
        raise ValueError("labels must be unique")
    warnings = []
    products = {str(d.get("product", "")).strip().lower() for d in docs}
    if len(products) > 1:
        warnings.append("The files name different products: "
                        + ", ".join(f"{l}: {d.get('product')!r}" for l, d in zip(labels, docs))
                        + ". Check they assess the same product.")
    bases = {d.get("basis", "shipped") for d in docs}
    if len(bases) > 1:
        warnings.append("The files mix a design reading and a shipped reading; they are not comparable.")
    shas = [re.findall(r"\b[0-9a-f]{7,40}\b", str(d.get("commit") or "") + " " + str(d.get("source") or ""))
            for d in docs]
    if all(shas) and not all(any(x.startswith(y) or y.startswith(x) for x in shas[0] for y in s) for s in shas[1:]):
        warnings.append("The files name different commits: "
                        + "; ".join(f"{l}: {', '.join(s)}" for l, s in zip(labels, shas)) + ".")

    score_r = [readings(d) for d in docs]
    ai_r = [readings(d, ai=True) for d in docs]
    ids = sorted(set().union(*[set(r) for r in score_r]), key=sort_key)
    ai_ids = sorted(set().union(*[set(r) for r in ai_r]), key=sort_key)
    if criteria:
        wanted = set(criteria)
        unknown = sorted(wanted - set(ids) - set(ai_ids))
        if unknown:
            warnings.append("Not found in any file: " + ", ".join(unknown) + ".")
        ids = [c for c in ids if c in wanted]
        ai_ids = [c for c in ai_ids if c in wanted]

    facts = []
    for d in docs:
        for f in d.get("scope_facts", {}):
            if f not in facts:
                facts.append(f)
    fact_rows = []
    for f in facts:
        values = [fact_value(d, f) for d in docs]
        known = {v for v in values if v is not None}
        fact_rows.append({"fact": f, "values": dict(zip(labels, values)),
                          "differ": len(known) > 1, "raters": sum(v is not None for v in values)})

    kinds = [kinds_of(d) for d in docs]
    raters = []
    for label, path, d, k in zip(labels, paths, docs, kinds):
        raters.append({"label": label, "path": path, "product": d.get("product"),
                       "criteria": len(d.get("scores", {})), "ai_readings": len(readings(d, ai=True)),
                       "scope_facts": len(d.get("scope_facts", {})),
                       "v07_fields": sorted(f for f in ("change_kinds", "basis", "proven", "ai_delivery") if f in d)
                       + (["confidence"] if any(isinstance(e, dict) and "confidence" in e
                                                for e in d.get("scores", {}).values()) else [])})

    pairs = []
    for (ia, la), (ib, lb) in itertools.combinations(enumerate(labels), 2):
        fa = [r for r in fact_rows if r["values"][la] is not None and r["values"][lb] is not None]
        pairs.append({
            "a": la, "b": lb,
            "scores": {"overall": pair_stats(score_r[ia], score_r[ib], ids),
                       "by_capability": by_capability(ids, lambda sub: pair_stats(score_r[ia], score_r[ib], sub))},
            "ai": {"overall": pair_stats(ai_r[ia], ai_r[ib], ai_ids),
                   "by_capability": by_capability(ai_ids, lambda sub: pair_stats(ai_r[ia], ai_r[ib], sub))},
            "scope_facts": {"compared": len(fa),
                            "differ": [r["fact"] for r in fa if r["values"][la] != r["values"][lb]]},
            "change_kinds": kinds_pair(kinds[ia], kinds[ib])})

    out = {"raters": raters, "warnings": warnings, "criteria_filter": sorted(criteria) if criteria else None,
           "criteria_compared": len(ids), "pairs": pairs}
    if len(docs) >= 3:
        out["all_raters"] = {
            "scores": {"overall": group_stats(score_r, ids),
                       "by_capability": by_capability(ids, lambda sub: group_stats(score_r, sub))},
            "ai": {"overall": group_stats(ai_r, ai_ids),
                   "by_capability": by_capability(ai_ids, lambda sub: group_stats(ai_r, sub))}}
    out["critical"] = []
    for cid in CRITICAL:
        if cid not in ids:
            continue
        rs = [r.get(cid, {"status": "missing"}) for r in score_r]
        present = {(r["status"], r.get("score")) for r in rs if r["status"] not in ("missing", "todo")}
        out["critical"].append({"id": cid, "readings": {l: show(r) for l, r in zip(labels, rs)},
                                "disagree": len(present) > 1})
    out["differences"] = differences(labels, score_r, ids)
    out["ai_differences"] = differences(labels, ai_r, ai_ids)
    out["scope_facts"] = fact_rows
    out["change_kinds"] = {l: k for l, k in zip(labels, kinds)}
    return out


def share(n, d):
    return f"{n} of {d} ({round(100 * n / d)}%)" if d else "–"


def stats_row(name, s):
    mad = "–" if s["mean_abs_diff"] is None else f"{s['mean_abs_diff']:.2f}"
    return (f"| {name} | {s['both_assessed']} | {share(s['exact'], s['both_assessed'])} | "
            f"{share(s['within_one'], s['both_assessed'])} | {share(s['ranges_overlap'], s['both_assessed'])} | {mad} | "
            f"{len(s['not_applicable_vs_assessed'])} | {len(s['not_evidenced_vs_assessed'])} | "
            f"{s['both_not_applicable']} | {s['not_in_both_files']} |")


STATS_HEAD = ("| {0} | Both assessed | Exact | Within one | Ranges overlap | Mean abs. diff. | "
              "One n/a, other assessed | One n/e, other assessed | Both n/a | Not in both files |\n"
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")


def render_block(lines, result, key, title):
    pairs = result["pairs"]
    lines += [f"## {title}", "", STATS_HEAD.format("Raters")]
    for p in pairs:
        lines.append(stats_row(f"{p['a']} · {p['b']}", p[key]["overall"]))
    lines.append("")
    mismatched = []
    for p in pairs:
        s = p[key]["overall"]
        for field, words in (("not_applicable_vs_assessed", "one not applicable, the other assessed"),
                             ("not_evidenced_vs_assessed", "one not evidenced, the other assessed"),
                             ("not_applicable_vs_not_evidenced", "one not applicable, the other not evidenced")):
            if s[field]:
                mismatched.append(f"- {p['a']} · {p['b']}, {words}: {', '.join(s[field])}")
    if mismatched:
        lines += ["Status mismatches:", ""] + mismatched + [""]
    if "all_raters" in result:
        g = result["all_raters"][key]["overall"]
        lines += [f"**All {len(result['raters'])} raters.** Assessed by all: {g['all_assessed']}. "
                  f"All the same: {share(g['all_same'], g['all_assessed'])}. "
                  f"All within one: {share(g['all_within_one'], g['all_assessed'])}."
                  + (f" Status differs: {', '.join(g['status_differs'])}." if g["status_differs"] else ""), ""]
    caps = list(pairs[0][key]["by_capability"]) if pairs else []
    if caps:
        lines += [f"### {title}, by capability", "", STATS_HEAD.format("Capability · raters")]
        for cap in caps:
            for p in pairs:
                lines.append(stats_row(f"{cap} · {p['a']} · {p['b']}", p[key]["by_capability"][cap]))
        if "all_raters" in result:
            lines += ["", "| Capability | Assessed by all | All the same | All within one |", "|---|---:|---:|---:|"]
            for cap in caps:
                g = result["all_raters"][key]["by_capability"][cap]
                lines.append(f"| {cap} | {g['all_assessed']} | {share(g['all_same'], g['all_assessed'])} | "
                             f"{share(g['all_within_one'], g['all_assessed'])} |")
        lines.append("")


def render(result):
    labels = [r["label"] for r in result["raters"]]
    product = result["raters"][0]["product"] or "unnamed product"
    lines = [f"# Rater agreement: {product}", ""]
    for w in result["warnings"]:
        lines.append(f"> **Warning.** {w}")
    if result["warnings"]:
        lines.append("")
    lines += ["| Rater | File | Criteria | AI readings | Scope facts | v0.7 fields |", "|---|---|---:|---:|---:|---|"]
    for r in result["raters"]:
        lines.append(f"| {r['label']} | `{r['path']}` | {r['criteria']} | {r['ai_readings']} | {r['scope_facts']} | "
                     f"{', '.join(r['v07_fields']) or 'none'} |")
    lines.append("")
    if result["criteria_filter"]:
        lines += [f"Filtered to {len(result['criteria_filter'])} criteria: {', '.join(result['criteria_filter'])}.", ""]
    render_block(lines, result, "scores", "Scores")

    head = "| Criterion | " + " | ".join(labels) + " |"
    rule = "|---|" + "---:|" * len(labels)
    lines += ["## Critical controls", "",
              "These criteria decide whether a loop can pass Level 3, so any disagreement is listed here.", ""]
    if result["critical"]:
        lines += [head[:-1] + "| Agree |", rule + "---|"]
        for c in result["critical"]:
            lines.append(f"| {c['id']} | " + " | ".join(c["readings"][l] for l in labels)
                         + f" | {'no' if c['disagree'] else 'yes'} |")
    else:
        lines.append("None of the critical-control criteria is in the comparison.")
    lines.append("")

    lines += ["## Where the raters differ", ""]
    if result["differences"]:
        lines += [head[:-1] + "| Spread |", rule + "---:|"]
        for d in result["differences"]:
            lines.append(f"| {d['id']}{' (critical)' if d['critical'] else ''} | "
                         + " | ".join(d["readings"][l] for l in labels)
                         + f" | {'–' if d['spread'] is None else d['spread']} |")
    else:
        lines.append("No differences in the criteria compared.")
    lines += ["", "n/a: not applicable. n/e: not evidenced. –: not in that file.", ""]

    lines += ["## Scope facts", ""]
    differ = [r for r in result["scope_facts"] if r["differ"]]
    compared = [r for r in result["scope_facts"] if r["raters"] >= 2]
    lines.append(f"{len(differ)} of {len(compared)} facts recorded by two or more raters differ.")
    if differ:
        lines += ["", "| Fact | " + " | ".join(labels) + " |", "|---|" + "---|" * len(labels)]
        for r in differ:
            lines.append(f"| `{r['fact']}` | " + " | ".join(
                "–" if r["values"][l] is None else str(r["values"][l]).lower() for l in labels) + " |")
    lines.append("")

    lines += ["## Kinds of change", ""]
    for p in result["pairs"]:
        k = p["change_kinds"]
        if not k["compared"]:
            lines.append(f"- {p['a']} · {p['b']}: {k['note']}.")
            continue
        lines.append(f"- {p['a']} · {p['b']}: {k['count_a']} and {k['count_b']} kinds; {k['main_a']} and {k['main_b']} "
                     f"main; {len(k['matched'])} matched (by id, name or shared words), reach the same on {k['reach_exact']} and "
                     f"within one on {k['reach_within_one']}; main the same on {k['main_agree']}.")
        for m in k["matched"]:
            lines.append(f"  - `{m['a']}` / `{m['b']}` (by {m['how']}): reach {m['reach_a']} / {m['reach_b']}, "
                         f"main {str(m['main_a']).lower()} / {str(m['main_b']).lower()}")
        if k["only_a"] or k["only_b"]:
            lines.append(f"  - unmatched: {', '.join(k['only_a']) or 'none'} / {', '.join(k['only_b']) or 'none'}")
    lines.append("")

    if any(p["ai"]["overall"]["in_both_files"] or p["ai"]["overall"]["not_in_both_files"] for p in result["pairs"]):
        render_block(lines, result, "ai", "AI-qualified readings")
        if result["ai_differences"]:
            lines += ["### AI readings where the raters differ", "", head[:-1] + "| Spread |", rule + "---:|"]
            for d in result["ai_differences"]:
                lines.append(f"| {d['id']} | " + " | ".join(d["readings"][l] for l in labels)
                             + f" | {'–' if d['spread'] is None else d['spread']} |")
            lines.append("")
    else:
        lines += ["## AI-qualified readings", "", "No AI readings in the files compared.", ""]
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compare two or more EVOLVE assessments of the same product.")
    parser.add_argument("assessments", nargs="+")
    parser.add_argument("--json", action="store_true", help="print the comparison as JSON")
    parser.add_argument("--criteria", help="comma-separated criterion ids to compare, for example GOV-05,ARC-09")
    parser.add_argument("--labels", help="comma-separated rater labels, one per file")
    args = parser.parse_args(argv)
    if len(args.assessments) < 2:
        parser.error("give at least two assessments")
    criteria = [c.strip().upper() for c in args.criteria.split(",") if c.strip()] if args.criteria else None
    labels = [l.strip() for l in args.labels.split(",")] if args.labels else None
    try:
        result = compare(args.assessments, labels, criteria)
    except (OSError, ValueError) as exc:  # json.JSONDecodeError is a ValueError
        print(f"Cannot compare: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        sys.stdout.write(render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
