#!/usr/bin/env python3
"""Validate, score, profile and prescribe an EVOLVE assessment.

Usage:
  score.py ASSESSMENT.json [--json] [--quiet] [--rubric PATH]
  score.py ASSESSMENT.json --prescribe [--target 3|4] [--json] [--remediation PATH]
  score.py ASSESSMENT.json --checklist LEVEL [--json]

Every scoring choice (capabilities, scope facts, applicability, loop conditions,
critical controls, depth rules, archetype exclusions, caps, reach of kinds of
change) is read from the evolve-model block in references/rubric.md.

Assessment fields:
  product, date, source, archetype
  basis            shipped (default) | design
  scope_facts      {fact: {"value": true|false, "evidence": text}} for every fact in the model
  change_kinds     [{"id", "name", "who", "main": bool, "reach": 0..5, "evidence",
                     "confidence" (optional), "note" (optional)}], 1 to 8 entries, at least one main
  scores           {criterion id: entry}
  proven           {loop: {"level": n, "evidence": text} | {"status": "not_evidenced", "searched": text}}
                   (optional, shipped only; level 0 to the loop's built level)
  ai_delivery      {"present": bool, "qualifies": bool, "evidence": text, "note": text} (optional;
                   never changes a score)

Criterion entry fields:
  status          assessed | not_evidenced | not_applicable
  score           0..4, the level in the default configuration (assessed)
  grade           A | B | C, or D in a design assessment (assessed)
  evidence        text (assessed)
  confidence      high | medium | low (assessed; all assessed criteria or none)
  alt_score       score + 1, a higher reading that is also defensible (assessed, optional)
  alt_note        why the alternate is defensible (required with alt_score)
  available_score 0..4, the level with shipped opt-in settings enabled (assessed, optional)
  facets          {"implemented": bool, "tested": bool, "operated": bool}
                  (required on depth-capped criteria for any reading of 3 or more, in a shipped assessment)
  inventory       {surface: 0..4 or "n/a"} (required on inventory criteria scoring 3 or more)
  single_entity   true | false (optional)
  incident        true | false (optional)
  searched        text (not_evidenced)
  rationale       text (not_applicable)
  if_applicable   0..4, the score it would get if counted (not_applicable, optional)
"""

import argparse
import json
import math
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
AI_DRIVEN_MIN = 2  # the first level at which the product, and so AI, does stage work
AI_DRIVEN_NONE = "AI drives no stage"
PARTS = ("stages", "spine", "architecture", "governance")
FACETS = ("implemented", "tested", "operated")
ID = r"[A-Z]{3}-\d{2}"
BASES = ("shipped", "design")
CONFIDENCE = ("high", "medium", "low")
KINDS_MAX = 8
KIND_ID = r"^[a-z0-9][a-z0-9-]*$"
KIND_FIELDS = ("id", "name", "who", "main", "reach", "evidence", "confidence", "note")
RECURSION = "LRN-10"  # the criterion the Recursion line reads
DESIGN_NOTE = ("A design reading says what the product is designed for. It is not comparable with a shipped "
               "reading, which says what the product is built to do.")
PROVEN_NOTE = "From a repository alone, proven is usually not evidenced."


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


def _uses_operated(test):
    """True when a condition, or any part of it, asks for the operated facet."""
    return "operated" in test or any(_uses_operated(sub) for key in ("any", "all") for sub in test.get(key, []))


def load_rubric(path):
    criteria, order, areas, ai_areas = {}, [], {}, {}
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    cap, area, in_ai, cid = None, None, False, None
    for line in text.splitlines():
        line = line.strip()
        anchor = re.match(r"^- \*\*([0-4])\*\* (.+)$", line)
        if anchor and cid:
            criteria[cid]["anchors"][int(anchor.group(1))] = anchor.group(2).strip()
            continue
        heading = re.match(r"^# Capability ([A-Z]{3}): (.+)$", line)
        if heading:
            cap, area, in_ai, cid = heading.group(1), None, False, None
            continue
        heading = re.match(r"^# AI Readiness Checks \(([A-Z]{3})\)$", line)
        if heading:
            cap, area, in_ai, cid = heading.group(1), None, True, None
            continue
        heading = re.match(r"^## Area: (.+)$", line)
        if heading:
            area, cid = heading.group(1).strip(), None
            continue
        criterion = re.match(rf"^### ({ID}) (.+)$", line)
        if criterion:
            cid = criterion.group(1)
            if cid in criteria:
                raise ModelError(f"Rubric defines {cid} twice: {path}")
            if cap is None or area is None or not cid.startswith(cap + "-"):
                raise ModelError(f"{cid} is not under a matching capability and area heading")
            criteria[cid] = {"cap": cap, "area": area, "title": criterion.group(2).strip(), "ai_check": in_ai,
                             "anchors": {}}
            (ai_areas if in_ai else areas).setdefault(cap, {}).setdefault(area, []).append(cid)
            order.append(cid)
    if not criteria:
        raise ModelError("Rubric has no criterion headings: " + path)
    for cid, info in criteria.items():
        if sorted(info["anchors"]) != [0, 1, 2, 3, 4]:
            raise ModelError(f"{cid} needs one anchored level for each of 0 to 4")
    block = re.search(r"```json evolve-model\n(.*?)\n```", text, re.S)
    if not block:
        raise ModelError("Rubric has no evolve-model block: " + path)
    model = json.loads(block.group(1))
    model["areas"] = areas
    model["ai_areas"] = ai_areas
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
                if "serves_main" in alt and alt["serves_main"] is not True:
                    raise ModelError(f"build path {loop}/{who}: serves_main must be true")
                if "kinds" in alt and alt["kinds"] != "main":
                    raise ModelError(f"build path {loop}/{who}: kinds must be \"main\"")
                known(_test_ids(alt), f"build path {loop}/{who}")
    known([r["c"] for r in model["rollback"]], "rollback")
    if len(model.get("reach", [])) != 6:
        raise ModelError("reach needs a name for each reach 0 to 5")
    for level, test in model.get("reach_needs", {}).items():
        if not level.isdigit() or not 1 <= int(level) <= 5:
            raise ModelError(f"reach_needs names unknown reach {level!r}")
        known(_test_ids(test), f"reach_needs {level}")
    if RECURSION not in criteria or len(model.get("recursion", [])) != 5:
        raise ModelError(f"recursion needs {RECURSION} in the rubric and a name for each of its levels 0 to 4")
    for level in range(1, len(model["levels"])):
        for loop in model["loops"]:
            if not model.get("challenges", {}).get(str(level), {}).get(loop):
                raise ModelError(f"challenges need a text for level {level}, loop {loop}")
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
            if _uses_operated(cond):
                raise ModelError(f"conditions may not require the operated facet; operating records belong to "
                                 f"the Proven reading: {cond}")
            known(_test_ids(cond), f"level {level} condition")
    view = model.get("ai_view")
    if view:
        checks = {c for c, info in criteria.items() if info["ai_check"]}
        for name, dim in view["dimensions"].items():
            if set(dim["checks"]) - checks:
                raise ModelError(f"AI dimension {name} names criteria outside the AI checks section")
            if set(dim["readings"]) - set(view["readings"]):
                raise ModelError(f"AI dimension {name} names readings not listed in ai_view readings")
        used = {c for dim in view["dimensions"].values() for c in dim["checks"]}
        if used != checks:
            raise ModelError(f"AI checks not in exactly the dimensions: {sorted(checks ^ used)}")
        known(view["readings"], "ai_view readings")
        if set(view["readings"]) & checks:
            raise ModelError("AI-qualified readings must be existing criteria, not AI checks")
        for loop, ids in view.get("driven", {}).items():
            if loop not in model["loops"]:
                raise ModelError(f"ai_view driven names unknown loop {loop!r}")
            if set(ids) - set(view["readings"]):
                raise ModelError(f"ai_view driven {loop} names readings not listed in ai_view readings")
        for area, ids in view["footprint"].items():
            if set(ids) - set(view["readings"]):
                raise ModelError(f"footprint area {area} names readings not listed in ai_view readings")
        for cid, fact in view["reading_applies_when"].items():
            known([cid], "reading_applies_when")
            if fact not in facts:
                raise ModelError(f"reading_applies_when {cid} names unknown scope fact {fact!r}")
        for gate in view["gates"]:
            known([gate["c"]], "ai_view gates")
            if gate["when"] not in facts:
                raise ModelError(f"ai_view gate names unknown scope fact {gate['when']!r}")
        if set(model.get("opt_in_facts", [])) - facts:
            raise ModelError("opt_in_facts names unknown scope facts")
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


def fact_values(data, opt_in=False):
    """Scope fact values; with opt_in, an AI fact's available_value replaces its default value."""
    facts = data.get("scope_facts") if isinstance(data, dict) else None
    if not isinstance(facts, dict):
        return {}
    out = {}
    for key, value in facts.items():
        if isinstance(value, dict):
            out[key] = value.get("available_value", value.get("value")) if opt_in else value.get("value")
    return out


def _switched_off(gate, data):
    """A criterion is switched off only when its facts are false by default and with opt-in settings."""
    gate = _as_list(gate)
    return bool(gate) and all(fact_values(data).get(f) is False and fact_values(data, True).get(f) is False
                              for f in gate)


def basis_of(data):
    """The assessment's basis: shipped unless it says design."""
    return "design" if isinstance(data, dict) and data.get("basis") == "design" else "shipped"


def _validate_assessed(cid, entry, model, errors, label=None, check_inventory=True, basis="shipped"):
    label = label or cid
    errs = []
    _validate_assessed_inner(cid, entry, model, errs, check_inventory, basis)
    errors.extend(e.replace(f"{cid}:", f"{label}:", 1) if label != cid else e for e in errs)


def _validate_assessed_inner(cid, entry, model, errors, check_inventory, basis):
    score = entry.get("score")
    if not _is_int_score(score):
        errors.append(f"{cid}: score must be an integer 0..4, got {score!r}")
        return
    grade = str(entry.get("grade", "")).upper()
    if grade == "D" and basis != "design":
        errors.append(f"{cid}: grade D (a design document) is only allowed when basis is design")
    elif grade not in ("A", "B", "C", "D"):
        errors.append(f"{cid}: grade must be A, B or C" + (", or D" if basis == "design" else "")
                      + f", got {entry.get('grade')!r}")
    if _text(entry, "evidence").lower() in PLACEHOLDERS:
        errors.append(f"{cid}: assessed criteria need evidence")
    if "confidence" in entry and entry["confidence"] not in CONFIDENCE:
        errors.append(f"{cid}: confidence must be one of {', '.join(CONFIDENCE)}, got {entry['confidence']!r}")
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
    elif cid in model["depth_capped"] and max(readings) >= 3 and basis != "design":
        errors.append(f"{cid}: depth-capped criterion read at 3 or more needs facets")
    if cid not in model["inventories"] or not check_inventory:
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
    if "basis" in data and data["basis"] not in BASES:
        errors.append(f"basis must be one of {', '.join(BASES)}, got {data['basis']!r}")
    basis = basis_of(data)
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
    for fact, entry in raw_facts.items():
        if isinstance(entry, dict) and "available_value" in entry:
            if fact not in model.get("opt_in_facts", []):
                errors.append(f"scope fact {fact}: available_value is only allowed on "
                              + ", ".join(model.get("opt_in_facts", [])))
            elif not isinstance(entry["available_value"], bool):
                errors.append(f"scope fact {fact}: available_value must be true or false")
            elif entry.get("value") is True and entry["available_value"] is False:
                errors.append(f"scope fact {fact}: available_value cannot switch off what is on by default")
    if "ai_view" in model:
        for opt_in, name in ((False, "by default"), (True, "with opt-in settings")):
            fv = fact_values(data, opt_in)
            for fact in ("ai_data_access", "ai_actions"):
                if fv.get(fact) is True and fv.get("ai_features") is not True:
                    errors.append(f"scope fact {fact}: cannot be true {name} while ai_features is not")
    facts = fact_values(data)
    paths = model.get("change_path_facts", [])
    if paths and all(isinstance(facts.get(f), bool) for f in paths) and not any(facts[f] for f in paths):
        errors.append("scope facts: at least one change path (" + " or ".join(paths) + ") must be true")
    _validate_kinds(data, model, errors)
    _validate_proven(data, model, errors, basis)
    _validate_ai_delivery(data, errors)
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
                             ("inventory", "assessed"), ("confidence", "assessed")):
            if key in entry and status != allowed:
                errors.append(f"{cid}: {key} is only allowed when status is {allowed}")
        gate = _as_list(model["applies_when"].get(cid, []))
        switched_off = _switched_off(gate, data)
        if switched_off and status != "not_applicable":
            errors.append(f"{cid}: does not apply because scope fact {' and '.join(gate)} is false; "
                          "mark it not_applicable")
        if status == "assessed":
            _validate_assessed(cid, entry, model, errors, basis=basis)
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
    assessed = [c for c in order if isinstance(scores.get(c), dict) and scores[c].get("status") == "assessed"]
    rated = [c for c in assessed if "confidence" in scores[c]]
    if rated and len(rated) < len(assessed):
        errors.append(f"confidence is all or nothing: {len(rated)} assessed criteria record it, so every assessed "
                      "criterion must; missing on " + ", ".join(c for c in assessed if c not in rated))
    if "ai_view" in model:
        _validate_ai_readings(data, scores, model, errors, basis)
    if not errors:
        # These checks read the default scores, so they run only on an otherwise valid assessment.
        errors += _validate_against_scores(data, criteria, order, model)
    return errors


def _validate_kinds(data, model, errors):
    kinds = data.get("change_kinds")
    hint = ("list the kinds of change operators or users commonly need, 1 to 8, each with id, name, who, "
            "main, reach and evidence, and at least one main kind")
    if kinds is None:
        errors.append("change_kinds: missing; " + hint)
        return
    if not isinstance(kinds, list):
        errors.append("change_kinds must be a list; " + hint)
        return
    if not kinds:
        errors.append("change_kinds: none listed yet; " + hint)
        return
    if len(kinds) > KINDS_MAX:
        errors.append(f"change_kinds: at most {KINDS_MAX} kinds, got {len(kinds)}; fold the rarer ones into the "
                      "nearest kind")
    top, seen, has_main = len(model["reach"]) - 1, set(), False
    for number, kind in enumerate(kinds, 1):
        if not isinstance(kind, dict):
            errors.append(f"change kind {number}: must be an object")
            continue
        kid = kind.get("id")
        label = f"change kind {kid}" if isinstance(kid, str) and kid else f"change kind {number}"
        if not isinstance(kid, str) or not re.match(KIND_ID, kid):
            errors.append(f"{label}: id must be lowercase letters, digits and hyphens, got {kid!r}")
        elif kid in seen:
            errors.append(f"{label}: id is listed more than once")
        seen.add(kid)
        for key in ("name", "who", "evidence"):
            if _text(kind, key).lower() in PLACEHOLDERS:
                errors.append(f"{label}: {key} must be non-empty text")
        if not isinstance(kind.get("main"), bool):
            errors.append(f"{label}: main must be true or false")
        elif kind["main"]:
            has_main = True
        reach = kind.get("reach")
        if not (isinstance(reach, int) and not isinstance(reach, bool) and 0 <= reach <= top):
            errors.append(f"{label}: reach must be an integer 0..{top}, got {reach!r}")
        if "confidence" in kind and kind["confidence"] not in CONFIDENCE:
            errors.append(f"{label}: confidence must be one of {', '.join(CONFIDENCE)}, got {kind['confidence']!r}")
        for key in sorted(set(kind) - set(KIND_FIELDS)):
            errors.append(f"{label}: unknown field {key!r} (allowed: {', '.join(KIND_FIELDS)})")
    if not has_main:
        errors.append("change_kinds: at least one kind must be main")


def _validate_proven(data, model, errors, basis):
    if "proven" not in data:
        return
    if basis == "design":
        errors.append("proven: not allowed when basis is design; a design reading has no operating records")
        return
    proven = data["proven"]
    if not isinstance(proven, dict):
        errors.append("proven must be an object keyed by loop")
        return
    for loop in sorted(set(proven) - set(model["loops"])):
        errors.append(f"proven {loop}: not a loop; use {', '.join(model['loops'])}")
    top = len(model["levels"]) - 1
    for loop in model["loops"]:
        if loop not in proven:
            continue
        entry, label = proven[loop], f"proven {loop}"
        if not isinstance(entry, dict):
            errors.append(f"{label}: must be an object")
            continue
        status = entry.get("status")
        if status == "todo":
            errors.append(f"{label}: not yet assessed; give a level with evidence, or status not_evidenced "
                          "with the searched scope")
            continue
        if status == "not_evidenced":
            allowed = ("status", "searched", "note")
            if _text(entry, "searched").lower() in PLACEHOLDERS:
                errors.append(f"{label}: not_evidenced needs the searched scope")
        elif status is not None:
            errors.append(f"{label}: status must be not_evidenced, or leave it out and give a level, "
                          f"got {status!r}")
            continue
        else:
            allowed = ("level", "evidence", "note")
            level = entry.get("level")
            if not (isinstance(level, int) and not isinstance(level, bool) and 0 <= level <= top):
                errors.append(f"{label}: level must be an integer 0..{top}, got {level!r}")
            if _text(entry, "evidence").lower() in PLACEHOLDERS:
                errors.append(f"{label}: a proven level needs evidence from operating records")
        for key in sorted(set(entry) - set(allowed)):
            errors.append(f"{label}: unknown field {key!r} (allowed: {', '.join(allowed)})")


def _validate_ai_delivery(data, errors):
    if "ai_delivery" not in data:
        return
    record = data["ai_delivery"]
    if not isinstance(record, dict):
        errors.append("ai_delivery must be an object")
        return
    for key in ("present", "qualifies"):
        if not isinstance(record.get(key), bool):
            errors.append(f"ai_delivery: {key} must be true or false, got {record.get(key)!r}")
    if record.get("qualifies") is True and record.get("present") is not True:
        errors.append("ai_delivery: qualifies can be true only when present is true")
    if _text(record, "evidence").lower() in PLACEHOLDERS:
        errors.append("ai_delivery: needs evidence (what was found, or what was searched)")
    if "note" in record and not isinstance(record["note"], str):
        errors.append("ai_delivery: note must be text")
    allowed = ("present", "qualifies", "evidence", "note")
    for key in sorted(set(record) - set(allowed)):
        errors.append(f"ai_delivery: unknown field {key!r} (allowed: {', '.join(allowed)})")


def _needs_text(test, nested=False):
    if "c" in test:
        return f"{test['c']} ≥ {test['min']}"
    for key, joiner in (("any", " or "), ("all", " with ")):
        if key in test:
            text = joiner.join(_needs_text(sub, True) for sub in test[key])
            return f"({text})" if nested else text
    raise ModelError(f"Unrecognised reach test: {test}")


def _meets(test, values):
    """Whether default values meet a reach test. A criterion with no default value (not applicable) fails."""
    if "c" in test:
        return values.get(test["c"]) is not None and values[test["c"]] >= test["min"]
    if "any" in test:
        return any(_meets(sub, values) for sub in test["any"])
    return all(_meets(sub, values) for sub in test["all"])


def _validate_against_scores(data, criteria, order, model):
    """Checks that compare declared readings with the default scores: kinds' reach and proven levels."""
    errors = []
    values, _ = effective_scores(data, order, model, "default")
    for kind in data["change_kinds"]:
        for level in sorted(model.get("reach_needs", {}), key=int):
            test = model["reach_needs"][level]
            if kind["reach"] < int(level) or _meets(test, values):
                continue
            has = ", ".join(f"{c} {'n/a' if values.get(c) is None else values[c]}"
                            for c in dict.fromkeys(_test_ids(test)))
            errors.append(f"change kind {kind['id']}: reach {kind['reach']} ({model['reach'][kind['reach']]}) "
                          f"needs {_needs_text(test)} for reach {level} or more, but has {has}")
    proven = data.get("proven")
    if isinstance(proven, dict) and basis_of(data) == "shipped":
        built = loop_levels(data, values, aggregate(values, criteria, model)["capabilities"], model)
        for loop in model["loops"]:
            entry = proven.get(loop)
            if isinstance(entry, dict) and "level" in entry and entry["level"] > built["loops"][loop]["level"]:
                errors.append(f"proven {loop}: level {entry['level']} is above the built level "
                              f"L{built['loops'][loop]['level']}; a loop cannot be proven above what it is built to do")
    return errors


def _validate_ai_readings(data, scores, model, errors, basis="shipped"):
    view = model["ai_view"]
    required = fact_values(data).get("ai_features") is True or fact_values(data, True).get("ai_features") is True
    for cid in view["readings"]:
        entry = scores.get(cid)
        if not isinstance(entry, dict) or entry.get("status") not in STATUSES:
            continue
        label = f"{cid} (AI)"
        ai = entry.get("ai")
        if ai is None:
            if required:
                errors.append(f"{label}: an AI-qualified reading is required because ai_features is true")
            continue
        if not isinstance(ai, dict):
            errors.append(f"{label}: must be an object")
            continue
        status = ai.get("status")
        if status == "todo":
            errors.append(f"{label}: not yet assessed")
            continue
        if status not in STATUSES:
            errors.append(f"{label}: status must be one of {', '.join(STATUSES)}, got {status!r}")
            continue
        for key in ("alt_score", "available_score", "confidence"):
            if key in ai and key != "confidence" and not _is_int_score(ai[key]):
                errors.append(f"{label}: {key} must be an integer 0..4, got {ai[key]!r}")
            if key in ai and status != "assessed":
                errors.append(f"{label}: {key} is only allowed when status is assessed")
        fact = view["reading_applies_when"].get(cid)
        allowed_na = entry["status"] == "not_applicable" or (fact is not None and _switched_off(fact, data))
        if entry["status"] == "not_applicable" and status != "not_applicable":
            errors.append(f"{label}: must be not_applicable because {cid} is not applicable")
        if status == "assessed":
            _validate_assessed(cid, ai, model, errors, label=label, check_inventory=False, basis=basis)
            surface = view["reading_inventory_surface"].get(cid)
            level = (entry.get("inventory") or {}).get(surface) if surface else None
            if _is_int_score(level) and _is_int_score(ai.get("score")) and ai["score"] != level:
                errors.append(f"{label}: score {ai['score']} must equal the {surface} inventory level {level}")
            for key in ("alt_score", "available_score"):
                if _is_int_score(level) and _is_int_score(ai.get(key)) and ai[key] > level:
                    errors.append(f"{label}: {key} {ai[key]} may not exceed the {surface} inventory level {level}")
        elif status == "not_evidenced":
            if _text(ai, "searched").lower() in PLACEHOLDERS:
                errors.append(f"{label}: not_evidenced needs the searched scope")
        else:
            if _text(ai, "rationale").lower() in PLACEHOLDERS:
                errors.append(f"{label}: not_applicable needs a rationale")
            if not allowed_na:
                errors.append(f"{label}: may be not_applicable only when {cid} is"
                              + (f" or {fact} is false" if fact else "")
                              + "; score missing AI behaviour as 0")


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
    """Rule 13: a 3 or a 4 on a depth-capped criterion needs tested evidence. Operated never changes a score."""
    if cid not in model["depth_capped"] or value < 3:
        return value
    allowed = 4 if entry.get("facets", {}).get("tested") else 2
    if value > allowed:
        flags.append(f"{cid}: evidence depth caps {value} -> {allowed}")
        return allowed
    return value


def effective_scores(data, order, model, variant):
    """Return ({criterion: value or None}, [cap flags]) for one variant."""
    values, flags = {}, []
    depth = basis_of(data) == "shipped"
    for cid in order:
        entry = data["scores"][cid]
        status = entry["status"]
        if status == "not_applicable":
            values[cid] = entry.get("if_applicable") if variant == "all_applicable" else None
            continue
        if status == "not_evidenced":
            values[cid] = None if variant == "assessed_only" else 0
            continue
        values[cid] = _assessed_value(cid, entry, model, variant, flags, depth=depth)
    return values, flags


def _assessed_value(cid, entry, model, variant, flags, use_inventory=True, label=None, depth=True):
    """One assessed entry's value for a variant, after every cap and deduction.
    A design assessment (depth False) has no depth cap."""
    caps, label = model["caps"], label or cid
    value = entry["score"]
    if variant == "high" and "alt_score" in entry:
        value = entry["alt_score"]
    if variant == "available" and "available_score" in entry:
        value = entry["available_score"]
    if str(entry["grade"]).upper() == "C" and value > caps["grade_c_max"]:
        flags.append(f"{label}: grade C caps {value} -> {caps['grade_c_max']}")
        value = caps["grade_c_max"]
    if entry.get("single_entity") is True and value > caps["single_entity_max"]:
        flags.append(f"{label}: single-entity caps {value} -> {caps['single_entity_max']}")
        value = caps["single_entity_max"]
    before = len(flags)
    if depth:
        value = _depth_cap(cid, value, entry, model, flags)
    if use_inventory:
        value = _inventory_cap(cid, value, entry, model, flags)
    if label != cid:
        flags[before:] = [f.replace(f"{cid}:", f"{label}:", 1) for f in flags[before:]]
    if entry.get("incident") is True and value > 0:
        new = max(0, value - caps["incident_penalty"])
        flags.append(f"{label}: incident deduction {value} -> {new}")
        value = new
    return value


def effective_ai_readings(data, model, variant):
    """AI-qualified reading values: {criterion: value or None}, plus not-evidenced ids and flags."""
    values, not_evidenced, flags = {}, [], []
    for cid in model["ai_view"]["readings"]:
        ai = data["scores"][cid].get("ai")
        if not isinstance(ai, dict) or ai.get("status") == "not_applicable":
            values[cid] = None if isinstance(ai, dict) else 0
            continue
        if ai["status"] == "not_evidenced":
            values[cid] = 0
            not_evidenced.append(cid)
            continue
        label = f"{cid} (AI)"
        value = _assessed_value(cid, ai, model, variant, flags, use_inventory=False, label=label,
                                depth=basis_of(data) == "shipped")
        surface = model["ai_view"]["reading_inventory_surface"].get(cid)
        ceiling = (data["scores"][cid].get("inventory") or {}).get(surface) if surface else None
        if _is_int_score(ceiling) and value > ceiling:
            flags.append(f"{label}: {surface} inventory caps {value} -> {ceiling}")
            value = ceiling
        values[cid] = value
    return values, not_evidenced, flags


def _floor_mean(items):
    return math.floor(mean(items) + 1e-9) if items else None


def ai_readiness(data, values, ai_values, ai_not_evidenced, model, opt_in):
    """The AI Readiness View and the AI Capability Footprint for one variant."""
    view = model["ai_view"]
    facts = fact_values(data, opt_in)
    footprint = {area: {"level": _floor_mean([ai_values[c] for c in ids if ai_values.get(c) is not None]),
                        "readings": {c: ai_values.get(c) for c in ids}}
                 for area, ids in view["footprint"].items()}
    if facts.get("ai_features") is not True:
        return {"status": "no_ai_features", "footprint": footprint}
    dimensions, check_ne = {}, []
    for name, dim in view["dimensions"].items():
        contributors = {}
        for cid in dim["checks"]:
            gate = _as_list(model["applies_when"].get(cid, []))
            if gate and not any(facts.get(f) is True for f in gate):
                continue
            if values.get(cid) is None:
                continue
            contributors[cid] = values[cid]
            if data["scores"][cid]["status"] == "not_evidenced":
                check_ne.append(cid)
        for cid in dim["readings"]:
            fact = view["reading_applies_when"].get(cid)
            if fact and facts.get(fact) is not True:
                continue
            if ai_values.get(cid) is None:
                continue
            contributors[f"{cid} (AI)"] = ai_values[cid]
        dimensions[name] = {"level": _floor_mean(list(contributors.values())), "contributors": contributors}
    applicable = [d["level"] for d in dimensions.values() if d["level"] is not None]
    level = min(applicable) if applicable else 0
    gates = []
    for gate in view["gates"]:
        if facts.get(gate["when"]) is not True:
            gates.append({"gate": gate["gate"], "needs": f"{gate['c']} ≥ {gate['min']}", "observed": "n/a",
                          "status": "n/a"})
            continue
        observed = values.get(gate["c"]) or 0
        gates.append({"gate": gate["gate"], "needs": f"{gate['c']} ≥ {gate['min']}", "observed": observed,
                      "status": "pass" if observed >= gate["min"] else "fail"})
    failed = [g for g in gates if g["status"] == "fail"]
    uncapped = level
    if failed:
        level = min(level, view["gate_cap"])
    return {"status": "assessed", "level": level, "name": view["levels"][level], "uncapped": uncapped,
            "label": view["gate_label"] if failed else None, "dimensions": dimensions, "gates": gates,
            "not_evidenced": sorted(set(check_ne) | {f"{c} (AI)" for c in ai_not_evidenced}),
            "footprint": footprint}


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

    def _crit(self, cid, minimum):
        """(passed, observed) for one criterion; a not-applicable criterion passes."""
        if self.data["scores"][cid]["status"] == "not_applicable":
            return True, "n/a"
        value = self.values.get(cid) or 0
        return value >= minimum, value

    def _path(self, loop, who, minimum):
        observed = []
        for alt in self.model["build_paths"][loop][who]:
            if "kinds" in alt:
                kinds = kinds_summary(self.data)
                ok = kinds["value"] >= minimum
                observed.append(f"kinds {kinds['main_self_serve']} of {kinds['main']} main self-serve")
            elif "cap" in alt:
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
                if ok and alt.get("serves_main"):
                    # The lane counts only when it carries a main kind of change at least this far.
                    reach = max((k["reach"] for k in self.data.get("change_kinds") or []
                                 if k.get("main") is True and isinstance(k.get("reach"), int)), default=0)
                    observed[-1] += f" serving a main kind at reach {reach}"
                    ok = reach >= minimum
            if ok:
                return True, ", ".join(observed)
        return False, ", ".join(observed)

    def _rollback(self, minimum):
        ok_all, observed = True, []
        for item in self.model["rollback"]:
            if item.get("when") and self.facts.get(item["when"]) is not True:
                continue
            ok, value = self._crit(item["c"], minimum)
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
        if "c" in cond:
            ok, value = self._crit(cond["c"], cond["min"])
            return ok, f"{cond['c']} ≥ {cond['min']}", str(value)
        if "path" in cond:
            ok, observed = self._path(loop, cond["path"], cond["min"])
            return ok, f"{cond['path']} build path ≥ {cond['min']}", observed
        if "rollback" in cond:
            ok, observed = self._rollback(cond["rollback"])
            return ok, f"rollback ≥ {cond['rollback']}", observed
        if "every" in cond:
            below = []
            for ids in self.model["areas"][cond["every"]].values():
                for cid in ids:
                    ok, value = self._crit(cid, cond["min"])
                    if not ok:
                        below.append(f"{cid} {value}")
            return not below, f"every applicable {cond['every']} ≥ {cond['min']}", \
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


def ai_driven(data, values, ai_values, capabilities, model, sal):
    """How far AI itself carries each loop: the loop rules re-run with each AI-performable stage
    criterion replaced by its AI-qualified reading. Never above the loop's own level."""
    driven = model["ai_view"]["driven"]
    subs = {c for ids in driven.values() for c in ids}
    swapped = dict(values)
    for cid in subs:
        if values.get(cid) is not None:
            swapped[cid] = ai_values.get(cid) if ai_values.get(cid) is not None else 0
    run = loop_levels(data, swapped, capabilities, model)
    loops = {}
    for loop in model["loops"]:
        level = min(run["loops"][loop]["level"], sal["loops"][loop]["level"])
        # L1 is people configuring the product; AI first drives a stage at L2, so below that it drives none.
        level = level if level >= AI_DRIVEN_MIN else 0
        # The AI stage conditions the AI-only run must meet for its next level.
        blockers = [b for b in run["loops"][loop]["blockers"]
                    if any(c in f"{b['needs']} {b['observed']}" for c in subs)]
        loops[loop] = {"level": level, "name": model["levels"][level] if level else AI_DRIVEN_NONE,
                       "stages": {c: ai_values.get(c) for c in driven.get(loop, [])},
                       "blockers": blockers}
    headline = min(loops[l]["level"] for l in model["headline"])
    return {"headline": headline, "headline_name": model["levels"][headline] if headline else AI_DRIVEN_NONE,
            "loops": loops}


def sensitivity(data, values, criteria, model):
    """Criteria whose one-level change would move the headline or a loop level.

    Raw criterion values are moved up or down by one; caps are not re-applied, so this
    shows how close the reading sits to a boundary, not what evidence would be needed.
    """
    base = loop_levels(data, values, aggregate(values, criteria, model)["capabilities"], model)
    raise_headline, lower_headline, raise_loop, lower_loop = [], [], {}, {}
    ai_checks = {c for ids in model.get("ai_areas", {}).get("AIR", {}).values() for c in ids}
    for cid, value in values.items():
        if value is None or data["scores"][cid]["status"] != "assessed" or cid in ai_checks:
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


def kinds_summary(data):
    """The kinds-of-change build path: 2 when every main kind is self-serve (reach 1 or more),
    1 when any kind is, 0 otherwise; with the counts behind it."""
    kinds = [k for k in data.get("change_kinds") or [] if isinstance(k, dict)]

    def serve(kind):
        reach = kind.get("reach")
        return isinstance(reach, int) and not isinstance(reach, bool) and reach >= 1

    main = [k for k in kinds if k.get("main") is True]
    main_serve = sum(1 for k in main if serve(k))
    any_serve = sum(1 for k in kinds if serve(k))
    value = 2 if main and main_serve == len(main) else 1 if any_serve else 0
    return {"value": value, "kinds": len(kinds), "self_serve": any_serve, "main": len(main),
            "main_self_serve": main_serve, "text": f"{main_serve} of {len(main)} main kinds are self-serve"}


def kinds_table(data, model):
    """Every kind of change with its reach name, in the order listed."""
    out = []
    for kind in data.get("change_kinds") or []:
        row = {k: kind[k] for k in KIND_FIELDS if k in kind}
        row["reach_name"] = model["reach"][kind["reach"]]
        out.append(row)
    return out


def proven_reading(data, sal, model):
    """What operating records show, per loop, beside what the product is built to do. None for a design basis."""
    if basis_of(data) == "design":
        return None
    proven = data.get("proven") if isinstance(data.get("proven"), dict) else {}
    loops = {}
    for loop in model["loops"]:
        entry, built = proven.get(loop), sal["loops"][loop]["level"]
        if isinstance(entry, dict) and "level" in entry:
            loops[loop] = {"status": "evidenced", "level": entry["level"], "built": built,
                           "evidence": entry.get("evidence")}
        elif isinstance(entry, dict) and entry.get("status") == "not_evidenced":
            loops[loop] = {"status": "not_evidenced", "level": None, "built": built,
                           "searched": entry.get("searched")}
        else:
            loops[loop] = {"status": "not_recorded", "level": None, "built": built}
    levels = [loops[l]["level"] for l in model["headline"]]
    headline = None if None in levels else min(levels)
    text = "Proven: not evidenced" if headline is None else \
        f"Proven: SAL {headline} ({model['levels'][headline]})"
    return {"headline": headline, "headline_name": None if headline is None else model["levels"][headline],
            "text": text, "loops": loops}


def recursion_reading(data, values, model):
    """The Recursion line: how far the loop improves its own checks, named from LRN-10's default score."""
    status, value = data["scores"][RECURSION]["status"], values.get(RECURSION)
    name = None if value is None else model["recursion"][value]
    if value is None:
        text = f"Recursion: not applicable ({RECURSION} excluded)"
    elif status == "not_evidenced":
        text = f"Recursion: {value} {name} ({RECURSION} not evidenced, counted as 0)"
    else:
        text = f"Recursion: {value} {name} ({RECURSION} at {value})"
    return {"criterion": RECURSION, "status": status, "score": value, "name": name, "text": text}


def ai_delivery_reading(data):
    """The AI delivery record, with a plain sentence. It never changes a score."""
    record = data.get("ai_delivery")
    if not isinstance(record, dict):
        return {"recorded": False, "present": None, "qualifies": None, "evidence": None, "note": None,
                "text": "No AI delivery record. Engineers building a product with AI coding agents is "
                        "AI-assisted engineering, not the product evolving itself."}
    if not record["present"]:
        text = ("Engineers are not seen building this product with AI coding agents or a delivery framework. "
                "Any self-evolution scored here is the product's own.")
    elif record["qualifies"]:
        text = ("Engineers build this product with AI coding agents or a delivery framework. AI-assisted "
                "engineering is not the product evolving itself, but this setup is installed, enforced and limited "
                "as part of the product, so the assessment may credit it as the product's own way of changing.")
    else:
        text = ("Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted "
                "engineering, not the product evolving itself. It is not installed, enforced and limited as part "
                "of the product, so it earns no credit.")
    return {"recorded": True, "present": record["present"], "qualifies": record["qualifies"],
            "evidence": record.get("evidence"), "note": record.get("note"), "text": text}


def confidence_summary(data, criteria, order, model, sal):
    """Counts of each confidence level, and the low-confidence criteria that hold a next-level
    blocker or an applicable critical control ("check these first")."""
    scores = data["scores"]

    def count(entries):
        out = {c: 0 for c in CONFIDENCE}
        out["none"] = 0
        for entry in entries:
            out[entry.get("confidence", "none")] += 1
        return out

    assessed = [c for c in order if scores[c]["status"] == "assessed"]
    readings = [scores[c]["ai"] for c in model.get("ai_view", {}).get("readings", [])
                if isinstance(scores[c].get("ai"), dict) and scores[c]["ai"].get("status") == "assessed"]
    holds = {}
    for loop, name in model["loops"].items():
        info = sal["loops"][loop]
        for blocker in info["blockers"]:
            for cid in re.findall(ID, f"{blocker['needs']} {blocker['observed']}"):
                holds.setdefault(cid, []).append(f"{name} to L{info['level'] + 1}")
    for ctl in sal["controls"]:
        if ctl["status"] != "n/a":
            for cid in re.findall(ID, ctl["needs"]):
                holds.setdefault(cid, []).append(f"{ctl['control']} control")
    check = [{"id": c, "title": criteria[c]["title"], "holds": list(dict.fromkeys(holds[c]))}
             for c in assessed if scores[c].get("confidence") == "low" and c in holds]
    return {"recorded": any("confidence" in scores[c] for c in assessed),
            "criteria": count(scores[c] for c in assessed), "ai_readings": count(readings),
            "change_kinds": count(k for k in data.get("change_kinds") or []), "check_first": check}


def score_assessment(data, criteria, order, model):
    result = {"variants": {}, "flags": []}
    for variant in VARIANTS:
        values, flags = effective_scores(data, order, model, variant)
        agg = aggregate(values, criteria, model)
        entry = {"effective": values, **agg}
        if variant in SAL_VARIANTS:
            entry["sal"] = loop_levels(data, values, agg["capabilities"], model)
            if "ai_view" in model:
                ai_values, ai_ne, ai_flags = effective_ai_readings(data, model, variant)
                if "driven" in model["ai_view"]:
                    entry["sal"]["ai_driven"] = ai_driven(data, values, ai_values, agg["capabilities"],
                                                          model, entry["sal"])
                entry["ai_readiness"] = ai_readiness(data, values, ai_values, ai_ne, model,
                                                     opt_in=(variant == "available"))
                entry["ai_flags"] = ai_flags
        result["variants"][variant] = entry
        if variant == "default":
            result["flags"] = flags + entry.get("ai_flags", [])
            result["sensitivity"] = sensitivity(data, values, criteria, model)
    coverage = {s: 0 for s in STATUSES}
    grades = {"A": 0, "B": 0, "C": 0, "D": 0}
    for cid in order:
        entry = data["scores"][cid]
        coverage[entry["status"]] += 1
        if entry["status"] == "assessed":
            grades[str(entry["grade"]).upper()] += 1
    result["coverage"], result["grades"] = coverage, grades
    default_sal = result["variants"]["default"]["sal"]
    result["basis"] = basis_of(data)
    result["kinds"] = kinds_summary(data)
    result["proven"] = proven_reading(data, default_sal, model)
    result["recursion"] = recursion_reading(data, result["variants"]["default"]["effective"], model)
    result["ai_delivery"] = ai_delivery_reading(data)
    result["confidence"] = confidence_summary(data, criteria, order, model, default_sal)
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


def headline_text(sal, model, with_progress=False, basis="shipped", proven=None):
    """`Built to SAL n (Name) · Proven: … · AI-driven n · loops`, or `Designed for SAL n …` for a design basis.
    Proven appears only when given, and never for a design basis."""
    drv = sal.get("ai_driven")
    loops = " · ".join(f"{model['loops'][l]} L{sal['loops'][l]['level']}"
                       + (f" (AI L{drv['loops'][l]['level']})" if drv else "")
                       + (progress(sal["loops"][l]) if with_progress else "") for l in model["loops"])
    claim = "Designed for" if basis == "design" else "Built to"
    shown = f" · {proven['text']}" if proven and basis != "design" else ""
    ai = f" · AI-driven {drv['headline']}" if drv else ""
    return f"{claim} SAL {sal['headline']} ({sal['headline_name']}){shown}{ai} · {loops}"


def result_headline(result, model):
    """The default headline of a scored assessment, with its basis and proven reading."""
    return headline_text(result["variants"]["default"]["sal"], model, basis=result["basis"], proven=result["proven"])


def ai_headline_text(view_result, model):
    if view_result["status"] != "assessed":
        return "no AI features"
    dims = " · ".join(f"{name} {'n/a' if d['level'] is None else d['level']}"
                      for name, d in view_result["dimensions"].items())
    text = f"AI Readiness L{view_result['level']} ({view_result['name']}) · {dims}"
    if view_result["label"]:
        text += f" · {view_result['label']}"
    return text


def render_ai_driven(sal, model):
    drv = sal.get("ai_driven")
    if not drv:
        return []
    lines = ["", "### What AI drives", "",
             "Each loop re-scored with its AI-performable stages read only on what AI does there. "
             "AI first drives a stage at L2, and never above the loop's own level.", "",
             "| Loop | Level | AI-driven | AI stage readings | What AI needs for its next level |", "|---|---:|---:|---|---|"]
    for loop, name in model["loops"].items():
        info = drv["loops"][loop]
        stages = ", ".join(f"{c} {'n/a' if v is None else v}" for c, v in info["stages"].items()) or "–"
        needs = "; ".join(f"{b['needs']} (has {b['observed']})" for b in info["blockers"]) or "–"
        lines.append(f"| {name} | L{sal['loops'][loop]['level']} | L{info['level']} | {stages} | {cell(needs)} |")
    return lines


def render_ai(result, model):
    if "ai_view" not in model:
        return []
    d, avail, high = (result["variants"][v]["ai_readiness"] for v in ("default", "available", "high"))
    lines = ["", "## AI Readiness", "",
             "How safely can the product run AI in production? Separate from SAL, which it never changes.", "",
             f"**{ai_headline_text(d, model)}**", "",
             f"- With opt-in settings: {ai_headline_text(avail, model)}.",
             f"- With every alternate reading: {ai_headline_text(high, model)}."]
    shown = d if d["status"] == "assessed" else avail
    if shown["status"] == "assessed":
        if shown is avail:
            lines += ["", "No AI features by default; the tables below show the opt-in reading."]
        lines += ["", "| Dimension | Level | Contributors |", "|---|---:|---|"]
        for name, dim in shown["dimensions"].items():
            contributors = ", ".join(f"{k} {v}" for k, v in dim["contributors"].items()) or "none applicable"
            lines.append(f"| {name} | {'n/a' if dim['level'] is None else dim['level']} | {cell(contributors)} |")
        lines += ["", "| AI gate | Needs | Observed | Status |", "|---|---|---|---|"]
        for gate in shown["gates"]:
            lines.append(f"| {gate['gate']} | {gate['needs']} | {gate['observed']} | {gate['status']} |")
        if shown["not_evidenced"]:
            lines += ["", "Not evidenced (computed as 0): " + ", ".join(shown["not_evidenced"]) + "."]
    fp = shown["footprint"]
    lines += ["", "### AI Capability Footprint", "",
              "What the product's AI does. Descriptive levels per area, with no headline: it never changes AI Readiness or SAL.", "",
              "| Area | Level | Readings |", "|---|---:|---|"]
    for area, info in fp.items():
        readings = ", ".join(f"{k} {'n/a' if v is None else v}" for k, v in info["readings"].items())
        lines.append(f"| {area} | {'–' if info['level'] is None else info['level']} | {readings} |")
    return lines


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
    basis = result["basis"]
    design = basis == "design"
    lines = [f"# EVOLVE assessment: {cell(data.get('product'))}", "",
             f"Framework {model['framework']} {model['version']}. Date {cell(data.get('date'))}. "
             f"Source {cell(data.get('source'))}. Archetype **{data.get('archetype')}**. "
             f"Basis **{basis}** ({'design documents' if design else 'what ships'}).", ""]
    if design:
        lines += [f"**Design reading.** {DESIGN_NOTE} Grade D evidence is allowed and the depth cap does not apply.",
                  ""]
    lines += [f"Scope facts true: {', '.join(on) or 'none'}. False: {', '.join(off) or 'none'}.", "",
             f"Coverage: {cov['assessed']} assessed, {cov['not_evidenced']} not evidenced, "
             f"{cov['not_applicable']} not applicable. Grades: {grades['A']} A, {grades['B']} B, {grades['C']} C"
             + (f", {grades['D']} D" if design or grades["D"] else "") + ".", "",
             confidence_text(result["confidence"]), "",
             "## Software Autonomy Level", "",
             f"**{result_headline(result, model)}**", "",
             f"Progress toward the next level: " + "; ".join(
                 f"{name} {sal['loops'][l]['next_met']} of {sal['loops'][l]['next_total']} conditions for "
                 f"L{sal['loops'][l]['level'] + 1}" for l, name in model["loops"].items()
                 if sal["loops"][l]["next_total"]) + ".", "",
             f"- With opt-in settings: {headline_text(avail, model, basis=basis)}.",
             f"- With every alternate reading: {headline_text(high, model, basis=basis)}.", "",
             "| Loop | Stages | Spine | Architecture | Governance | Level | AI-driven | With opt-in settings |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    drv = sal.get("ai_driven")
    for loop, name in model["loops"].items():
        info = sal["loops"][loop]
        parts = " | ".join(f"L{info['parts'][p]}" for p in PARTS)
        ai_cell = f"L{drv['loops'][loop]['level']}" if drv else "–"
        lines.append(f"| {name} | {parts} | **L{info['level']}** | {ai_cell} | L{avail['loops'][loop]['level']} |")
    lines += ["", f"**{result['recursion']['text']}.** How far the loop improves its own checks, evaluation sets, "
              "policies and prompts from measured results.", "",
              f"**AI delivery.** {result['ai_delivery']['text']}"]
    lines += render_kinds(data, model, result)
    lines += render_proven(result, model)
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
    lines += render_ai_driven(sal, model)
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
    lines += render_ai(result, model)
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
        ai = entry.get("ai")
        if isinstance(ai, dict) and ai.get("status"):
            ai_text = ai["score"] if ai["status"] == "assessed" else ai["status"].replace("_", " ")
            text = f"AI-qualified reading: {ai_text}. " + text
        lines.append(f"| {cid} {cell(criteria[cid]['title'])} | {status} | "
                     f"{'excluded' if value is None else value} | {entry.get('alt_score', '')} | "
                     f"{entry.get('available_score', '')} | {grade_cell(entry)} | "
                     f"{facet_text} | {cell(text)} |")
    lines += ["", "Grade cell: evidence grade, then confidence where recorded. Facets: I implemented, T tested, "
              "O operated. Operated supports a Proven reading and never changes a score."]
    return "\n".join(lines)


def grade_cell(entry):
    if entry["status"] != "assessed":
        return "-"
    return str(entry.get("grade", "-")) + (f", {entry['confidence']}" if entry.get("confidence") else "")


def confidence_text(conf):
    if not conf["recorded"]:
        return "Confidence: not recorded."
    c = conf["criteria"]
    text = f"Confidence: {c['high']} high, {c['medium']} medium, {c['low']} low across the assessed criteria."
    if conf["check_first"]:
        text += " Check these first (low confidence, and they hold a blocker or a critical control): " + "; ".join(
            f"{i['id']} ({', '.join(i['holds'])})" for i in conf["check_first"]) + "."
    else:
        text += " No low-confidence criterion holds a next-level blocker or a critical control."
    return text


def render_kinds(data, model, result):
    kinds = result["kinds"]
    lines = ["", "### Kinds of change", "",
             f"{kinds['text']} (reach 1 or more: the people running the product make it themselves and can undo it).",
             "", "| Kind | Who | Main | Reach | Evidence |", "|---|---|---|---|---|"]
    for kind in kinds_table(data, model):
        conf = f" Confidence {kind['confidence']}." if kind.get("confidence") else ""
        lines.append(f"| {cell(kind['name'])} (`{kind['id']}`) | {cell(kind['who'])} | "
                     f"{'yes' if kind['main'] else 'no'} | {kind['reach']} {kind['reach_name']} | "
                     f"{cell(kind['evidence'])}{conf} |")
    return lines


def render_proven(result, model):
    proven = result["proven"]
    if proven is None:
        return ["", "### Proven", "", "Not read: a design assessment has no operating records. " + DESIGN_NOTE]
    lines = ["", "### Proven", "",
             f"**{proven['text']}.** What operating records show real changes doing, beside what the product is "
             f"built to do. {PROVEN_NOTE}", "",
             "| Loop | Built | Proven | Operating records, or what was searched |", "|---|---:|---|---|"]
    for loop, name in model["loops"].items():
        info = proven["loops"][loop]
        if info["status"] == "evidenced":
            shown, text = f"L{info['level']}", info["evidence"]
        elif info["status"] == "not_evidenced":
            shown, text = "not evidenced", "Searched: " + str(info["searched"])
        else:
            shown, text = "not recorded", "–"
        lines.append(f"| {name} | L{info['built']} | {shown} | {cell(text)} |")
    return lines


def describe_condition(cond, loop, criteria, model, facts, kinds=()):
    """Plain words for one level condition, from the rubric's own anchored levels."""
    if "c" in cond:
        info = criteria[cond["c"]]
        return f"{cond['c']} {info['title']}: {info['anchors'][cond['min']]}"
    if "path" in cond:
        parts = []
        for alt in model["build_paths"][loop][cond["path"]]:
            if "kinds" in alt:
                if cond["min"] >= 2:
                    text = "Every main kind of change can be made by the people running the product, and undone."
                    waiting = [k["name"] for k in kinds if k.get("main") and k.get("reach", 0) < 1]
                    if waiting:
                        text += " Not yet: " + "; ".join(waiting) + "."
                else:
                    text = "At least one kind of change can be made by the people running the product, and undone."
                parts.append(text)
            elif "cap" in alt:
                label = model["capabilities"][alt["cap"]]
                parts.append(f"The {label} ({alt['cap']}) capability averages {cond['min']} or more.")
            else:
                text = f"{alt['c']} {criteria[alt['c']]['title']}: {criteria[alt['c']]['anchors'][cond['min']]}"
                if "with" in alt:
                    w = alt["with"]
                    text += f" (with {w['c']} {criteria[w['c']]['title']}: {criteria[w['c']]['anchors'][w['min']]})"
                if alt.get("serves_main"):
                    text += (f" It counts only for a main kind of change it carries to reach {cond['min']} or more"
                             f" ({model['reach'][min(cond['min'], 5)]}).")
                parts.append(text)
        who = "People build the change" if cond["path"] == "people" else "The product builds the change"
        return f"{who}. " + " Or: ".join(parts)
    if "rollback" in cond:
        items = [f"{r['c']} {criteria[r['c']]['title']}: {criteria[r['c']]['anchors'][cond['rollback']]}"
                 for r in model["rollback"] if not r.get("when") or facts.get(r["when"]) is True]
        return " ".join(items)
    if "every" in cond:
        label = model["capabilities"][cond["every"]]
        return f"Every applicable {label} ({cond['every']}) criterion is at {cond['min']} or more."
    for key, joiner in (("any", " Or: "), ("all", " And: ")):
        if key in cond:
            return joiner.join(describe_condition(sub, loop, criteria, model, facts, kinds) for sub in cond[key])
    raise ModelError(f"Unrecognised condition: {cond}")


def checklist(data, criteria, model, default, target):
    """What done means for each loop at the target level: the challenge to run on the product, and every
    condition the next assessment must find, from the target level and any lower level not yet met."""
    ev = Evaluator(data, default["effective"], default["capabilities"], model)
    loops = {}
    for loop, name in model["loops"].items():
        now = default["sal"]["loops"][loop]["level"]
        items = []
        for level in range(1, target + 1):
            for cond in model["conditions"].get(str(level), []):
                if cond.get("loop") not in (None, loop):
                    continue
                ok, needs, observed = ev.test(cond, loop)
                if observed == "n/a" or (ok and level < target):
                    continue
                items.append({"level": level, "part": cond["part"], "stage": cond["stage"],
                              "control": cond.get("control"), "needs": needs, "observed": observed, "met": ok,
                              "description": describe_condition(cond, loop, criteria, model, ev.facts,
                                                                data.get("change_kinds") or [])})
        loops[loop] = {"name": name, "level": now, "target": target, "challenge": model["challenges"][str(target)][loop],
                       "items": items}
    return loops


def render_checklist(product, loops, model, today):
    lines = [f"# Definition of done: {cell(product)} to L{next(iter(loops.values()))['target']}", "",
             f"Today: {today}.", "",
             "A loop is done at the target level when its challenge passes on the running product and a fresh "
             "assessment finds every item below. On a depth-capped criterion, a score of 3 or 4 needs automated "
             "tests in scope (the `tested` facet). Records of it working in production support a Proven reading, "
             "reported separately; they never change the level.", ""]
    for loop in loops.values():
        lines.append(f"## {loop['name']}: L{loop['level']} → L{loop['target']}")
        lines.append("")
        if loop["level"] >= loop["target"]:
            lines += [f"Already at L{loop['level']}.", ""]
            continue
        lines += [f"**Challenge.** {loop['challenge']}", "", "**Evidence the next assessment must find:**", ""]
        for item in loop["items"]:
            box = "x" if item["met"] else " "
            tag = f" Critical control: {item['control']}." if item.get("control") else ""
            lines.append(f"- [{box}] **{item['stage']}** (L{item['level']}, now {cell(item['observed'])}). "
                         f"{cell(item['description'])}{tag}")
        met = sum(i["met"] for i in loop["items"])
        lines += ["", f"{met} of {len(loop['items'])} met.", ""]
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate, score and prescribe an EVOLVE assessment.")
    parser.add_argument("scores")
    parser.add_argument("--rubric", default=DEFAULT_RUBRIC)
    parser.add_argument("--remediation", default=DEFAULT_REMEDIATION)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--quiet", action="store_true", help="print only the SAL and profile summary")
    parser.add_argument("--prescribe", action="store_true")
    parser.add_argument("--target", type=int, choices=(3, 4), default=3)
    parser.add_argument("--checklist", type=int, choices=(1, 2, 3, 4, 5), metavar="LEVEL",
                        help="print what done means for each loop at this autonomy level")
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

    if args.checklist:
        loops = checklist(data, criteria, model, default, args.checklist)
        if args.json:
            print(json.dumps({"product": data.get("product"), "target": args.checklist, "loops": loops},
                             indent=2, ensure_ascii=False))
        else:
            print(render_checklist(data.get("product"), loops, model, result_headline(result, model)), end="")
        return 0

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
        print(f"Current: {result_headline(result, model)}.\n")
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
        out = {"headline": sal["headline"], "headline_name": sal["headline_name"],
               "loops": {l: {"level": v["level"], "parts": v["parts"]} for l, v in sal["loops"].items()}}
        if "ai_driven" in sal:
            out["ai_driven"] = {"headline": sal["ai_driven"]["headline"],
                                "loops": {l: v["level"] for l, v in sal["ai_driven"]["loops"].items()}}
        return out

    payload = {"product": data.get("product"), "date": data.get("date"), "source": data.get("source"),
               "archetype": data.get("archetype"), "framework": model["framework"],
               "framework_version": model["version"],
               "basis": result["basis"],
               "headline_text": result_headline(result, model),
               "scope_facts": {f: data["scope_facts"][f]["value"] for f in model["scope_facts"]},
               "coverage": result["coverage"], "grades": result["grades"],
               "sal": default["sal"],
               "change_kinds": kinds_table(data, model),
               "kinds_summary": result["kinds"],
               "proven": result["proven"],
               "recursion": result["recursion"],
               "ai_delivery": result["ai_delivery"],
               "confidence": result["confidence"],
               "sensitivity": result["sensitivity"],
               **({"ai_readiness": {v: result["variants"][v]["ai_readiness"] for v in SAL_VARIANTS}}
                  if "ai_view" in model else {}),
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
        print(result_headline(result, model))
        if result["basis"] == "design":
            print(DESIGN_NOTE)
        if "ai_view" in model:
            print(ai_headline_text(default["ai_readiness"], model))
        print("  ".join(f"{label} {fmt(default['capabilities'][cap])}" for cap, label in model["capabilities"].items()))
        return 0
    print(render_markdown(data, criteria, order, model, result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
