#!/usr/bin/env python3
"""Print a plain-language EVOLVE report for business and product readers.

Usage:
  report.py ASSESSMENT.json [--json] [--rubric PATH] [--plain PATH]

The scorer (score.py) computes every reading; this script only puts it into words. All names, questions
and gap sentences come from references/plain-language.md, and the script refuses to run when an entry it
may need is missing. The body of the report (every section before "For engineers") never contains a
criterion code or engineering jargon: if it would, the script stops with an error, because that means
the plain-language file or this template has a defect. Codes appear only in the "For engineers" appendix.

Sections, in order: In one paragraph; Where it stands; The kinds of change; What works today; What holds
it back; Safety gates; How much AI does; Does the loop improve itself; Has it been proven; How sure this
reading is; What to do next; For engineers.

--json prints the same content as data: each section's blocks (paragraphs, lists and tables, in the same
words) and the readings behind them. render() turns that data back into the Markdown report.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import score  # noqa: E402

DEFAULT_PLAIN = os.path.join(HERE, "..", "references", "plain-language.md")

SECTIONS = (
    ("summary", "In one paragraph"),
    ("stands", "Where it stands"),
    ("kinds", "The kinds of change"),
    ("works", "What works today"),
    ("holds", "What holds it back"),
    ("gates", "Safety gates"),
    ("ai", "How much AI does"),
    ("recursion", "Does the loop improve itself"),
    ("proven", "Has it been proven"),
    ("confidence", "How sure this reading is"),
    ("next", "What to do next"),
    ("engineers", "For engineers"),
)
ENGINEERS = "engineers"  # the only section where codes may appear

CODE = re.compile(r"[A-Z]{3}-\d\d")
BANNED = re.compile(r"\b(?:roll-?backs?|tenan\w*|schema\w*|migration\w*|crud|ddl|canar(?:y|ies)|idempoten\w*|"
                    r"telemetry|\w*deploy\w*|pipelines?|provenance)\b", re.I)

# The model's challenge texts are written for engineers. These replacements put the few engineering words
# they contain into the plain-language file's own terms; anything else that slips through is caught by the
# guard, which then names the line.
CHALLENGE_WORDS = (
    ("code change or redeploy", "code change or new release"),
    ("show that tenants cannot reach each other (where there are tenants)",
     "show that customer organisations cannot reach each other's data (where there are several)"),
    ("in a real deployment", "in real use"),
)

STRONG = 3          # a criterion at this default score or more counts as working today
NAMES_PER_LINE = 4  # strongest criteria named per capability in "What works today"
GRADE_WORDS = (
    ("A", "checked in the code"),
    ("B", "taken from the product's own documents or settings"),
    ("C", "inferred from other material"),
    ("D", "taken from design documents"),
)
CONFIDENCE_WORDS = {"high": "the rater read the code and its tests",
                    "medium": "the rater read the code, but not every path through it",
                    "low": "inferred from part of the evidence"}
CONTROL_STATUS = {"pass": "Passed", "fail": "Not yet", "n/a": "Does not apply"}


class PlainLanguageError(Exception):
    """plain-language.md lacks an entry or field the report may need."""


class ReportDefect(Exception):
    """Generated body text contains a code or a banned word."""


# ---------------------------------------------------------------- plain language

def load_plain(path):
    """{section: {key: {field: value}}} from `## ` sections, `### ` keys and `Field: value` lines."""
    plain, section, key = {}, None, None
    with open(path, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.rstrip("\n")
            if line.startswith("## "):
                section, key = line[3:].strip(), None
                plain.setdefault(section, {})
                continue
            if line.startswith("### "):
                if section is None:
                    raise PlainLanguageError(f"{path}: entry {line[4:].strip()!r} is outside a section")
                key = line[4:].strip()
                plain[section][key] = {}
                continue
            field = re.match(r"^([A-Z][A-Za-z ]*?):\s+(.+)$", line)
            if field and section and key:
                plain[section][key][field.group(1)] = field.group(2).strip()
    return plain


def required_entries(criteria, order, model):
    """[(section, key, fields)] for every entry a report may need."""
    need = [("Levels", f"L{n}", ("Name", "Product", "People")) for n in range(len(model["levels"]))]
    need += [("Loops", loop, ("Name", "Question")) for loop in model["loops"]]
    need += [("Parts", part, ("Name", "Meaning")) for part in score.PARTS]
    stages, controls = [], []
    for conds in model["conditions"].values():
        for cond in conds:
            stages.append(cond["stage"])
            if cond.get("control"):
                controls.append(cond["control"])
    need += [("Stages", s, ("Name",)) for s in dict.fromkeys(stages)]
    need += [("Controls", c, ("Name", "Why")) for c in dict.fromkeys(controls)]
    caps = list(model["capabilities"]) + sorted({criteria[c]["cap"] for c in order} - set(model["capabilities"]))
    need += [("Capabilities", c, ("Name", "Asks")) for c in caps]
    need += [("Scope facts", f, ("Name",)) for f in model["scope_facts"]]
    need += [("Reach", str(n), ("Name", "Meaning")) for n in range(len(model["reach"]))]
    need += [("Recursion", str(n), ("Name", "Meaning")) for n in range(len(model["recursion"]))]
    view = model.get("ai_view")
    if view:
        need += [("AI readiness", d, ("Name", "Asks")) for d in view["dimensions"]]
        need += [("AI readiness", g["gate"], ("Name", "Asks")) for g in view["gates"]]
    need += [("Criteria", c, ("Name", "Question", "Gap")) for c in order]
    return need


def check_plain(plain, criteria, order, model):
    """Every missing entry or field, as text; empty when the file is complete."""
    missing = []
    for section, key, fields in required_entries(criteria, order, model):
        entry = plain.get(section, {}).get(key)
        if entry is None:
            missing.append(f"## {section} / ### {key}: missing")
            continue
        absent = [f for f in fields if not entry.get(f)]
        if absent:
            missing.append(f"## {section} / ### {key}: needs {', '.join(absent)}")
    return missing


# ---------------------------------------------------------------- words

def lower_first(text):
    """Lower-case the first letter of a sentence, unless it starts an acronym such as AI."""
    if len(text) > 1 and text[0].isupper() and not text[1].isupper():
        return text[0].lower() + text[1:]
    return text


def join_names(names):
    """'a, b and c'; or 'a; b; c' when a name has its own comma or 'and', so the list stays unambiguous."""
    names = list(names)
    if len(names) <= 1:
        return "".join(names)
    if any("," in n or " and " in n for n in names):
        return "; ".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


class Words:
    """Plain-language lookups."""

    def __init__(self, plain, model):
        self.p, self.model = plain, model

    def level(self, n):
        return self.p["Levels"][f"L{n}"]

    def level_name(self, n):
        return f"Level {n}, {self.level(n)['Name']}"

    def loop(self, loop):
        return self.p["Loops"][loop]["Name"]

    def crit(self, cid):
        return self.p["Criteria"][cid]

    def control(self, name):
        return self.p["Controls"][name]

    def stage(self, name):
        return self.p["Stages"][name]["Name"]

    def part(self, name):
        return self.p["Parts"][name]

    def cap(self, cap):
        return self.p["Capabilities"][cap]["Name"]

    def reach(self, n):
        return self.p["Reach"][str(n)]

    def recursion(self, n):
        return self.p["Recursion"][str(n)]

    def ai(self, key):
        return self.p["AI readiness"][key]

    def fact(self, key):
        return self.p["Scope facts"][key]["Name"]


def para(text):
    return {"type": "paragraph", "text": text}


def bullets(items):
    return {"type": "list", "items": list(items)}


def table(header, rows):
    return {"type": "table", "header": list(header), "rows": [list(r) for r in rows]}


# ---------------------------------------------------------------- what holds it back

def _kinds_not_self_serve(data):
    return [k["name"] for k in data["change_kinds"] if k.get("main") and k.get("reach", 0) < 1]


def _needs(cond, loop, ev, data, model, words):
    """The atomic things a failing condition lacks: [(key, sentence, codes)]."""
    if "c" in cond:
        return [(cond["c"], words.crit(cond["c"])["Gap"], [cond["c"]])]
    if "path" in cond:
        # The first way up names the gap; the other ways up appear for engineers.
        alt = model["build_paths"][loop][cond["path"]][0]
        if "kinds" in alt:
            return [("kinds", "Not every main kind of change can be made by the people running the product: "
                              + join_names(_kinds_not_self_serve(data)) + ".", [])]
        return [(alt["c"], words.crit(alt["c"])["Gap"], [alt["c"]])]
    if "rollback" in cond:
        out = []
        for item in model["rollback"]:
            if item.get("when") and ev.facts.get(item["when"]) is not True:
                continue
            ok, _ = ev._crit(item["c"], cond["rollback"])
            if not ok:
                out.append((item["c"], words.crit(item["c"])["Gap"], [item["c"]]))
        return out
    if "every" in cond:
        out = []
        for ids in model["areas"][cond["every"]].values():
            for cid in ids:
                ok, _ = ev._crit(cid, cond["min"])
                if not ok:
                    out.append((cid, words.crit(cid)["Gap"], [cid]))
        return out
    if "all" in cond:
        out = []
        for sub in cond["all"]:
            if not ev.test(sub, loop)[0]:
                out += _needs(sub, loop, ev, data, model, words)
        return out
    if "any" in cond:
        first = _needs(cond["any"][0], loop, ev, data, model, words)
        if any("path" in sub and sub["path"] == "product" for sub in cond["any"][1:]):
            first = [(key, text + " Nor does the product build the change itself yet.", codes)
                     for key, text, codes in first]
        return first
    raise score.ModelError(f"Unrecognised condition: {cond}")


def holds_back(data, model, default, words):
    """Next-level gaps for every loop, deduplicated across loops and ordered by how many loops each holds."""
    ev = score.Evaluator(data, default["effective"], default["capabilities"], model)
    sal, top = default["sal"], len(model["levels"]) - 1
    items, order = {}, 0
    for loop in model["loops"]:
        level = sal["loops"][loop]["level"]
        if level >= top:
            continue
        for cond in model["conditions"].get(str(level + 1), []):
            if cond.get("loop") not in (None, loop) or ev.test(cond, loop)[0]:
                continue
            for key, text, codes in _needs(cond, loop, ev, data, model, words):
                item = items.get(key)
                if item is None:
                    item = items[key] = {"key": key, "stage": cond["stage"], "stage_name": words.stage(cond["stage"]),
                                         "text": text, "codes": codes, "loops": [], "first": order}
                    order += 1
                if loop not in [l["loop"] for l in item["loops"]]:
                    item["loops"].append({"loop": loop, "to": level + 1})
    ranked = sorted(items.values(), key=lambda i: (-len(i["loops"]), i["first"]))
    for item in ranked:
        del item["first"]
    return ranked


def _loops_text(item, words, model):
    if len(item["loops"]) == len(model["loops"]):
        return "Holds back all three loops." if len(model["loops"]) == 3 else "Holds back every loop."
    return "Holds back: " + "; ".join(f"{words.loop(l['loop'])}, on the way to Level {l['to']}"
                                      for l in item["loops"]) + "."


# ---------------------------------------------------------------- sections

def build_report(data, criteria, order, model, plain, result=None):
    """The whole report as data: {"product", ..., "sections": [{"id", "title", "blocks", "data"}]}."""
    words = Words(plain, model)
    result = result or score.score_assessment(data, criteria, order, model)
    default = result["variants"]["default"]
    sal = default["sal"]
    design = result["basis"] == "design"
    claim = "Designed for" if design else "Built to"
    top = len(model["levels"]) - 1
    headline = sal["headline"]
    blocks_held = holds_back(data, model, default, words)
    headline_loops = list(model["headline"])
    sections = {}

    # 1. In one paragraph
    lvl = words.level(headline)
    text = f"{claim} {words.level_name(headline)}: {lower_first(lvl['Product'])}"
    proven = result["proven"]
    if design:
        text += " " + score.DESIGN_NOTE
    elif proven["headline"] is None:
        text += " Not yet proven in operation."
    else:
        text += f" Proven in operation at {words.level_name(proven['headline'])}."
    text += (" As designed, " if design else " In practice, ") + lower_first(lvl["People"])
    biggest = next((i for i in blocks_held
                    if any(l["loop"] in headline_loops and l["to"] == headline + 1 for l in i["loops"])),
                   blocks_held[0] if blocks_held else None)
    if headline >= top:
        text += " It is at the top level, so nothing holds it back."
    elif biggest:
        text += " The biggest thing holding it back is that " + lower_first(biggest["text"])
    sections["summary"] = {"blocks": [para(text)],
                           "data": {"claim": claim, "level": headline, "name": lvl["Name"],
                                    "proven": None if design else proven["headline"],
                                    "biggest": biggest and biggest["key"]}}

    # 2. Where it stands
    blocks = [para("The product is read on three loops. Its overall level is the lower of the first two; the "
                   "third is reported beside it.")]
    loops_data = {}
    for loop in model["loops"]:
        info = sal["loops"][loop]
        n = info["level"]
        lines = [f"{claim} {words.level_name(n)}. {words.level(n)['Product']}"]
        if n < top:
            held = [lower_first(words.part(p)["Name"]) for p in score.PARTS if info["parts"][p] == n]
            lines.append("Held at this level by " + join_names(held) + ".")
        if not design:
            p = proven["loops"][loop]
            lines.append("Proven: not evidenced." if p["level"] is None
                         else f"Proven at {words.level_name(p['level'])}.")
        blocks.append(para(f"**{words.loop(loop)}.** {plain['Loops'][loop]['Question']}"))
        blocks.append(bullets(lines))
        loops_data[loop] = {"level": n, "name": words.level(n)["Name"],
                            "proven": None if design else proven["loops"][loop]["level"]}
    if design:
        blocks.append(para("This is a design reading. " + score.DESIGN_NOTE))
    else:
        blocks.append(para("Built to says what the product ships and can do. Proven says what operating records "
                           "show it has done. The two are reported separately and never added together."))
    sections["stands"] = {"blocks": blocks, "data": {"basis": result["basis"], "loops": loops_data}}

    # 3. The kinds of change
    rows = []
    for kind in data["change_kinds"]:
        reach = words.reach(kind["reach"])
        rows.append([kind["name"], kind["who"], f"{reach['Name']}. {reach['Meaning']}",
                     "Yes" if kind["main"] else "No"])
    kinds = result["kinds"]
    serve = words.reach(1)
    sections["kinds"] = {
        "blocks": [para("The changes the people running the product most often need, and how far each has come."),
                   table(("Kind of change", "Who makes it", "How far it has come", "Main kind"), rows),
                   para(f"{kinds['text']}. "
                        f"Self-serve means: {lower_first(serve['Meaning'])}")],
        "data": {"kinds": [{"id": k["id"], "name": k["name"], "who": k["who"], "main": k["main"],
                            "reach": k["reach"], "reach_name": words.reach(k["reach"])["Name"]}
                           for k in data["change_kinds"]],
                 "main": kinds["main"], "main_self_serve": kinds["main_self_serve"]}}

    # 4. What works today
    strong = [c for c in order if data["scores"][c]["status"] == "assessed"
              and (default["effective"].get(c) or 0) >= STRONG]
    caps = list(model["capabilities"]) + sorted({criteria[c]["cap"] for c in order} - set(model["capabilities"]))
    lines, works = [], {}
    for cap in caps:
        ids = sorted((c for c in strong if criteria[c]["cap"] == cap),
                     key=lambda c: (-default["effective"][c], order.index(c)))
        if not ids:
            continue
        names = [words.crit(c)["Name"] for c in ids]
        shown = "; ".join(names[:NAMES_PER_LINE])
        if len(names) > NAMES_PER_LINE:
            shown += f"; and {len(names) - NAMES_PER_LINE} more"
        lines.append(f"**{words.cap(cap)}:** {shown}.")
        works[cap] = ids
    if lines:
        blocks = [para("The strongest parts of the product, rated 3 or more out of 4."), bullets(lines)]
    else:
        blocks = [para("Nothing is yet rated strong (3 or more out of 4).")]
    sections["works"] = {"blocks": blocks, "data": {"strong": works}}

    # 5. What holds it back
    if blocks_held:
        blocks = [para("What each loop lacks for its next level, most widely felt first."),
                  bullets(f"**{i['stage_name']}.** {i['text']} {_loops_text(i, words, model)}" for i in blocks_held)]
    else:
        blocks = [para("Every loop is at the top level.")]
    sections["holds"] = {"blocks": blocks, "data": {"items": blocks_held}}

    # 6. Safety gates
    rows, gates = [], []
    for ctl in sal["controls"]:
        entry = words.control(ctl["control"])
        rows.append([entry["Name"], CONTROL_STATUS[ctl["status"]], entry["Why"] if ctl["status"] == "fail" else ""])
        gates.append({"control": ctl["control"], "status": ctl["status"]})
    applicable = [g for g in gates if g["status"] != "n/a"]
    passed = sum(g["status"] == "pass" for g in applicable)
    sections["gates"] = {
        "blocks": [para("Safety gates must all pass before the product may carry changes from start to finish "
                        f"(Level 3). {passed} of {len(applicable)} that apply have passed."),
                   table(("Safety gate", "Status", "Why it matters"), rows)],
        "data": {"gates": gates, "passed": passed, "applicable": len(applicable)}}

    # 7. How much AI does
    sections["ai"] = _ai_section(data, model, result, words)

    # 8. Does the loop improve itself
    rec = result["recursion"]
    if rec["score"] is None:
        blocks = [para("Not read: this check does not apply to the product.")]
    else:
        entry = words.recursion(rec["score"])
        text = f"**{entry['Name']}** (step {rec['score']} of {len(model['recursion']) - 1}). {entry['Meaning']}"
        if rec["status"] == "not_evidenced":
            text += " No evidence was found, so it counts as the lowest step."
        blocks = [para("Do the checks, tests and rules that govern change get better from results? A loop whose "
                       "checks never improve repeats its mistakes faster."), para(text)]
    sections["recursion"] = {"blocks": blocks, "data": {"step": rec["score"], "status": rec["status"]}}

    # 9. Has it been proven
    sections["proven"] = _proven_section(model, result, words)

    # 10. How sure this reading is
    sections["confidence"] = _confidence_section(data, criteria, order, model, result, words)

    # 11. What to do next
    sections["next"] = _next_section(model, sal, words, design)

    # 12. For engineers
    sections["engineers"] = _engineers_section(data, criteria, order, model, result, words)

    report = {"product": data.get("product"), "date": data.get("date"), "source": data.get("source"),
              "framework": model["framework"], "framework_version": model["version"], "basis": result["basis"],
              "headline_text": score.result_headline(result, model),
              "sections": [dict({"id": sid, "title": title}, **sections[sid]) for sid, title in SECTIONS]}
    guard(report)
    return report


def _ai_section(data, model, result, words):
    sal = result["variants"]["default"]["sal"]
    blocks, out = [], {}
    drv = sal.get("ai_driven")
    if drv:
        lines = []
        for loop in model["loops"]:
            n = drv["loops"][loop]["level"]
            lines.append(f"{words.loop(loop)}: " + (f"AI does the work up to {words.level_name(n)}." if n
                                                    else "AI does none of the steps on its own yet."))
        blocks += [para("How far the product's own AI carries each loop. Level 1 is people changing the product, "
                        "so AI counts from Level 2, and never above the loop's own level."), bullets(lines)]
        out["ai_driven"] = {"headline": drv["headline"], "loops": {l: drv["loops"][l]["level"] for l in model["loops"]}}
    delivery = result["ai_delivery"]
    blocks.append(para(delivery["text"]))
    out["ai_delivery"] = {"recorded": delivery["recorded"], "present": delivery["present"],
                          "qualifies": delivery["qualifies"]}
    if "ai_view" in model:
        d = result["variants"]["default"]["ai_readiness"]
        avail = result["variants"]["available"]["ai_readiness"]
        if d["status"] == "assessed":
            blocks += _ai_readiness_blocks(d, model, words, "How safe its AI features are to run for real customers")
            out["ai_readiness"] = {"level": d["level"], "capped": bool(d["label"])}
        elif avail["status"] == "assessed":
            blocks.append(para("The product has no AI features as shipped, but they can be switched on."))
            blocks += _ai_readiness_blocks(avail, model, words, "With them switched on, how safe they are to run "
                                                                "for real customers")
            out["ai_readiness"] = {"level": None, "opt_in_level": avail["level"], "capped": bool(avail["label"])}
        else:
            blocks.append(para("The product has no AI features, so the checks on AI features do not apply."))
            out["ai_readiness"] = {"level": None}
    return {"blocks": blocks, "data": out}


def _ai_readiness_blocks(view, model, words, lead):
    top = len(model["ai_view"]["levels"]) - 1
    blocks = [para(f"{lead}: {view['level']} out of {top}. The weakest area sets this.")]
    lines = []
    for name, dim in view["dimensions"].items():
        shown = "does not apply" if dim["level"] is None else f"{dim['level']} out of {top}"
        lines.append(f"{words.ai(name)['Name']}: {shown}.")
    for gate in view["gates"]:
        lines.append(f"{words.ai(gate['gate'])['Name']}: {CONTROL_STATUS[gate['status']].lower()}.")
    blocks.append(bullets(lines))
    if view["label"]:
        failed = [words.ai(g["gate"])["Name"] for g in view["gates"] if g["status"] == "fail"]
        blocks.append(para(f"Whatever else improves, it cannot rise above {model['ai_view']['gate_cap']} until "
                           "these pass: " + join_names(failed) + "."))
    return blocks


def _proven_section(model, result, words):
    proven = result["proven"]
    if proven is None:
        return {"blocks": [para("Not read. A design reading has no operating records, so it cannot say what the "
                                "product has been seen to do.")], "data": {"read": False}}
    lines = []
    for loop in model["loops"]:
        info = proven["loops"][loop]
        if info["status"] == "evidenced":
            lines.append(f"{words.loop(loop)}: proven at {words.level_name(info['level'])}. "
                         f"It is built to Level {info['built']}.")
        elif info["status"] == "not_evidenced":
            lines.append(f"{words.loop(loop)}: not evidenced. The rater looked for operating records and found "
                         "none that show it.")
        else:
            lines.append(f"{words.loop(loop)}: not evidenced. No operating records were given for it.")
    blocks = []
    if proven["headline"] is None:
        blocks.append(para("Not yet proven in operation."))
    else:
        blocks.append(para(f"Proven in operation at {words.level_name(proven['headline'])}: records show real "
                           "changes going through the loop at that level, more than once, in real use."))
    blocks.append(bullets(lines))
    if not any(proven["loops"][l]["status"] == "evidenced" for l in model["loops"]):
        blocks.append(para("This reading comes from the product's code and documents alone. Nobody observed the "
                           "product in operation, so the reading cannot say what it has been seen to do."))
    blocks.append(para("Built says what the product can do; proven says what it has been seen to do. A product "
                       "should run at the level it has proven, and take on more as the proof grows."))
    return {"blocks": blocks,
            "data": {"read": True, "headline": proven["headline"],
                     "loops": {l: proven["loops"][l]["level"] for l in model["loops"]}}}


def _holds_plain(text, model, words):
    """A scorer 'holds' string ('<loop> to L<n>' or '<control> control') in plain words."""
    for loop, name in model["loops"].items():
        match = re.match(rf"^{re.escape(name)} to L(\d)$", text)
        if match:
            return f"{words.loop(loop)}, on the way to Level {match.group(1)}"
    if text.endswith(" control"):
        return "the safety gate " + lower_first(words.control(text[:-len(" control")])["Name"])
    return text


def _confidence_section(data, criteria, order, model, result, words):
    conf, cov, grades = result["confidence"], result["coverage"], result["grades"]
    blocks, out = [], {"recorded": conf["recorded"]}
    if conf["recorded"]:
        c = conf["criteria"]
        assessed = c["high"] + c["medium"] + c["low"]
        blocks.append(para(f"Of the {assessed} answers based on evidence, {c['high']} are held with high confidence "
                           f"({CONFIDENCE_WORDS['high']}), {c['medium']} with medium confidence "
                           f"({CONFIDENCE_WORDS['medium']}) and {c['low']} with low confidence "
                           f"({CONFIDENCE_WORDS['low']})."))
        k = conf["change_kinds"]
        if k["none"] < len(data["change_kinds"]):
            blocks.append(para(f"For the kinds of change: {k['high']} high, {k['medium']} medium and {k['low']} low."))
        out["criteria"] = c
    else:
        blocks.append(para("The rater did not record how sure they were of each answer."))
    if conf["check_first"]:
        blocks.append(para("Check these first. The rater was least sure of them, and each one decides a level or "
                           "a safety gate:"))
        blocks.append(bullets(f"{words.crit(i['id'])['Name']}: holds "
                              + "; ".join(_holds_plain(h, model, words) for h in i["holds"]) + "."
                              for i in conf["check_first"]))
    out["check_first"] = [i["id"] for i in conf["check_first"]]
    total = sum(cov.values())
    blocks.append(para(f"The reading answers {total} questions: {cov['assessed']} from evidence, "
                       f"{cov['not_evidenced']} where no evidence was found (counted as missing), and "
                       f"{cov['not_applicable']} that do not apply to this product."))
    shown = [f"{grades[g]} {text}" for g, text in GRADE_WORDS if g != "D" or grades["D"] or result["basis"] == "design"]
    blocks.append(para("The evidence behind the answers: " + join_names(shown) + "."))
    out["coverage"], out["grades"] = cov, grades
    changes = _variant_changes(model, result, words)
    blocks += [para(t) for t in changes] or [para("Neither the higher readings some evidence also supports, nor "
                                                  "settings that ship switched off, would change any level.")]
    out["variant_changes"] = changes
    fragile = result["sensitivity"]["lower_headline"]
    if fragile:
        blocks.append(para("The overall level would drop if any of these were rated one step lower: "
                           + join_names(words.crit(c)["Name"] for c in fragile) + "."))
    facts = [words.fact(f) for f in model["scope_facts"] if data["scope_facts"][f]["value"]]
    if facts:
        blocks.append(para("The reading treats the product as follows:"))
        blocks.append(bullets(f + "." for f in facts))
    blocks.append(para("This is one rater's reading of the evidence. A second, independent reading may differ."))
    return {"blocks": blocks, "data": out}


def _variant_changes(model, result, words):
    base = result["variants"]["default"]["sal"]
    out = []
    for variant, lead in (("high", "With the higher readings some evidence also supports"),
                          ("available", "With settings that ship switched off turned on")):
        other = result["variants"][variant]["sal"]
        moved = [f"{words.loop(l)} would read {words.level_name(other['loops'][l]['level'])}"
                 for l in model["loops"] if other["loops"][l]["level"] != base["loops"][l]["level"]]
        if moved:
            text = f"{lead}, " + "; ".join(moved) + "."
            if other["headline"] != base["headline"]:
                text += f" The overall level would be {words.level_name(other['headline'])}."
            out.append(text)
    return out


def plain_challenge(text, model, words):
    for old, new in CHALLENGE_WORDS:
        text = text.replace(old, new)
    for loop, name in model["loops"].items():
        text = text.replace(name, f"‘{words.loop(loop)}’")
    return text


def _next_section(model, sal, words, design):
    top = len(model["levels"]) - 1
    blocks, challenges = [], {}
    for loop in model["headline"]:
        n = sal["loops"][loop]["level"]
        if n >= top:
            blocks.append(para(f"**{words.loop(loop)}** is at the top level. Keep proving it in operation."))
            continue
        text = plain_challenge(model["challenges"][str(n + 1)][loop], model, words)
        challenges[loop] = {"to": n + 1, "text": text}
        blocks.append(para(f"**{words.loop(loop)}, to {words.level_name(n + 1)}.** The check to run on the live "
                           f"product: {text}"))
    if len(challenges) > 1:
        blocks.append(para("For the overall level to rise, both checks must pass."))
    if design:
        blocks.append(para("A design reading becomes a built one only when a fresh assessment of what ships finds "
                           "the evidence."))
    target = min(sal["headline"] + 1, top)
    blocks.append(bullets([
        "For a plan of milestones that starts from a business goal, run "
        "`python3 scripts/blueprint.py <assessment.json> --goal \"<business goal>\"`.",
        "For the full list of what the next assessment must find, run "
        f"`python3 scripts/score.py <assessment.json> --checklist {target}`."]))
    return {"blocks": blocks, "data": {"challenges": challenges, "checklist_level": target}}


def _engineers_section(data, criteria, order, model, result, words):
    default = result["variants"]["default"]
    rows = []
    for cid in order:
        entry, value = data["scores"][cid], default["effective"][cid]
        if entry["status"] == "not_applicable":
            shown = "does not apply"
        elif entry["status"] == "not_evidenced":
            shown = "0 (no evidence found)"
        else:
            shown = str(value)
        rows.append([words.crit(cid)["Name"], cid, shown])
    blocks = [para(f"Headline as the scorer prints it: **{score.result_headline(result, model)}**")]
    if "ai_view" in model:
        blocks.append(para("AI Readiness as the scorer prints it: "
                           + score.ai_headline_text(default["ai_readiness"], model) + "."))
    blocks.append(para(result["recursion"]["text"] + ". " + result["kinds"]["text"] + "."))
    blockers = []
    for loop, name in model["loops"].items():
        info = default["sal"]["loops"][loop]
        if info["blockers"]:
            blockers.append(f"{name} to L{info['level'] + 1}: " + "; ".join(
                f"{b['part']} {b['stage']} needs {b['needs']} (has {b['observed']})" for b in info["blockers"]))
    if blockers:
        blocks += [para("Next-level blockers in the scorer's terms:"), bullets(blockers)]
    blocks.append(table(("Plain name", "Code", "Score"), rows))
    return {"blocks": blocks, "data": {"scores": {cid: default["effective"][cid] for cid in order}}}


# ---------------------------------------------------------------- rendering and the guard

def render_blocks(blocks):
    lines = []
    for block in blocks:
        if block["type"] == "paragraph":
            lines += [block["text"], ""]
        elif block["type"] == "list":
            lines += [f"- {item}" for item in block["items"]] + [""]
        elif block["type"] == "table":
            lines.append("| " + " | ".join(score.cell(h) for h in block["header"]) + " |")
            lines.append("|" + "---|" * len(block["header"]))
            lines += ["| " + " | ".join(score.cell(c) for c in row) + " |" for row in block["rows"]]
            lines.append("")
        else:
            raise ValueError(f"unknown block type {block['type']!r}")
    return lines


def render_section(section):
    return [f"## {section['title']}", ""] + render_blocks(section["blocks"])


def render(report):
    """The Markdown report from its data (the --json payload renders to the same text)."""
    lines = [f"# {score.cell(report.get('product'))}: how ready it is to evolve itself", "",
             f"A plain-language reading of an {report['framework']} {report['framework_version']} assessment. "
             f"Date {score.cell(report.get('date'))}.", ""]
    for section in report["sections"]:
        lines += render_section(section)
    return "\n".join(lines).rstrip() + "\n"


def body_text(report):
    """Every rendered line of the body: all sections before For engineers."""
    lines = []
    for section in report["sections"]:
        if section["id"] != ENGINEERS:
            lines += render_section(section)
    return lines


def guard(report):
    """Fail loudly when the body carries a criterion code or a banned word."""
    bad = []
    for line in body_text(report):
        found = CODE.findall(line) + BANNED.findall(line)
        if found:
            bad.append(f"{', '.join(dict.fromkeys(found))}: {line}")
    if bad:
        raise ReportDefect("The report body would contain codes or engineering words. Fix the plain-language "
                           "file, the assessment's kind names or this template:\n" + "\n".join(" - " + b for b in bad))


# ---------------------------------------------------------------- command line

def main(argv=None):
    parser = argparse.ArgumentParser(description="Print a plain-language EVOLVE report.")
    parser.add_argument("assessment")
    parser.add_argument("--json", action="store_true", help="print the same content as data")
    parser.add_argument("--rubric", default=score.DEFAULT_RUBRIC)
    parser.add_argument("--plain", default=DEFAULT_PLAIN, help="the plain-language file")
    args = parser.parse_args(argv)

    criteria, order, model = score.load_rubric(args.rubric)
    try:
        plain = load_plain(args.plain)
    except (OSError, PlainLanguageError) as exc:
        print(f"Cannot read the plain-language file {args.plain}: {exc}", file=sys.stderr)
        return 2
    missing = check_plain(plain, criteria, order, model)
    if missing:
        print(f"PLAIN LANGUAGE INCOMPLETE: {args.plain} lacks entries the report needs", file=sys.stderr)
        for item in missing:
            print(" -", item, file=sys.stderr)
        return 2
    try:
        with open(args.assessment, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read {args.assessment}: {exc}")
        return 2
    errors = score.validate(data, criteria, order, model)
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(" -", error)
        return 2
    try:
        report = build_report(data, criteria, order, model, plain)
    except ReportDefect as exc:
        print(f"REPORT DEFECT: {exc}", file=sys.stderr)
        return 3
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render(report), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
