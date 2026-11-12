"""Foundations 1 and 2: the declared kinds of change, and validation of their versioned data."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KINDS_PATH = os.path.join(ROOT, "kinds.json")
KEY_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,47}$")


def load_kinds(path=KINDS_PATH):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def traffic_kinds(kinds):
    return [k for k, d in kinds.items() if d.get("traffic")]


def validate_body(kind_def, body):
    """Return a list of plain error messages; an empty list means the body is valid.

    A body of None means "remove this definition" and is valid here; the policy decides who may do it.
    """
    if body is None:
        return []
    if not isinstance(body, dict):
        return ["the definition must be a JSON object"]
    fields = kind_def["fields"]
    errors = ["unknown field '%s'" % name for name in sorted(body) if name not in fields]
    for name, spec in fields.items():
        if name not in body:
            if spec.get("required"):
                errors.append("missing field '%s'" % name)
            continue
        errors.extend(_check_value(name, body[name], spec))
    return errors


def _check_value(name, value, spec):
    kind = spec["type"]
    if kind == "str":
        if not isinstance(value, str) or not value.strip():
            return ["'%s' must be non-empty text" % name]
        if len(value) > spec.get("max_length", 10000):
            return ["'%s' is longer than %d characters" % (name, spec["max_length"])]
    elif kind == "int":
        if not isinstance(value, int) or isinstance(value, bool):
            return ["'%s' must be a whole number" % name]
        if value < spec.get("min", value) or value > spec.get("max", value):
            return ["'%s' must be between %s and %s" % (name, spec.get("min"), spec.get("max"))]
    elif kind == "list[str]":
        if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
            return ["'%s' must be a list of words" % name]
        if not spec.get("min_items", 0) <= len(value) <= spec.get("max_items", 1000):
            return ["'%s' must have %d to %d items" % (name, spec.get("min_items", 0), spec.get("max_items", 1000))]
        pattern = spec.get("pattern")
        if pattern and not all(re.match(pattern, v) for v in value):
            return ["'%s' items must match %s" % (name, pattern)]
    elif kind == "dict":
        if not isinstance(value, dict):
            return ["'%s' must be an object" % name]
        allowed = spec.get("keys")
        if allowed is not None:
            if not value:
                return ["'%s' needs at least one of %s" % (name, ", ".join(allowed))]
            extra = sorted(set(value) - set(allowed))
            if extra:
                return ["'%s' has unknown keys: %s" % (name, ", ".join(extra))]
    return []
