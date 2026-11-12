"""Foundation 7: checks that run on every change, stored as definitions so they can grow.

A check is a question and the outcome it must get. A change is rejected when it makes a check
that passes today fail (a regression). A new check that fails today records a known problem and
does not block unrelated changes; the change that fixes it turns it green, and from then on it
guards against the problem coming back.
"""
from .desk import apply, resolve


def passes(case, views):
    result = resolve(case["question"], views["answers"], views["routing-rules"])
    return all(result.get(name) == value for name, value in case["expect"].items())


def run(check_cases, before, kind, key, body):
    """Run every check against today's definitions and against them with the change applied."""
    after = dict(before, **{kind: apply(before[kind], key, body)})
    results = []
    for case_key, case in sorted(check_cases.items()):
        results.append({"check": case_key, "before": passes(case, before), "after": passes(case, after)})
    return {
        "ran": len(results),
        "regressions": [r["check"] for r in results if r["before"] and not r["after"]],
        "fixed": [r["check"] for r in results if r["after"] and not r["before"]],
        "failing": [r["check"] for r in results if not r["after"]],
    }
