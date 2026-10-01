#!/usr/bin/env python3
"""Validate, score, profile and prescribe an EVOLVE assessment.

Usage:
  score.py ASSESSMENT.json [--json] [--quiet] [--rubric PATH]
  score.py ASSESSMENT.json --prescribe [--target 3|4] [--json] [--remediation PATH]

Every scoring choice (capabilities, scope facts, applicability, loop conditions,
critical controls, depth rules, archetype exclusions, caps) is read from the
evolve-model block in references/rubric.md.

Assessment fields:
  product, date, source, archetype
  scope_facts      {fact: {"value": true|false, "evidence": text}} for every fact in the model
  scores           {criterion id: entry}

Criterion entry fields:
  status          assessed | not_evidenced | not_applicable
  score           0..4, the level in the default configuration (assessed)
  grade           A | B | C (assessed)
  evidence        text (assessed)
  alt_score       score + 1, a higher reading that is also defensible (assessed, optional)
  alt_note        why the alternate is defensible (required with alt_score)
  available_score 0..4, the level with shipped opt-in settings enabled (assessed, optional)
  facets          {"implemented": bool, "tested": bool, "operated": bool}
                  (required on depth-capped criteria for any reading of 3 or more)
  inventory       {surface: 0..4 or "n/a"} (required on inventory criteria scoring 3 or more)
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
VARIANTS = ("default", "high", "available", "assessed_only", "all_applicable")
SAL_VARIANTS = ("default", "high", "available")
PARTS = ("stages", "spine", "architecture", "governance")
FACETS = ("implemented", "tested", "operated")
ID = r"[A-Z]{3}-\d{2}"


class ModelError(SystemExit):
    pass


def r1(value):
    """Round half up to one decimal, for display only."""
    if value is None:
        return None
    return float(Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


# ---------------------------------------------------------------- model

def _as_list(value):
    return [value] if isinstance(value, str) else list(value)


def _test_ids(test):
    """Every criterion id a condition test names."""
    ids = []
    if "c" in test:
        ids.append(test["c"])
    if "with" in test:
        ids += _test_ids(test["with"])
    for key in ("any", "all"):
        for sub in test.get(key, []):
            ids += _test_ids(sub)
    return ids


def load_rubric(path):
    criteria, order, areas = {}, [], {}
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    cap, area = None, None
    for line in text.splitlines():
        line = line.strip()
        heading = re.match(r"^# Capability ([A-Z]{3}): (.+)$", line)
        if heading:
            cap, area = heading.group(1), None
            continue
        heading = re.match(r"^## Area: (.+)$", line)
        if heading:
            area = heading.group(1).strip()
            continue
        criterion = re.match(rf"^### ({ID}) (.+)$", line)
        if criterion:
            cid = criterion.group(1)
            if cid in criteria:
                raise ModelError(f"Rubric defines {cid} twice: {path}")
            if cap is None or area is None or not cid.startswith(cap + "-"):
                raise ModelError(f"{cid} is not under a matching capability and area heading")
            criteria[cid] = {"cap": cap, "area": area, "title": criterion.group(2).strip()}
            areas.setdefault(cap, {}).setdefault(area, []).append(cid)
            order.append(cid)
    if not criteria:
        raise ModelError("Rubric has no criterion headings: " + path)
    block = re.search(r"```json evolve-model\n(.*?)\n```", text, re.S)
    if not block:
        raise ModelError("Rubric has no evolve-model block: " + path)
    model = json.loads(block.group(1))
    model["areas"] = areas
    caps = set(model["capabilities"])
    if caps != set(areas):
        raise ModelError(f"Capabilities in the model {sorted(caps)} do not match the rubric {sorted(areas)}")
    facts = set(model["scope_facts"])

    def known(ids, where):
        unknown = sorted(set(ids) - set(criteria))
        if unknown:
            raise ModelError(f"{where} names unknown criteria: {unknown}")

    for cid, gate in model["applies_when"].items():
        known([cid], "applies_when")
        unknown = set(_as_list(gate)) - facts
        if unknown:
            raise ModelError(f"applies_when {cid} names unknown scope facts {sorted(unknown)}")
    known(model["depth_capped"], "depth_capped")
    known(model["inventories"], "inventories")
    for name, excluded in model["archetype_exclusions"].items():
        if excluded != "*":
            known(excluded, f"archetype {name}")
    for loop, paths in model["build_paths"].items():
        if loop not in model["loops"]:
            raise ModelError(f"build_paths names unknown loop {loop!r}")
        for who in ("people", "product"):
            for alt in paths[who]:
                if "cap" in alt and alt["cap"] not in caps:
                    raise ModelError(f"build path {loop}/{who} names unknown capability {alt['cap']}")
                known(_test_ids(alt), f"build path {loop}/{who}")
    known([r["c"] for r in model["rollback"]], "rollback")
    if set(model["headline"]) - set(model["loops"]):
        raise ModelError("headline names unknown loops")
    for level, conds in model["conditions"].items():
        if not 1 <= int(level) <= len(model["levels"]) - 1:
            raise ModelError(f"conditions for unknown level {level}")
        for cond in conds:
            if cond["part"] not in PARTS:
                raise ModelError(f"condition part must be one of {PARTS}: {cond}")
            if cond.get("loop") and cond["loop"] not in model["loops"]:
                raise ModelError(f"condition names unknown loop: {cond}")
            if cond.get("every") and cond["every"] not in caps:
                raise ModelError(f"condition names unknown capability: {cond}")
            if set(_as_list(cond.get("when", []))) - facts:
                raise ModelError(f"condition names unknown scope fact: {cond}")
            known(_test_ids(cond), f"level {level} condition")
    return criteria, order, model


def load_remediation(path, criteria):
    remediation, current = {}, None
    with open(path, encoding="utf-8") as handle:
        lines = handle.readlines()
    for raw in lines:
        line = raw.rstrip("\n")
        heading = re.match(rf"^### ({ID})\s*$", line.strip())
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
                ids = [] if body.lower().startswith("none") else re.findall(rf"\b({ID})\b", body)
                unknown = [i for i in ids if i not in criteria]
                if unknown:
                    raise ModelError(f"Remediation {current} {prefix} names unknown criteria: {unknown}")
                remediation[current][field] = ids
    return remediation


# ---------------------------------------------------------------- validation

def _is_int_score(value):
    return isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 4


def _text(entry, key):
    return str(entry.get(key) or "").strip()


def fact_values(data):
    facts = data.get("scope_facts") if isinstance(data, dict) else None
    if not isinstance(facts, dict):
        return {}
    return {k: v.get("value") for k, v in facts.items() if isinstance(v, dict)}


def _validate_assessed(cid, entry, model, errors):
    score = entry.get("score")
    if not _is_int_score(score):
        errors.append(f"{cid}: score must be an integer 0..4, got {score!r}")
        return
    if str(entry.get("grade", "")).upper() not in ("A", "B", "C"):
        errors.append(f"{cid}: grade must be A, B or C, got {entry.get('grade')!r}")
    if _text(entry, "evidence").lower() in PLACEHOLDERS:
        errors.append(f"{cid}: assessed criteria need evidence")
    if _is_int_score(entry.get("alt_score")):
        if entry["alt_score"] != score + 1:
            errors.append(f"{cid}: alt_score must be the next level up (score + 1); "
                          "score the lower reading and record the higher one")
        if _text(entry, "alt_note").lower() in PLACEHOLDERS:
            errors.append(f"{cid}: alt_score needs an alt_note")
    if _is_int_score(entry.get("available_score")) and entry["available_score"] < score:
        errors.append(f"{cid}: available_score cannot be below score")
    readings = [score] + [entry[k] for k in ("alt_score", "available_score") if _is_int_score(entry.get(k))]
    if "facets" in entry:
        facets = entry["facets"]
        if not isinstance(facets, dict) or set(facets) != set(FACETS) \
                or not all(isinstance(facets[f], bool) for f in FACETS):
            errors.append(f"{cid}: facets must give implemented, tested and operated as true or false")
        elif (facets["tested"] or facets["operated"]) and not facets["implemented"]:
            errors.append(f"{cid}: tested or operated facets require implemented")
    elif cid in model["depth_capped"] and max(readings) >= 3:
        errors.append(f"{cid}: depth-capped criterion read at 3 or more needs facets")
    if cid not in model["inventories"]:
        return
    inventory = entry.get("inventory")
    if inventory is None:
        if max(readings) >= 3:
            errors.append(f"{cid}: inventory criterion read at 3 or more needs an inventory")
        return
    if not isinstance(inventory, dict) or not inventory:
        errors.append(f"{cid}: inventory must be a non-empty object of surface levels")
        return
    allowed, levels = model["inventories"][cid], []
    if allowed:
        missing = [s for s in allowed if s not in inventory]
        if missing:
            errors.append(f"{cid}: inventory must list every surface, using \"n/a\" where one does not apply "
                          f"(missing: {', '.join(missing)})")
    for surface, level in inventory.items():
        if allowed and surface not in allowed:
            errors.append(f"{cid}: inventory surface {surface!r} must be one of {', '.join(allowed)}")
        if level == "n/a":
            continue
        if not _is_int_score(level):
            errors.append(f"{cid}: inventory level for {surface!r} must be 0..4 or \"n/a\"")
        else:
            levels.append(level)
    if not levels:
        errors.append(f"{cid}: inventory needs at least one surface with a level")
    for name, reading in zip(("score", "alt_score", "available_score"),
                             [score] + [entry.get(k) for k in ("alt_score", "available_score")]):
        if _is_int_score(reading) and levels and reading >= 3 and reading > min(levels):
            errors.append(f"{cid}: {name} {reading} exceeds the lowest inventory level {min(levels)}")


def validate(data, criteria, order, model):
    errors = []
    if not isinstance(data, dict):
        return ["assessment file must be a JSON object"]
    exclusions = model["archetype_exclusions"]
    archetype = data.get("archetype")
    if archetype not in exclusions:
        errors.append("archetype must be one of: " + ", ".join(sorted(exclusions)))
    raw_facts = data.get("scope_facts")
    if not isinstance(raw_facts, dict):
        errors.append("'scope_facts' must be an object keyed by fact")
        raw_facts = {}
    for fact in model["scope_facts"]:
        entry = raw_facts.get(fact)
        if not isinstance(entry, dict) or not isinstance(entry.get("value"), bool):
            errors.append(f"scope fact {fact}: value must be true or false")
        elif _text(entry, "evidence").lower() in PLACEHOLDERS:
            errors.append(f"scope fact {fact}: needs evidence")
    for unknown in sorted(set(raw_facts) - set(model["scope_facts"])):
        errors.append(f"scope fact {unknown}: not in the model")
    facts = fact_values(data)
    paths = model.get("change_path_facts", [])
    if paths and all(isinstance(facts.get(f), bool) for f in paths) and not any(facts[f] for f in paths):
        errors.append("scope facts: at least one change path (" + " or ".join(paths) + ") must be true")
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
        for key, allowed in (("alt_score", "assessed"), ("available_score", "assessed"),
                             ("if_applicable", "not_applicable"), ("facets", "assessed"),
                             ("inventory", "assessed")):
            if key in entry and status != allowed:
                errors.append(f"{cid}: {key} is only allowed when status is {allowed}")
        gate = _as_list(model["applies_when"].get(cid, []))
        switched_off = bool(gate) and all(facts.get(f) is False for f in gate)
        if switched_off and status != "not_applicable":
            errors.append(f"{cid}: does not apply because scope fact {' and '.join(gate)} is false; "
                          "mark it not_applicable")
        if status == "assessed":
            _validate_assessed(cid, entry, model, errors)
        elif status == "not_evidenced":
            if _text(entry, "searched").lower() in PLACEHOLDERS:
                errors.append(f"{cid}: not_evidenced needs the searched scope")
        else:
            if _text(entry, "rationale").lower() in PLACEHOLDERS:
                errors.append(f"{cid}: not_applicable needs a rationale")
            if not switched_off and allowed_na != "*" and cid not in allowed_na:
                hint = f" or set scope fact {' and '.join(gate)} to false" if gate else ""
                errors.append(f"{cid}: archetype '{archetype}' may not exclude {cid} "
                              f"(allowed: {', '.join(allowed_na) or 'none'}{hint})")
    for unknown in sorted(set(scores) - set(order)):
        errors.append(f"{unknown}: not in rubric")
    return errors


# ---------------------------------------------------------------- scoring

def inventory_floor(entry):
    """The weakest applicable surface level, or None when there is no inventory."""
    levels = [v for v in (entry.get("inventory") or {}).values() if _is_int_score(v)]
    return min(levels) if levels else None


def _inventory_cap(cid, value, entry, model, flags):
    if cid not in model["inventories"] or value < 3:
        return value
    floor = inventory_floor(entry)
    allowed = 2 if floor is None else max(2, floor)
    if value > allowed:
        flags.append(f"{cid}: inventory caps {value} -> {allowed}")
        return allowed
    return value


def _depth_cap(cid, value, entry, model, flags):
    if cid not in model["depth_capped"] or value < 3:
        return value
    facets = entry.get("facets", {})
    allowed = 4 if facets.get("tested") and facets.get("operated") else 3 if facets.get("tested") else 2
    if value > allowed:
        flags.append(f"{cid}: evidence depth caps {value} -> {allowed}")
        return allowed
    return value


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
            values[cid] = None if variant == "assessed_only" else 0
            continue
        value = entry["score"]
        if variant == "high" and "alt_score" in entry:
            value = entry["alt_score"]
        if variant == "available" and "available_score" in entry:
            value = entry["available_score"]
        if str(entry["grade"]).upper() == "C" and value > caps["grade_c_max"]:
            flags.append(f"{cid}: grade C caps {value} -> {caps['grade_c_max']}")
            value = caps["grade_c_max"]
        if entry.get("single_entity") is True and value > caps["single_entity_max"]:
            flags.append(f"{cid}: single-entity caps {value} -> {caps['single_entity_max']}")
            value = caps["single_entity_max"]
        value = _depth_cap(cid, value, entry, model, flags)
        value = _inventory_cap(cid, value, entry, model, flags)
        if entry.get("incident") is True and value > 0:
            new = max(0, value - caps["incident_penalty"])
            flags.append(f"{cid}: incident deduction {value} -> {new}")
            value = new
        values[cid] = value
    return values, flags


def aggregate(values, criteria, model):
    """Area means and capability scores (mean of area means)."""
    area_means, capabilities = {}, {}
    for cap, areas in model["areas"].items():
        means = []
        for area, ids in areas.items():
            present = [values[c] for c in ids if values.get(c) is not None]
            if present:
                area_means[f"{cap} {area}"] = mean(present)
                means.append(mean(present))
        capabilities[cap] = mean(means) if means else None
    return {"area_means": area_means, "capabilities": capabilities}


class Evaluator:
    """Evaluates level conditions for one variant."""

    def __init__(self, data, values, capabilities, model):
        self.data, self.values, self.caps, self.model = data, values, capabilities, model
        self.facts = fact_values(data)

    def _operated(self, cid):
        return self.data["scores"][cid].get("facets", {}).get("operated") is True

    def _crit(self, cid, minimum, operated=False):
        """(passed, observed) for one criterion; a not-applicable criterion passes."""
        if self.data["scores"][cid]["status"] == "not_applicable":
            return True, "n/a"
        value = self.values.get(cid) or 0
        return value >= minimum and (not operated or self._operated(cid)), value

    def _path(self, loop, who, minimum):
        observed = []
        for alt in self.model["build_paths"][loop][who]:
            if "cap" in alt:
                value = self.caps.get(alt["cap"])
                ok = value is not None and value >= minimum
                observed.append(f"{alt['cap']} {fmt(value)}")
            else:
                ok, value = self._crit(alt["c"], minimum)
                ok = ok and value != "n/a"
                observed.append(f"{alt['c']} {value}")
                if ok and "with" in alt:
                    w_ok, w_value = self._crit(alt["with"]["c"], alt["with"]["min"])
                    observed[-1] += f" with {alt['with']['c']} {w_value}"
                    ok = w_ok
            if ok:
                return True, ", ".join(observed)
        return False, ", ".join(observed)

    def _rollback(self, minimum, operated=False):
        ok_all, observed = True, []
        for item in self.model["rollback"]:
            if item.get("when") and self.facts.get(item["when"]) is not True:
                continue
            ok, value = self._crit(item["c"], minimum, operated)
            observed.append(f"{item['c']} {value}")
            ok_all = ok_all and ok
        return ok_all, ", ".join(observed)

    def test(self, cond, loop):
        """(passed, needs text, observed text)."""
        when = cond.get("when")
        if when:
            when = [when] if isinstance(when, str) else when
            if not any(self.facts.get(f) is True for f in when):
                return True, "not applicable (" + " and ".join(when) + " false)", "n/a"
        operated = cond.get("operated", False)
        suffix = ", operated" if operated else ""
        if "c" in cond:
            ok, value = self._crit(cond["c"], cond["min"], operated)
            return ok, f"{cond['c']} ≥ {cond['min']}{suffix}", str(value)
        if "path" in cond:
            ok, observed = self._path(loop, cond["path"], cond["min"])
            return ok, f"{cond['path']} build path ≥ {cond['min']}", observed
        if "rollback" in cond:
            ok, observed = self._rollback(cond["rollback"], operated)
            return ok, f"rollback ≥ {cond['rollback']}{suffix}", observed
        if "every" in cond:
            below = []
            for ids in self.model["areas"][cond["every"]].values():
                for cid in ids:
                    ok, value = self._crit(cid, cond["min"], operated)
                    if not ok:
                        below.append(f"{cid} {value}")
            return not below, f"every applicable {cond['every']} ≥ {cond['min']}{suffix}", \
                ", ".join(below) or "all met"
        for key, combine in (("any", any), ("all", all)):
            if key in cond:
                results = [self.test(sub, loop) for sub in cond[key]]
                joiner = " or " if key == "any" else " and "
                return combine(r[0] for r in results), joiner.join(r[1] for r in results), \
                    "; ".join(r[2] for r in results)
        raise ModelError(f"Unrecognised condition: {cond}")


def loop_levels(data, values, capabilities, model):
    ev = Evaluator(data, values, capabilities, model)
    top = len(model["levels"]) - 1
    loops = {}
    for loop in model["loops"]:
        part_level = {p: top for p in PARTS}
        failures, counts = {}, {}
        for level in range(1, top + 1):
            for cond in model["conditions"].get(str(level), []):
                if cond.get("loop") not in (None, loop):
                    continue
                ok, needs, observed = ev.test(cond, loop)
                if observed != "n/a":
                    # Conditions that do not apply count in neither the numerator nor the denominator.
                    met, total = counts.get(level, (0, 0))
                    counts[level] = (met + ok, total + 1)
                if not ok:
                    failures.setdefault(level, []).append(
                        {"part": cond["part"], "stage": cond["stage"], "needs": needs, "observed": observed,
                         "control": cond.get("control")})
                    part_level[cond["part"]] = min(part_level[cond["part"]], level - 1)
        level = min(part_level.values())
        met, total = counts.get(level + 1, (0, 0)) if level < top else (0, 0)
        loops[loop] = {"level": level, "name": model["levels"][level], "parts": part_level,
                       "next_met": met, "next_total": total,
                       "blockers": failures.get(level + 1, []) if level < top else []}
    controls, seen = [], set()
    for cond in model["conditions"].get("3", []):
        name = cond.get("control")
        if not name or name in seen:
            continue
        seen.add(name)
        ok, needs, observed = ev.test(cond, None)
        status = "n/a" if observed == "n/a" else "pass" if ok else "fail"
        controls.append({"control": name, "needs": needs, "observed": observed, "status": status})
    headline = min(loops[l]["level"] for l in model["headline"])
    return {"headline": headline, "headline_name": model["levels"][headline], "loops": loops, "controls": controls}


def sensitivity(data, values, criteria, model):
    """Criteria whose one-level change would move the headline or a loop level.

    Raw criterion values are moved up or down by one; caps are not re-applied, so this
    shows how close the reading sits to a boundary, not what evidence would be needed.
    """
    base = loop_levels(data, values, aggregate(values, criteria, model)["capabilities"], model)
    raise_headline, lower_headline, raise_loop, lower_loop = [], [], {}, {}
    for cid, value in values.items():
        if value is None or data["scores"][cid]["status"] != "assessed":
            continue
        for step in (1, -1):
            new = value + step
            if not 0 <= new <= 4:
                continue
            trial = dict(values, **{cid: new})
            out = loop_levels(data, trial, aggregate(trial, criteria, model)["capabilities"], model)
            if out["headline"] != base["headline"]:
                (raise_headline if step > 0 else lower_headline).append(cid)
            for loop in model["loops"]:
                if out["loops"][loop]["level"] != base["loops"][loop]["level"]:
                    (raise_loop if step > 0 else lower_loop).setdefault(loop, []).append(cid)
    return {"raise_headline": raise_headline, "lower_headline": lower_headline,
            "raise_loop": raise_loop, "lower_loop": lower_loop}


def score_assessment(data, criteria, order, model):
    result = {"variants": {}, "flags": []}
    for variant in VARIANTS:
        values, flags = effective_scores(data, order, model, variant)
        agg = aggregate(values, criteria, model)
        entry = {"effective": values, **agg}
        if variant in SAL_VARIANTS:
            entry["sal"] = loop_levels(data, values, agg["capabilities"], model)
        result["variants"][variant] = entry
        if variant == "default":
            result["flags"] = flags
            result["sensitivity"] = sensitivity(data, values, criteria, model)
    coverage = {s: 0 for s in STATUSES}
    grades = {"A": 0, "B": 0, "C": 0}
    for cid in order:
        entry = data["scores"][cid]
        coverage[entry["status"]] += 1
        if entry["status"] == "assessed":
            grades[str(entry["grade"]).upper()] += 1
    result["coverage"], result["grades"] = coverage, grades
    # Alternates only ever move up, so the default and high readings bound every capability score.
    default, high = result["variants"]["default"]["capabilities"], result["variants"]["high"]["capabilities"]
    result["ranges"] = {cap: None if default[cap] is None else [default[cap], high[cap]]
                        for cap in model["capabilities"]}
    return result


# ---------------------------------------------------------------- output

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


def progress(info):
    if not info.get("next_total"):
        return ""
    return f" ({info['next_met']}/{info['next_total']} toward L{info['level'] + 1})"


def headline_text(sal, model, with_progress=False):
    loops = " · ".join(f"{model['loops'][l]} L{sal['loops'][l]['level']}"
                       + (progress(sal["loops"][l]) if with_progress else "") for l in model["loops"])
    return f"SAL {sal['headline']} ({sal['headline_name']}) · {loops}"


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


def render_markdown(data, criteria, order, model, result):
    d = result["variants"]["default"]
    sal, avail, high = d["sal"], result["variants"]["available"]["sal"], result["variants"]["high"]["sal"]
    facts = data["scope_facts"]
    on = [f for f in model["scope_facts"] if facts[f]["value"]]
    off = [f for f in model["scope_facts"] if not facts[f]["value"]]
    cov, grades = result["coverage"], result["grades"]
    lines = [f"# EVOLVE assessment: {cell(data.get('product'))}", "",
             f"Framework {model['framework']} {model['version']}. Date {cell(data.get('date'))}. "
             f"Source {cell(data.get('source'))}. Archetype **{data.get('archetype')}**.", "",
             f"Scope facts true: {', '.join(on) or 'none'}. False: {', '.join(off) or 'none'}.", "",
             f"Coverage: {cov['assessed']} assessed, {cov['not_evidenced']} not evidenced, "
             f"{cov['not_applicable']} not applicable. Grades: {grades['A']} A, {grades['B']} B, {grades['C']} C.", "",
             "## Software Autonomy Level", "",
             f"**{headline_text(sal, model)}**", "",
             f"Progress toward the next level: " + "; ".join(
                 f"{name} {sal['loops'][l]['next_met']} of {sal['loops'][l]['next_total']} conditions for "
                 f"L{sal['loops'][l]['level'] + 1}" for l, name in model["loops"].items()
                 if sal["loops"][l]["next_total"]) + ".", "",
             f"- With opt-in settings: {headline_text(avail, model)}.",
             f"- With every alternate reading: {headline_text(high, model)}.", "",
             "| Loop | Stages | Spine | Architecture | Governance | Level | With opt-in settings |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for loop, name in model["loops"].items():
        info = sal["loops"][loop]
        parts = " | ".join(f"L{info['parts'][p]}" for p in PARTS)
        lines.append(f"| {name} | {parts} | **L{info['level']}** | L{avail['loops'][loop]['level']} |")
    lines += ["", "### Critical controls", "", "| Control | Needs | Observed | Status |", "|---|---|---|---|"]
    for ctl in sal["controls"]:
        lines.append(f"| {ctl['control']} | {cell(ctl['needs'])} | {cell(ctl['observed'])} | {ctl['status']} |")
    lines += ["", "### What blocks the next level", ""]
    for loop, name in model["loops"].items():
        info = sal["loops"][loop]
        if not info["blockers"]:
            lines.append(f"- **{name}**: at the top level.")
            continue
        items = "; ".join(f"{b['part']} {b['stage']} needs {b['needs']} (has {b['observed']})"
                          for b in info["blockers"])
        lines.append(f"- **{name} to L{info['level'] + 1}**: {cell(items)}")
    sens = result["sensitivity"]
    lines += ["", "### Sensitivity", ""]
    if sens["lower_headline"]:
        lines.append("- **Fragile:** the headline drops if any of these falls one level: "
                     + ", ".join(sens["lower_headline"]) + ".")
    else:
        lines.append("- **Robust:** no single criterion falling one level lowers the headline.")
    if sens["raise_headline"]:
        lines.append("- **One step away:** raising any of these one level lifts the headline: "
                     + ", ".join(sens["raise_headline"]) + ".")
    else:
        lines.append("- No single criterion rising one level lifts the headline.")
    lines += ["", "## EVOLVE profile", "",
              "| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |",
              "|---|---:|---|---:|---:|---:|"]
    for cap, label in model["capabilities"].items():
        rng = result["ranges"][cap]
        rng_text = "–" if rng is None else (fmt(rng[0]) if r1(rng[0]) == r1(rng[1]) else f"{fmt(rng[0])}–{fmt(rng[1])}")
        lines.append(f"| {label} ({cap}) | {fmt(d['capabilities'][cap])} | {rng_text} | "
                     f"{fmt(result['variants']['available']['capabilities'][cap])} | "
                     f"{fmt(result['variants']['assessed_only']['capabilities'][cap])} | "
                     f"{fmt(result['variants']['all_applicable']['capabilities'][cap])} |")
    if result["flags"]:
        lines += ["", "Caps and deductions applied:", ""] + [f"- {f}" for f in result["flags"]]
    lines += ["", "## Area means", "", "| Area | Default |", "|---|---:|"]
    for area, value in d["area_means"].items():
        lines.append(f"| {cell(area)} | {fmt(value)} |")
    lines += ["", "## Criteria", "",
              "| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |",
              "|---|---|---:|---:|---:|---|---|---|"]
    for cid in order:
        entry = data["scores"][cid]
        status = entry["status"]
        value = d["effective"][cid]
        text = entry.get("evidence") or entry.get("searched") or entry.get("rationale") or ""
        facets = entry.get("facets")
        facet_text = "" if not facets else "".join(f[0].upper() for f in FACETS if facets.get(f))
        if entry.get("inventory"):
            text = "Inventory: " + ", ".join(f"{k} {v}" for k, v in entry["inventory"].items()) + ". " + text
        lines.append(f"| {cid} {cell(criteria[cid]['title'])} | {status} | "
                     f"{'excluded' if value is None else value} | {entry.get('alt_score', '')} | "
                     f"{entry.get('available_score', '')} | {entry.get('grade', '-') if status == 'assessed' else '-'} | "
                     f"{facet_text} | {cell(text)} |")
    lines += ["", "Facets: I implemented, T tested, O operated."]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate, score and prescribe an EVOLVE assessment.")
    parser.add_argument("scores")
    parser.add_argument("--rubric", default=DEFAULT_RUBRIC)
    parser.add_argument("--remediation", default=DEFAULT_REMEDIATION)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--quiet", action="store_true", help="print only the SAL and profile summary")
    parser.add_argument("--prescribe", action="store_true")
    parser.add_argument("--target", type=int, choices=(3, 4), default=3)
    args = parser.parse_args(argv)

    criteria, order, model = load_rubric(args.rubric)
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
        projected_caps = aggregate(projected, criteria, model)["capabilities"]
        blockers = {model["loops"][l]: default["sal"]["loops"][l]["blockers"] for l in model["loops"]}
        out = {"product": data.get("product"), "target": args.target, "investigate_first": investigate,
               "sal": default["sal"]["headline"], "next_level_blockers": blockers,
               "slices": [[{"id": c, "title": criteria[c]["title"], "from": default["effective"][c],
                            "size": remediation[c]["size"], "requires": remediation[c]["requires"],
                            "helps": remediation[c]["helps"],
                            "move": remediation[c]["to3" if args.target == 3 else "to4"]} for c in sl]
                          for sl in slices],
               "current": rounded(default["capabilities"]), "projected_ceiling": rounded(projected_caps)}
        if args.json:
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0
        print(f"# EVOLVE prescription: {cell(out['product'])} to level {args.target}\n")
        print(f"Current: {headline_text(default['sal'], model)}.\n")
        print("## Unblock the next SAL level first\n")
        for name, items in blockers.items():
            text = "; ".join(f"{b['needs']} (has {b['observed']})" for b in items) or "at the top level"
            print(f"- **{name}**: {cell(text)}")
        print()
        if investigate:
            print("## Investigate first\n")
            print("These criteria are not evidenced. Establish whether the capability exists before planning work: "
                  + ", ".join(f"{c} {criteria[c]['title']}" for c in investigate) + ".\n")
        print(f"{len(build)} assessed criteria are below {args.target}. "
              "Items in a slice can proceed in parallel after earlier slices.\n")
        for number, sl in enumerate(out["slices"], 1):
            print(f"## Slice {number}\n\n| Criterion | Now | Size | Requires | Helps | Move |\n|---|---:|---|---|---|---|")
            for item in sl:
                print(f"| {item['id']} {cell(item['title'])} | {item['from']} | {item['size']} | "
                      f"{', '.join(item['requires']) or 'none'} | {', '.join(item['helps']) or '–'} | {cell(item['move'])} |")
            print()
        print("## Projected ceilings if every move lands\n\n| Capability | Now | Ceiling |\n|---|---:|---:|")
        for cap, label in model["capabilities"].items():
            print(f"| {label} ({cap}) | {fmt(default['capabilities'][cap])} | {fmt(projected_caps[cap])} |")
        print("\nCeilings, not delivery forecasts. Re-estimate every size for the assessed software.")
        return 0

    def sal_summary(sal):
        return {"headline": sal["headline"], "headline_name": sal["headline_name"],
                "loops": {l: {"level": v["level"], "parts": v["parts"]} for l, v in sal["loops"].items()}}

    payload = {"product": data.get("product"), "date": data.get("date"), "source": data.get("source"),
               "archetype": data.get("archetype"), "framework": model["framework"],
               "framework_version": model["version"],
               "scope_facts": {f: data["scope_facts"][f]["value"] for f in model["scope_facts"]},
               "coverage": result["coverage"], "grades": result["grades"],
               "sal": default["sal"],
               "sensitivity": result["sensitivity"],
               "capabilities": rounded(default["capabilities"]),
               "ranges": rounded(result["ranges"]),
               "area_means": rounded(default["area_means"]),
               "flags": result["flags"],
               "effective_scores": default["effective"],
               "variants": {v: {"capabilities": rounded(result["variants"][v]["capabilities"]),
                                **({"sal": sal_summary(result["variants"][v]["sal"])} if v in SAL_VARIANTS else {})}
                            for v in VARIANTS if v != "default"},
               "criteria_in_rubric": len(order)}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    if args.quiet:
        print(headline_text(default["sal"], model))
        print("  ".join(f"{label} {fmt(default['capabilities'][cap])}" for cap, label in model["capabilities"].items()))
        return 0
    print(render_markdown(data, criteria, order, model, result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
