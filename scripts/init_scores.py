#!/usr/bin/env python3
"""Create an EVOLVE assessment template from the rubric.

Every scope fact starts as null and every criterion as status "todo". The
scorer refuses to score the file until each fact is true or false with
evidence and each criterion is assessed, marked not_evidenced with a search scope, or
excluded with a rationale the archetype or a scope fact allows.
"""

import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from score import DEFAULT_RUBRIC, load_rubric  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--product", required=True)
    parser.add_argument("--archetype", required=True)
    parser.add_argument("--source", required=True, help="repositories and immutable tips")
    parser.add_argument("--date", default=datetime.date.today().isoformat())
    parser.add_argument("--rubric", default=DEFAULT_RUBRIC)
    parser.add_argument("--out", help="write here instead of stdout; refuses to overwrite")
    args = parser.parse_args(argv)

    _criteria, order, model = load_rubric(args.rubric)
    if args.archetype not in model["archetype_exclusions"]:
        parser.error("archetype must be one of: " + ", ".join(sorted(model["archetype_exclusions"])))
    output = {
        "product": args.product,
        "date": args.date,
        "source": args.source,
        "archetype": args.archetype,
        "framework": model["framework"],
        "framework_version": model["version"],
        "scope_facts": {fact: {"value": None, "evidence": ""} for fact in model["scope_facts"]},
        "scores": {cid: {"status": "todo"} for cid in order},
    }
    text = json.dumps(output, indent=2) + "\n"
    if args.out:
        if os.path.exists(args.out):
            parser.error(f"{args.out} exists; keep prior inputs and choose a new file name")
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
