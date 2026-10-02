#!/usr/bin/env python3
"""Build result.json, scorecard.md and evidence.md for every assessed system,
then comparison.md across systems. All numbers come from scripts/score.py.

Usage: python3 tools/build.py   (run from this folder)
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(ROOT))
SCORER = os.path.join(REPO, "scripts", "score.py")
sys.path.insert(0, os.path.join(REPO, "scripts"))
import score as evolve  # noqa: E402

SYSTEMS = ["frappe", "directus", "discourse", "posthog", "n8n", "dify", "librechat",
           "hermes-agent", "openclaw", "opencode", "openhands"]


def f1(x):
    return "–" if x is None else f"{x:.1f}"


def build(system, criteria, order, model):
    folder = os.path.join(ROOT, system)
    path = os.path.join(folder, "assessment.json")
    with open(path) as handle:
        data = json.load(handle)
    js = subprocess.run([sys.executable, SCORER, path, "--json"], capture_output=True, text=True)
    if js.returncode:
        raise SystemExit(f"{system}: {js.stdout}{js.stderr}")
    result = json.loads(js.stdout)
    with open(os.path.join(folder, "result.json"), "w") as h:
        h.write(js.stdout)
    md = subprocess.run([sys.executable, SCORER, path], capture_output=True, text=True).stdout
    head = [f"# {data['product']}: EVOLVE v{model['version'].rsplit('.', 1)[0]} scorecard", "",
            f"Evaluator: Claude, single rater. Framework: EVOLVE {model['version']} in this repository.", "",
            data.get("scope_line", ""), "", "## Reading", "", data.get("reading", "_Not written._"), "",
            "## Limits", "", data.get("limits", ""), "", "---", ""]
    with open(os.path.join(folder, "scorecard.md"), "w") as h:
        h.write(("\n".join(head) + md.split("\n", 2)[2]).rstrip("\n") + "\n")
    ev = [f"# {data['product']} evidence", "",
          f"Read at {data['source']} on {data['date']}. Grade A is code at the tip, B is in-repository documentation.", "",
          "## Scope facts", ""]
    for fact in model["scope_facts"]:
        entry = data["scope_facts"][fact]
        value = "true" if entry["value"] else "false"
        if "available_value" in entry and entry["available_value"] != entry["value"]:
            value += f" by default, {'true' if entry['available_value'] else 'false'} with opt-in settings"
        ev.append(f"- **{fact}**: {value}. {entry['evidence']}")
    cap, area = None, None
    for cid in order:
        if criteria[cid]["cap"] != cap:
            cap = criteria[cid]["cap"]
            name = model["capabilities"].get(cap, "AI Readiness Checks")
            ev += ["", f"## {name} ({cap})"]
        if criteria[cid]["area"] != area:
            area = criteria[cid]["area"]
            ev += ["", f"### {area}", ""]
        e = data["scores"][cid]
        ev.append(f"- **{cid} {criteria[cid]['title']}**: " + describe(e))
        if "inventory" in e:
            ev.append("  - Inventory: " + ", ".join(f"{k} {v}" for k, v in e["inventory"].items()))
        if "alt_score" in e:
            ev.append(f"  - Higher reading {e['alt_score']}: {e.get('alt_note', '')}")
        if "ai" in e:
            ev.append("  - AI-qualified reading: " + describe(e["ai"]))
            if "alt_score" in e["ai"]:
                ev.append(f"    - Higher reading {e['ai']['alt_score']}: {e['ai'].get('alt_note', '')}")
    with open(os.path.join(folder, "evidence.md"), "w") as h:
        h.write("\n".join(ev) + "\n")
    return data, result


def describe(e):
    st = e["status"]
    if st == "assessed":
        head_txt = f"**{e['score']}** (grade {e['grade']})"
        if "available_score" in e:
            head_txt += f", **{e['available_score']}** with opt-in settings"
        if "facets" in e:
            head_txt += ", facets: " + ", ".join(k for k in evolve.FACETS if e["facets"][k])
        body = e["evidence"]
    elif st == "not_evidenced":
        head_txt, body = "**not evidenced**", "Searched: " + e["searched"]
    else:
        head_txt = "**not applicable**"
        body = e["rationale"] + (f" If counted: {e['if_applicable']}." if "if_applicable" in e else "")
    return f"{head_txt}. {body}"


def fact_cell(entry):
    yn = lambda v: "yes" if v else "no"
    if "available_value" in entry and entry["available_value"] != entry["value"]:
        return f"{yn(entry['value'])} → {yn(entry['available_value'])}"
    return yn(entry["value"])


def ai_level(result):
    for variant in ("default", "available"):
        view = result["ai_readiness"][variant]
        if view["status"] == "assessed":
            return view["level"]
    return -1


def main():
    criteria, order, model = evolve.load_rubric(os.path.join(REPO, "references", "rubric.md"))
    with open(os.path.join(HERE, "v03_comparison.json")) as handle:
        v03 = json.load(handle)["systems"]
    rows = {s: build(s, criteria, order, model) for s in SYSTEMS}
    loops = list(model["loops"])

    def sal_key(s):
        r = rows[s][1]
        return (-r["sal"]["headline"], -sum(r["sal"]["loops"][l]["level"] for l in loops), s)

    ranked = sorted(SYSTEMS, key=sal_key)
    L = ["# Comparison: EVOLVE v0.5", "", "Generated by `tools/build.py`. Every number comes from `scripts/score.py`.", "",
         "## Software Autonomy Level (default configuration)", "",
         "Each loop shows its level and how many of the next level's applicable conditions it already meets.", "",
         "| System | Archetype | SAL | Request → Release | Issue → Fix | Opportunity → Expansion | SAL with opt-in settings | SAL with every alternate reading |",
         "|---|---|---:|---|---|---|---:|---:|"]
    for s in ranked:
        d, r = rows[s]
        lv = r["sal"]["loops"]
        L.append(f"| {d['product']} | {d['archetype']} | **{r['sal']['headline']}** | "
                 + " | ".join(f"L{lv[l]['level']} ({lv[l]['next_met']}/{lv[l]['next_total']})" if lv[l]["next_total"]
                              else f"L{lv[l]['level']}" for l in loops)
                 + f" | {r['variants']['available']['sal']['headline']} | {r['variants']['high']['sal']['headline']} |")
    L += ["", "## What holds each loop at its level", "",
          "A loop's level is the lowest of its four parts. Each cell names the parts with an unmet condition for the next level.", "",
          "| System | Request → Release | Issue → Fix | Opportunity → Expansion |", "|---|---|---|---|"]
    for s in ranked:
        d, r = rows[s]
        cells = []
        for l in loops:
            weak = sorted({b["part"] for b in r["sal"]["loops"][l]["blockers"]})
            cells.append(", ".join(weak) or "top level")
        L.append(f"| {d['product']} | " + " | ".join(cells) + " |")
    L += ["", "## Sensitivity of the headline", "",
          "Criteria whose one-level change would move the headline SAL. A long first column means a fragile headline.", "",
          "| System | Headline drops if any of these falls one level | Headline rises if any of these rises one level |",
          "|---|---|---|"]
    for s in ranked:
        d, r = rows[s]
        sens = r["sensitivity"]
        L.append(f"| {d['product']} | {', '.join(sens['lower_headline']) or 'none'} | {', '.join(sens['raise_headline']) or 'none'} |")
    controls = [c["control"] for c in rows[SYSTEMS[0]][1]["sal"]["controls"]]
    L += ["", "## Critical controls", "", "A failed applicable control caps every loop at L2.", "",
          "| System | " + " | ".join(controls) + " |", "|---|" + "---|" * len(controls)]
    for s in ranked:
        d, r = rows[s]
        status = {c["control"]: c["status"] for c in r["sal"]["controls"]}
        L.append(f"| {d['product']} | " + " | ".join(status[c] for c in controls) + " |")
    caps = list(model["capabilities"])
    L += ["", "## EVOLVE profile (default, with the range from alternate readings)", "",
          "| System | " + " | ".join(f"{model['capabilities'][c]} ({c})" for c in caps) + " |", "|---|" + "---|" * len(caps)]
    for s in ranked:
        d, r = rows[s]
        cells = []
        for c in caps:
            v, rg = r["capabilities"][c], r["ranges"][c]
            cells.append(f1(v) if rg is None or f1(rg[0]) == f1(rg[1]) else f"{f1(v)} ({f1(rg[0])}–{f1(rg[1])})")
        L.append(f"| {d['product']} | " + " | ".join(cells) + " |")
    ai_rank = sorted(SYSTEMS, key=lambda s: (-ai_level(rows[s][1]), s))
    dims = list(model["ai_view"]["dimensions"])
    L += ["", "## AI Readiness (provisional, single rater)", "",
          "How safely each product runs AI in production. Separate from SAL, which it never changes. "
          "The headline is the weakest dimension, capped at L2 when a gate fails. "
          "Where AI is off by default, the row says so and shows the opt-in reading. The last column uses the default configuration.", "",
          "| System | AI Readiness | " + " | ".join(dims) + " | Gates (access / evals / traces) | With every alternate reading |",
          "|---|---|" + "---:|" * len(dims) + "---|---:|"]
    for s in ai_rank:
        d, r = rows[s]
        v = r["ai_readiness"]
        shown, note = (v["default"], "") if v["default"]["status"] == "assessed" else (v["available"], " (opt-in)")
        if shown["status"] != "assessed":
            L.append(f"| {d['product']} | no AI features | " + " | ".join("–" for _ in dims) + " | – | – |")
            continue
        head = (f"**L{shown['level']}** {shown['name']}" if not note
                else f"no AI by default; **L{shown['level']}** {shown['name']} with opt-in")
        cells = ["n/a" if shown["dimensions"][n]["level"] is None else str(shown["dimensions"][n]["level"]) for n in dims]
        gates = " / ".join("n/a" if g["status"] == "not_applicable" else g["status"] for g in shown["gates"])
        hi = v["high"] if v["high"]["status"] == "assessed" else None
        L.append(f"| {d['product']} | {head} | " + " | ".join(cells) + f" | {gates} | {'L' + str(hi['level']) if hi else '–'} |")
    areas = list(model["ai_view"]["footprint"])
    L += ["", "## AI Capability Footprint (descriptive, non-headline)", "",
          "What each product's AI does, by area, with opt-in settings. Each level is descriptive: there is no footprint headline, and it never changes AI Readiness or SAL.", "",
          "| System | " + " | ".join(areas) + " |", "|---|" + "---:|" * len(areas)]
    for s in ai_rank:
        d, r = rows[s]
        fp = r["ai_readiness"]["available"]["footprint"]
        if ai_level(r) < 0:
            L.append(f"| {d['product']} | " + " | ".join("–" for _ in areas) + " |")
            continue
        L.append(f"| {d['product']} | " + " | ".join("–" if fp[a]["level"] is None else str(fp[a]["level"]) for a in areas) + " |")
    L += ["", "## Scope facts", "", "Default value; where a shipped opt-in setting changes a fact, the cell reads default → with opt-in.", "",
          "| System | " + " | ".join(model["scope_facts"]) + " |",
          "|---|" + "---|" * len(model["scope_facts"])]
    for s in ranked:
        d, r = rows[s]
        L.append(f"| {d['product']} | " + " | ".join(fact_cell(d["scope_facts"][f]) for f in model["scope_facts"]) + " |")
    L += ["", "## Same systems under v0.3", "",
          "v0.3 reported four non-overlapping indexes and a closed-loop flag. EVOLVE reports loop levels and a six-capability profile, "
          "so the columns are not directly comparable.", "",
          "| System | v0.3 Malleability | v0.3 Governance | v0.3 Learning | v0.3 Factory | v0.3 closed loop (default / opt-in) | v0.5 SAL |",
          "|---|---:|---:|---:|---:|---|---:|"]
    for s in ranked:
        d, r = rows[s]
        o = v03[s]
        i = o["indexes"]
        L.append(f"| {d['product']} | {f1(i['malleability'])} | {f1(i['governance'])} | {f1(i['learning'])} | {f1(i['factory'])} | "
                 f"{'yes' if o['closed_loop_candidate'] else 'no'} / {'yes' if o['closed_loop_candidate_opt_in'] else 'no'} | "
                 f"{r['sal']['headline']} |")
    with open(os.path.join(ROOT, "comparison.md"), "w") as h:
        h.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
